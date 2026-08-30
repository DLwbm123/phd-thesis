#!/usr/bin/env python3
"""Translate original PDF labels using fixed font sizes for matching roles.

Requires installed PyMuPDF and pypdf. Optional arguments select PDF filenames.
The immutable original supplies geometry, images, formulas and numbers. Long
Chinese phrases use whitespace or intentional breaks, never font shrinking.
"""
from collections import Counter
import io
from pathlib import Path
import re
import subprocess
import sys

import fitz
from pypdf import PdfReader, PdfWriter
from pypdf.generic import ContentStream, NameObject

fitz.TOOLS.set_small_glyph_heights(True)
ROOT = Path(__file__).resolve().parents[1]
SOURCE_REVISION = 'b34b0e4'
FONT = ROOT / 'FontStyle/SimHei.ttf'
METRICS = fitz.Font(fontfile=str(FONT))


def numbers(text):
    return Counter(re.findall(r'-?\d*\.\d+|-?\d+', text.replace('−', '-')))


def without_text_objects(data):
    """Remove text without rewriting the bubble figure's transparency groups."""
    writer = PdfWriter(clone_from=PdfReader(io.BytesIO(data)))
    seen = set()

    def strip(stream):
        parsed = ContentStream(stream, writer)
        kept, inside = [], False
        for operands, operator in parsed.operations:
            if operator == b'BT':
                inside = True
            elif operator == b'ET':
                inside = False
            elif not inside:
                kept.append((operands, operator))
        parsed.operations = kept
        return parsed

    def forms(resources):
        for ref in resources.get('/XObject', {}).values():
            obj = ref.get_object()
            if obj.get('/Subtype') != '/Form' or id(obj) in seen:
                continue
            seen.add(id(obj))
            if any(op == b'BT' for _, op in ContentStream(obj, writer).operations):
                obj.set_data(strip(obj).get_data())
            forms(obj.get('/Resources', {}))

    for page in writer.pages:
        page[NameObject('/Contents')] = writer._add_object(strip(page.get_contents()))
        forms(page.get('/Resources', {}))
    result = io.BytesIO()
    writer.write(result)
    return result.getvalue()


def put_label(page, rect, text, size, color, vertical=False, align='center'):
    rect = fitz.Rect(rect)
    lines = text.split('\n')
    assert all(ch.isspace() or METRICS.has_glyph(ord(ch)) for ch in text), text
    assert not vertical or len(lines) == 1
    extent = rect.height if vertical else rect.width
    for line in lines:
        assert METRICS.text_length(line, fontsize=size) <= extent + .05, (
            text, size, tuple(rect), 'too wide: edit phrase/box, not font size')
    leading = size * 1.2
    height = (METRICS.ascender - METRICS.descender) * size + leading * (len(lines)-1)
    assert height <= (rect.width if vertical else rect.height) + .05, (
        text, size, tuple(rect), 'label too tall')
    offset = (METRICS.ascender + METRICS.descender) * size / 2
    for i, line in enumerate(lines):
        width = METRICS.text_length(line, fontsize=size)
        if vertical:
            point = ((rect.x0+rect.x1)/2+offset, (rect.y0+rect.y1+width)/2)
        else:
            x = rect.x0 if align == 'left' else (rect.x0+rect.x1-width)/2
            point = (x, (rect.y0+rect.y1)/2+offset+(i-(len(lines)-1)/2)*leading)
        page.insert_text(point, line, fontname='FigureChinese',
                         fontsize=size, color=color, rotate=90 if vertical else 0)


