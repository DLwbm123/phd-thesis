#!/usr/bin/env python3
"""Read-only audit of H5 split, patient and label contracts."""
from __future__ import annotations
import argparse
from hashlib import sha256
import json
from pathlib import Path
import sys
import h5py
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from medcl.data import dataset_path, tasks_for
from medcl.data.protocols import EXPECTED_SHA256, order_sha256
from medcl.utils import file_sha256


def main():
    parser=argparse.ArgumentParser(); parser.add_argument("--scenario",choices=("class","domain","organ"),required=True); parser.add_argument("--data-root",type=Path,required=True); parser.add_argument("--output",type=Path,required=True); args=parser.parse_args()
    tasks=tasks_for(args.scenario); rows=[]
    for task in tasks:
        path=dataset_path(args.data_root,task); digest=file_sha256(path); expected=EXPECTED_SHA256[f"{task.folder}/{task.file}"]; split={}
        with h5py.File(path,"r") as handle:
            for name in ("train","val","test"):
                images=handle[f"{name}_images"]; labels=handle[f"{name}_labels"]; patient=np.asarray(handle[f"patient_info_{name}"][:],dtype=int)
                split[name]={"images_shape":list(images.shape),"labels_shape":list(labels.shape),"patients":len(patient),"patient_ends":patient.tolist(),"labels":sorted(np.unique(labels[:]).astype(int).tolist()),"finite":bool(np.isfinite(images[:]).all()),"mean":float(np.mean(images[:])),"std":float(np.std(images[:]))}
        rows.append({"task":task.code,"file":f"{task.folder}/{task.file}","sha256":digest,"expected_sha256":expected,"sha_match":digest==expected,"split":split})
    if args.scenario=="class":
        path=args.data_root/"MMWHS"/"whole_heart_test.h5"; digest=file_sha256(path); expected=EXPECTED_SHA256["MMWHS/whole_heart_test.h5"]
        with h5py.File(path,"r") as handle:
            images=handle["test_images"]; labels=handle["test_labels"]; patient=np.asarray(handle["patient_info_test"][:],dtype=int); split={"test":{"images_shape":list(images.shape),"labels_shape":list(labels.shape),"patients":len(patient),"patient_ends":patient.tolist(),"labels":sorted(np.unique(labels[:]).astype(int).tolist()),"finite":bool(np.isfinite(images[:]).all()),"mean":float(np.mean(images[:])),"std":float(np.std(images[:]))}}
        rows.append({"task":"WCD","file":"MMWHS/whole_heart_test.h5","sha256":digest,"expected_sha256":expected,"sha_match":digest==expected,"split":split})
    result={"status":"PASS" if all(x["sha_match"] for x in rows) else "FAIL","scenario":args.scenario,"order_sha256":order_sha256(tasks),"tasks":rows}; args.output.parent.mkdir(parents=True,exist_ok=True); args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n"); print(json.dumps(result,indent=2,sort_keys=True))


if __name__=="__main__": main()
