import random
import numpy as np
import sys 

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import torch.backends.cudnn as cudnn
import torchvision
import torchvision.transforms as transforms
import matplotlib.pyplot as plt 
from sklearn.decomposition import PCA

# from dedpul import *
# from data import *
# from models import *
# from mmd import *
# from helper import * 
# from KM import *
# from TIcE import tice

def p_probs(net, device, p_loader,isIMDbBERT=False): 
    net.eval()
    pp_probs = None
    with torch.no_grad():
        for batch_idx, (_, inputs, targets) in enumerate(p_loader):
           
            if isIMDbBERT:
                vinput_ids = inputs['input_ids'].to(device)
                vlabels = targets.to(device)
                vattention_mask = inputs['attention_mask'].to(device)
                voutputs = net(vinput_ids, attention_mask=vattention_mask, labels=vlabels)
                outputs = voutputs[1]
            else:
                inputs = inputs.to(device)
                outputs = net(inputs)

            probs = torch.nn.functional.softmax(outputs, dim=-1)[:,0] 
#             probs = torch.stack((probs, 1-probs), dim=1)
#             probs = probs.to(torch.int32)
            if pp_probs is None: 
                pp_probs = probs.detach().cpu().numpy().squeeze()
            else:
                pp_probs = np.concatenate((pp_probs, \
                    probs.detach().cpu().numpy().squeeze()), axis=0)
    
    return pp_probs    

def u_probs(net, device, u_loader,isIMDbBERT=False):
    net.eval()
    pu_probs = None
    pu_targets = None
    with torch.no_grad():
        for batch_idx, (_, inputs, _, targets) in enumerate(u_loader):
            if isIMDbBERT:
                vinput_ids = inputs['input_ids'].to(device)
                vlabels = targets.to(device)
                vattention_mask = inputs['attention_mask'].to(device)
                voutputs = net(vinput_ids, attention_mask=vattention_mask, labels=vlabels)
                outputs = voutputs[1]
            else:
                inputs = inputs.to(device)
                outputs = net(inputs)
                
            probs = torch.nn.functional.softmax(outputs, dim=-1) 
            
            if pu_probs is None: 
                pu_probs = probs.detach().cpu().numpy().squeeze()
                pu_targets = targets.numpy().squeeze()
                
            else:
                pu_probs = np.concatenate( (pu_probs, \
                    probs.detach().cpu().numpy().squeeze()))
                pu_targets = np.concatenate( (pu_targets, \
                    targets.numpy().squeeze()))
                
    
    return pu_probs, pu_targets

def DKW_bound(x,y,t,m,n,delta=0.1, gamma= 0.01):
#     from scipy.stats import norm
    
#     sigma = 1.0/x - 1.0/m + 1.0/y - 1.0/n 
    temp = np.sqrt(np.log(1/delta)/2/n) + np.sqrt(np.log(1/delta)/2/m)
    bound = temp*(1+gamma)/(y/n)

    estimate = t

    return estimate, t - bound, t + bound


def bininv(m,e,c): 
    from scipy.stats import binom
    plo = 0
    phi = 1
    p = .5

    max_iter = 20 
    tol = c*0.001   

    iter = 0;

    while iter <= max_iter:
        iter = iter + 1;
        bintail = binom.cdf(e,m,p)
        if abs(bintail - c) <= tol: 
            return p

        if bintail < c: 
            phi = p
        else: 
            plo = p
        p = (phi + plo)/2

def scott_estimator(pdata_probs, udata_probs):
    p_indices = np.argsort(pdata_probs[:,0])
    sorted_p_probs = pdata_probs[:,0][p_indices]
    u_indices = np.argsort(udata_probs[:,0])
    sorted_u_probs = udata_probs[:,0][u_indices]

    sorted_u_probs = sorted_u_probs[::-1]
    sorted_p_probs = sorted_p_probs[::-1]
    num = len(sorted_u_probs)
    ratios = []
    delta=0.1
    n = len(sorted_u_probs)
    m = len(sorted_p_probs)
    alphas = []
    for index in range(n):
        start_interval =  sorted_u_probs[index]   

        i = index

        j=0
        while (j<m and sorted_p_probs[j] >= start_interval):
            j+= 1
        q_p = j/m
        q_u = i/n
        if q_p > 0:
            t = q_u/q_p + (1/q_p)*(np.sqrt(np.log(4/delta)/2/n) + np.sqrt(np.log(4/delta)/2/m))
            ratios.append(t)
            alphas.append(q_u/q_p)

    if len(ratios)!= 0: 
        return alphas[ratios.index(min(ratios))]
    else:   
        print("error")
        print(sorted_u_probs)
        print(sorted_p_probs)

def top_bin_estimator_count(pdata_probs, udata_probs):
    p_indices = np.argsort(pdata_probs[:,0])
    sorted_p_probs = pdata_probs[:,0][p_indices]
    u_indices = np.argsort(udata_probs[:,0])
    sorted_u_probs = udata_probs[:,0][u_indices]

    sorted_u_probs = sorted_u_probs[::-1]
    sorted_p_probs = sorted_p_probs[::-1]
    num = len(sorted_u_probs)

    plot_arr = []
    plot_ratio = []
    j = 0
    num_u_samples = 0

    upper_cfb = []
    lower_cfb = []            

    i = 0
    while (i < num):
        start_interval =  sorted_u_probs[i]   
        k = i 
        if (i<num-1 and start_interval> sorted_u_probs[i+1]): 
            pass
        else: 
            i += 1
            continue

        while ( j<len(sorted_p_probs) and sorted_p_probs[j] >= start_interval):
            j+= 1

        if j>1 and i > 1:
            t = (i)*1.0*len(sorted_p_probs)/j/len(sorted_u_probs)
            plot_ratio.append(t)
            estimate, lower , upper = DKW_bound(i, j, t, len(sorted_u_probs), len(sorted_p_probs))

            plot_arr.append(estimate)
            upper_cfb.append(upper)
            lower_cfb.append(lower)

        i+=1
    if (len(upper_cfb) != 0): 
        mpe_estimate = np.min(upper_cfb)
        idx = np.argmin(upper_cfb)

        if (plot_arr[idx] != plot_ratio[idx]): 
            print("fallback...")

        return plot_arr[idx]
    else: 
        print("error!")
        print("udata_probs:", udata_probs)
        print("pdata_probs:", pdata_probs)