def translate(destination, original):
    source = fitz.open(stream=original, filetype='pdf')
    source_page = source[0]
    lines = [line for block in source_page.get_text('dict')['blocks']
             for line in block.get('lines', [])]
    for line in lines:
        line['text'] = ''.join(span['text'] for span in line['spans'])
    labels, erase = [], []
    name = destination.name

    def add(indices, text, size, rect=None, color=None, vertical=None, align='center'):
        indices = [indices] if isinstance(indices, int) else indices
        selected = [lines[i] for i in indices]
        bounds = fitz.Rect(selected[0]['bbox'])
        for line in selected[1:]:
            bounds |= fitz.Rect(line['bbox'])
        erase.extend(fitz.Rect(line['bbox']) for line in selected)
        if vertical is None:
            vertical = selected[0]['dir'][1] < -.9
        if rect is None:
            cx, cy = (bounds.x0+bounds.x1)/2, (bounds.y0+bounds.y1)/2
            w = max(bounds.width, size*1.15 if vertical else max(METRICS.text_length(s, fontsize=size) for s in text.split('\n')))
            h = max(bounds.height, METRICS.text_length(text, fontsize=size) if vertical else size*(1.15+1.2*(len(text.split('\n'))-1)))
            rect = (cx-w/2, cy-h/2, cx+w/2, cy+h/2)
        if color is None:
            color = fitz.sRGB_to_pdf(selected[0]['spans'][0]['color'])
        labels.append((rect, text, size, color, vertical, align))

    if name == 'fedsubmerge_overview.pdf':
        replacements = [
            (36, '联邦任务流与 PGS 构建', 16, (10,0,335,23)),
            (37, '服务器端子空间融合', 16, (429,0,668,23)),
            (38, '本地投影训练与客户端 PGS 更新', 16, (776,0,1095,23)),
            (6, '主梯度子空间（PGS）构建', 16, (9,249,411,276)),
            (48, 'FedSubMerge：统一融合', 15, (429,26,746,47)),
            (7, 'FedSubMerge-AD：逐层自适应融合', 15, (429,214,775,236)),
            (45, '服务器', 14, (204,149,260,176)),
            (46, '模型聚合', 14, (74,202,193,227)),
            (47, '子空间融合', 14, (250,202,368,227)),
            (11, '最终模型', 14, (17,280,92,302)),
            (64, '梯度矩阵', 14, (160,280,263,303)),
            (9, '加权基拼接', 14, (484,122,667,144)),
            (10, '子空间距离', 14, (513,235,643,259)),
            (50, '选择并融合', 14, (652,235,772,259)),
            (51, '服务器返回的 PGS', 14, (801,34,1020,57)),
            (52, '任务内：本地投影训练', 14, (801,106,1083,129)),
            (8, '任务末：客户端 PGS 更新', 14, (801,251,1083,274)),
            (55, '正交投影', 12, (884,137,998,156)),
            (56, '优化器更新', 12, (931,191,1026,212)),
            (16, 'PGS 更新', 12, (807,280,884,299)),
            (5, '每任务上传一次', 12, (961,276,1078,297)),
            (3, '第1层 PGS', 12, (431,270,494,288)),
            (4, '第2层 PGS', 12, (431,296,494,314)),
            (35, '第L层 PGS', 12, (431,351,494,369)),
            (33, '低', 10, (525,354,545,369)),
            (34, '高', 10, (609,354,631,369)),
        ]
        for index, text, size, rect in replacements:
            add(index, text, size, rect, align='left' if index in {36,37,38,6,48,7,9,51,52,8,55,16,5} else 'center')
        for index in (40,42,44):
            add(index, '历史影像', 10)
        add([53,54], '当前\n小批量', 11, (808,185,866,215))
        # Keep mathematical C_i and n_s glyphs in the original mixed text lines.
        for index in (39,41,43,49,12):
            for span in lines[index]['spans']:
                word = span['text'].strip()
                replacement = {'Hospital':'医院','Target':'目标','Sample':'采样','Examples':'个样本'}.get(word)
                if replacement:
                    rect = fitz.Rect(span['bbox']); erase.append(rect)
                    cy = (rect.y0+rect.y1)/2
                    labels.append(((rect.x0,cy-9,rect.x1,cy+9), replacement,12,
                                   fitz.sRGB_to_pdf(span['color']),False,'center'))
        erase.append(fitz.Rect(lines[57]['bbox']))
        labels.extend([((297,346,341,366),'基',12,(.18,.43,.40),False,'center'),
                       ((346,346,415,366),'奇异值',12,(.18,.43,.40),False,'center')])

    elif name == 'benchmark_overview_new.pdf':
        for index, text in {0:'临床驱动的持续学习场景',4:'统一基准协议',23:'超越遗忘的综合评价'}.items():
            add(index, text, 28)
        for index, text in {1:'（a）域增量',2:'（b）类别增量',3:'（c）器官增量'}.items():
            add(index, text,28,(18,lines[index]['bbox'][1]-2,360,lines[index]['bbox'][3]+4),align='left')
        words = {'Sequential learning':'顺序学习','Regularization':'正则化','Replay':'经验回放',
                 'Class-CL specific':'类别增量专用方法','Conventional metrics':'常规评价指标',
                 'general performance':'总体性能','stability (forgetting)':'稳定性（遗忘）',
                 'whole-class Dice (Class-CL)':'全类别 Dice','parameter efficiency':'参数效率',
                 'replay burden':'回放负担','plasticity':'可塑性','generalizability':'泛化能力',
                 'Beyond forgetting':'遗忘之外的能力','Key Findings':'主要发现',
                 'Same label space, shifted image domains':'标签空间不变，图像域发生变化',
                 'Same image distribution, evolving anatomical labels':'图像分布不变，解剖标签逐步增加',
                 'Different organs, modalities, and label spaces':'器官、模态与标签空间发生变化',
                 'Left atrium MRI':'左心房 MRI','Prostate MRI':'前列腺 MRI','Liver CT':'肝脏 CT',
                 'Brain FLAIR MRI':'脑部 FLAIR MRI'}
        for i, line in enumerate(lines):
            text = line['text'].strip()
            if text in words:
                add(i, words[text],24)
            elif re.fullmatch(r'Task [1-6T]',text):
                add(i,text.replace('Task ','任务 '),24)
            elif re.fullmatch(r'Center [A-F]',text):
                add(i,text.replace('Center ','中心 '),24)
        add([74,75],'参数隔离',24)
        add([21,22],'统一任务定义、数据划分\n与评价设置',24,(790,868,1140,932))
        add(67,'· 没有一种策略满足所有要求',24,(1263,753,1729,791),align='left')
        add(68,'· 回放兼顾稳定性与可塑性',24,(1263,788,1729,826),align='left')
        add([69,70],'· 参数隔离减轻遗忘，\n  但增加模型规模',24,(1263,822,1729,886),align='left')
        add(71,'· 前向泛化能力仍有限',24,(1263,887,1729,925),align='left')

    elif name == 'plots_for_benchmark.pdf':
        groups = [([0,1],'持续学习'),([2,3,4],'持续\n测试时适应'),([5,6],'迁移学习'),
                  ([7,8,9],'无监督\n领域适应'),([10,11,12],'无监督\n持续学习'),
                  ([13,14],'表征学习'),([15,16],'生成式模型'),([17,18],'多任务学习'),
                  ([19,20,21],'少样本\n持续学习'),([22,23],'少样本学习'),([24,25],'元学习'),
                  ([26,27,28],'持续\n强化学习'),([29,30],'强化学习'),([31,32,33],'联邦\n持续学习'),
                  ([34,35],'联邦学习'),([36,37,38],'持续\n新类别发现'),([39,40,41],'开放世界\n学习')]
        for ids, phrase in groups:
            add(ids,phrase,16 if ids[0]==0 else 12,color=(1,1,1))

    else:
        words = {'Method':'方法','Task Order':'任务顺序','Buffer Size':'回放容量',
                 'SAM with LoRA Fine-Tuning':'SAM（LoRA 微调）','Domain-CL':'域增量',
                 'Organ-CL':'器官增量','Class-CL':'类别增量','Accuracy (%)':'准确率（%）',
                 'Trained through task t':'已完成任务 t','Evaluated task τ':'评价任务 τ',
                 'self-only':'仅自身','default':'默认','uniform':'统一融合',
                 'Neighborhood size n':'相关客户端数 n','(a) Neighborhood size n':'（a）相关客户端数 n',
                 'Energy threshold γ':'能量阈值 γ','(b) Energy threshold γ':'（b）能量阈值 γ',
                 'ACC (%)':'准确率（%）','BWT (%)':'后向迁移（%）','Fixed':'固定图像',
                 'Moving':'移动图像','Brain MR-MR':'脑部 MR-MR','Abdomen CT-CT':'腹部 CT-CT',
                 'Lung CT-CT':'肺部 CT-CT','Abdomen MR-CT':'腹部 MR-CT',
                 'Continual Medical Image Registration':'持续医学图像配准',
                 'Universal Medical Image Registration':'多任务配准推理','Deployment Phase':'推理阶段',
                 'Training Phase':'训练阶段','Inputs from All Tasks':'各任务图像输入',
                 'Sequential':'顺序训练','Multitask':'多任务训练','Independent':'独立训练',
                 'In-domain Generalization':'域内前向泛化','Out-of-domain Generalization':'域外前向泛化'}
        for i, line in enumerate(lines):
            text = line['text'].strip(); phrase=words.get(text)
            if re.fullmatch(r'Task [1-6]',text):
                phrase=text.replace('Task ','任务 ')
            elif re.fullmatch(r'Order[A-J]',text):
                phrase=text.replace('Order','顺序 ')
            if phrase is None:
                continue
            size=line['spans'][0]['size']; rect=None
            if name == 'samcl_qualitative.pdf':
                size=17.26
                if text in {'Fixed','Moving'}:
                    cy=sum(line['bbox'][1::2])/2; rect=(3,cy-12,77,cy+12)
            elif name == 'samcl_framework.pdf':
                size=14 if text.endswith('Phase') else 11 if 'Registration' in text else 13
            elif name == 'scribble_annotation_fig.pdf':
                size=16
            elif name == 'fedsubmerge_accuracy_matrix.pdf':
                size=10
            elif name == 'fedsubmerge_hyperparameter.pdf':
                size=16 if text in {'self-only','default','uniform'} else 18
            elif name == 'plot_sam_new.pdf':
                size=12
            add(i,phrase,size,rect)

    if name == 'plots_for_benchmark.pdf':
        doc=fitz.open(stream=without_text_objects(original),filetype='pdf'); page=doc[0]
    else:
        doc=fitz.open(stream=original,filetype='pdf'); page=doc[0]
        for rect in erase:
            page.add_redact_annot(rect,fill=None)
        if erase:
            page.apply_redactions(images=0,graphics=0,text=0)
    raster_labels=[]
    if name == 'plot_memory_nnn.pdf':
        raster_labels=[((62,177,114,189),'回放 50',9),((62,190,114,202),'回放 100',9),
                       ((62,203,114,215),'回放 200',9)]
    elif name == 'plot_sam_new.pdf':
        raster_labels=[((470,27,508,39),'无 SAM',9),((470,40,508,52),'有 SAM',9),
                       ((54,235,116,250),'CTCT→CTCT',10),((151,235,216,250),'MRCT→MRCT',10),
                       ((249,235,317,250),'CTCT→MRCT',10),((341,235,404,250),'CTCT→NLST',10),
                       ((438,235,509,250),'OASIS→NLST',10)]
    # Subset only the new text layer. Re-subsetting source fonts can damage
    # original ActualText/formula resources in the FedSubMerge PDF.
    overlay = fitz.open()
    overlay_page = overlay.new_page(width=page.rect.width,height=page.rect.height)
    overlay_page.insert_font(fontname='FigureChinese',fontfile=str(FONT))
    for args in labels:
        put_label(overlay_page,*args)
    assert numbers(page.get_text()) + numbers(overlay_page.get_text()) == numbers(source_page.get_text()),name
    for rect,phrase,size in raster_labels:
        overlay_page.draw_rect(rect,color=None,fill=(1,1,1),overlay=True)
        put_label(overlay_page,rect,phrase,size,(0,0,0))
    overlay.subset_fonts()
    page.show_pdf_page(page.rect,overlay,0)
    doc.save(destination,garbage=4,deflate=True)
    print(f'{destination.relative_to(ROOT)}: {len(labels)} fixed-size labels; numeric text unchanged')


def main():
    selected=set(sys.argv[1:])
    for destination in sorted((ROOT/'figures').rglob('*.pdf')):
        if selected and destination.name not in selected:
            continue
        path=destination.relative_to(ROOT).as_posix()
        path=path.replace('/ch04/','/OLD04/').replace('/ch05/','/ch04/').replace('/OLD04/','/ch05/')
        original=subprocess.check_output(['git','show',f'{SOURCE_REVISION}:{path}'],cwd=ROOT)
        translate(destination,original)


if __name__ == '__main__':
    main()