def EM_estimate(dic_prob):
    #initialize
    g0 = dic_prob[0]["g"]
    p0 = dic_prob[0]["p"]
    g1 = dic_prob[1]["g"]
    p1 = dic_prob[1]["p"]
    g2 = dic_prob[2]["g"]
    p2 = dic_prob[2]["p"]
    g3 = dic_prob[3]["g"]
    p3 = dic_prob[3]["p"]

    P0_ = g0.mean()
    P1_ = g1.mean()
    P2_ = g2.mean()
    P3_ = g3.mean()


    delta =1

    while delta > 1e-3:
        P0_ini = P0_
        P1_ini = P1_
        P2_ini = P2_
        P3_ini = P3_
        nume0 = (P0_*p0)/g0.mean()
        nume1 = (P1_*p1)/g1.mean()
        nume2 = (P2_*p2)/g2.mean()
        nume3 = (P3_*p3)/g3.mean()
        denom = nume0+nume1+nume2+nume3
        P0_ = (nume0/denom).mean()
        P1_ = (nume1/denom).mean()
        P2_ = (nume2/denom).mean()
        P3_ = (nume3/denom).mean()

        delta = abs(P0_-P0_ini) + abs(P1_-P1_ini) + abs(P2_-P2_ini) + abs(P3_-P3_ini)
    return  {1:P1_,2:P2_,3:P3_}


def estimator_CM_EN(pdata_probs, pudata_probs):
    return np.sum(pudata_probs)*len(pdata_probs)/len(pudata_probs)/np.sum(pdata_probs)

def estimator_prob_EN(pdata_probs):
    return np.sum(pdata_probs, axis=0)/len(pdata_probs)

def estimator_max_EN(pdata_probs, pudata_probs):
    return np.max(np.concatenate((pdata_probs, pudata_probs) ))


def dedpul(pdata_probs, udata_probs,udata_targets):

    alpha = None
    poster = np.zeros_like(udata_probs[:,0])
    preds = np.concatenate((1.0- pdata_probs, udata_probs[:,1]),axis=0)
    targets = np.concatenate((np.zeros_like(pdata_probs), np.ones_like(udata_probs[:,1])), axis=0 )
    
    try:    
        diff = estimate_diff(preds, targets) 
        alpha, poster = estimate_poster_em(diff=diff, mode='dedpul', alpha=None)

        if alpha<=1e-4: 
            alpha, poster =  estimate_poster_dedpul(diff=diff, alpha=alpha)
    
    except: 
        alpha = 0.0
        poster = preds

    return 1 - alpha, poster

def plot_our_estimator(our_mpe_estimate, index, ratio_estimate, lower_bound, \
        upper_bound, plot_arr, ideal_plot_arr, alpha): 
    num = len(upper_bound)
    plt.plot(range(num), ideal_plot_arr)
    plt.plot(range(num), plot_arr)
    plt.fill_between(range(num), lower_bound, upper_bound, alpha=0.3)
    plt.plot(range(num), [alpha]*(num), '--')
    plt.plot(index, ratio_estimate, 'x', markersize=10)
    plt.ylim((0.0,1.0))
    plt.savefig("our-estimator.png",transparent=True,bbox_inches='tight')
    plt.clf()


def dedpul_acc(udata_probs,udata_targets): 
    predictions = (udata_probs >=0.5)

    return np.mean(udata_targets == predictions) 

def KM_estimate(p_data, u_data, data_type):
    if not data_type.startswith("UCI"):
        pca = PCA(n_components=50, svd_solver='full')
        new_X = pca.fit_transform(np.concatenate((u_data, p_data), axis=0))

        X_mixture = new_X[0:len(u_data)]
        X_component = new_X[len(u_data):]
    else: 
        X_mixture = u_data 
        X_component = p_data
    

    n_shuffle = np.random.permutation(len(X_mixture))
    p_shuffle = np.random.permutation(len(X_component))

    X_component = X_component[p_shuffle][:2000]
    X_mixture = X_mixture[n_shuffle][:2000]

    return wrapper(X_mixture, X_component)

def min_max_scale(data):
    data_norm = data - np.min(data, axis=0)
    data_norm = data_norm / np.max(data_norm, axis=0)
    return data_norm

def tice_c_to_alpha(c, gamma):
    return 1 - (1 - gamma) * (1 - c) / gamma / c

def TiCE_estimate(p_data, u_data, data_type): 
    if not data_type.startswith("UCI"):
        pca = PCA(n_components=100, svd_solver='full')
        new_X = pca.fit_transform(np.concatenate((u_data, p_data), axis=0))

        X_mixture = new_X[0:len(u_data)]
        X_component = new_X[len(u_data):]
    else: 
        X_mixture = u_data 
        X_component = p_data
    

    data = np.concatenate((X_component,X_mixture),axis=0)
    data = min_max_scale(data)
    labels = np.concatenate((np.ones(len(X_component)), np.zeros(len(X_mixture))))
    folds =  np.random.randint(5, size=len(data))

    c = tice(data, labels, 10, folds=folds, delta=0.2)[0]
    
    return tice_c_to_alpha(c, 0.5)
