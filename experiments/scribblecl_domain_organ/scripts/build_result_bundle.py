#!/usr/bin/env python3
"""Build the registered CSV and figure bundle from complete immutable runs."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import shutil

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def read_csv(path: Path) -> list[dict]:
    with path.open(newline="") as stream:
        return list(csv.DictReader(stream))


def write_csv(path: Path, rows: list[dict]) -> None:
    fields = sorted({key for row in rows for key in row})
    with path.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def matrix(path: Path) -> tuple[list[str], np.ndarray]:
    with path.open(newline="") as stream:
        rows = list(csv.reader(stream))
    names = rows[0][1:]
    values = np.asarray([[float(x) if x else np.nan for x in row[1:]] for row in rows[1:]])
    return names, values


def plot_matrix(path: Path, names: list[str], values: np.ndarray, title: str) -> None:
    fig, ax = plt.subplots(figsize=(6.4, 5.4))
    image = ax.imshow(values, vmin=0, vmax=1, cmap="viridis")
    for row in range(len(values)):
        for col in range(len(values)):
            if np.isfinite(values[row, col]):
                ax.text(col, row, f"{values[row, col]:.3f}", ha="center", va="center", color="white" if values[row, col] < .65 else "black", fontsize=8)
    ax.set(xticks=range(len(names)), yticks=range(len(names)), xticklabels=names, yticklabels=[str(i + 1) for i in range(len(names))], xlabel="Evaluation task/domain", ylabel="After stage", title=title)
    fig.colorbar(image, ax=ax, label="Benchmark mean Dice")
    fig.tight_layout(); fig.savefig(path, dpi=180); plt.close(fig)


def plot_curves(path: Path, names: list[str], values: np.ndarray, title: str) -> None:
    fig, ax = plt.subplots(figsize=(7.0, 4.4))
    stages = np.arange(1, len(values) + 1)
    for index, name in enumerate(names):
        ax.plot(stages, values[:, index], marker="o", label=name)
    ax.set(xlabel="Stage", ylabel="Benchmark mean Dice", ylim=(0, 1), xticks=stages, title=title)
    ax.legend(ncol=2, fontsize=8); ax.grid(alpha=.25); fig.tight_layout(); fig.savefig(path, dpi=180); plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scenario", choices=["domain", "organ"], required=True)
    parser.add_argument("--runs-root", required=True)
    parser.add_argument("--annotation-summary", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    out = Path(args.output); out.mkdir(parents=True, exist_ok=True)
    matrices = out / "stage_domain_matrices"; matrices.mkdir(exist_ok=True)
    figures = out / "figures"; figures.mkdir(exist_ok=True)
    annotations = json.loads(Path(args.annotation_summary).read_text())
    annotated = sum(x["foreground_pixels"] + x["background_pixels"] for x in annotations)
    total = sum(x["slices"] * 256 * 256 for x in annotations)
    annotation_ratio = annotated / total
    annotation_rows = [{key: value for key, value in record.items() if key != "npz"} for record in annotations]
    write_csv(out / "annotation_summary.csv", annotation_rows)

    runs = []
    for path in sorted((Path(args.runs_root) / args.scenario).glob("*/run_manifest.json")):
        manifest = json.loads(path.read_text())
        if manifest.get("status") == "complete":
            runs.append((path.parent, manifest))
    if not runs:
        raise RuntimeError("no complete runs")
    index_rows=[]; summary_rows=[]; per_rows=[]; fisher_rows=[]; resource_rows=[]
    scatter=[]
    for run, manifest in runs:
        summary=json.loads((run/"summary.json").read_text()); names, values=matrix(run/"performance_matrix.csv")
        shutil.copyfile(run/"performance_matrix.csv",matrices/f"{manifest['run_id']}.csv")
        index_rows.append({key:manifest.get(key) for key in ("run_id","scenario","method","seed","backbone","head","status","source_tree_sha256","order_sha256","split_checksum_sha256","parent_checkpoint_sha256")})
        row={"run_id":manifest["run_id"],"method":manifest["method"],"supervision":manifest["method"].split("_")[0],"CL":manifest["method"].split("_")[-1].upper(),"history_data":False,"annotation_ratio":annotation_ratio,**summary}; summary_rows.append(row)
        scatter.append((manifest["method"],summary["A-Dice"],summary["BWTR"],summary.get("E-FWT")))
        for stage in range(len(values)):
            for index,name in enumerate(names):
                per_rows.append({"run_id":manifest["run_id"],"stage":stage+1,"evaluated":name,"score":"" if not np.isfinite(values[stage,index]) else values[stage,index],"seen":index<=stage})
        for record in json.loads((run/"fisher_summary.json").read_text()): fisher_rows.append({"run_id":manifest["run_id"],**record})
        for record in read_csv(run/"stage_metrics.csv"): resource_rows.append({"run_id":manifest["run_id"],**record})
        plot_matrix(figures/f"{manifest['run_id']}_matrix.png",names,values,f"{args.scenario.title()} {manifest['method']} seed {manifest['seed']}")
        plot_curves(figures/f"{manifest['run_id']}_curves.png",names,values,f"Per-{args.scenario} trajectory")
        if args.scenario == "organ":
            params=[float(x["model_parameters"]) for x in read_csv(run/"stage_metrics.csv")]
            fig,ax=plt.subplots(figsize=(5.8,4.0)); ax.plot(range(1,len(params)+1),params,marker="o"); ax.set(xlabel="Stage / active heads",ylabel="Parameters",xticks=range(1,len(params)+1),title="Task-head parameter growth"); ax.grid(alpha=.25); fig.tight_layout(); fig.savefig(figures/f"{manifest['run_id']}_head_growth.png",dpi=180); plt.close(fig)
    write_csv(out/"run_index.csv",index_rows); write_csv(out/"core_summary.csv",summary_rows); write_csv(out/("per_domain.csv" if args.scenario=="domain" else "per_task.csv"),per_rows); write_csv(out/"fisher_summary.csv",fisher_rows); write_csv(out/"resource_summary.csv",resource_rows)
    fig,ax=plt.subplots(figsize=(5.8,4.4))
    for name,a_dice,bwtr,_ in scatter: ax.scatter(a_dice,bwtr,label=name,s=55)
    ax.set(xlabel="A-Dice",ylabel="BWTR",title="Stability-plasticity summary"); ax.grid(alpha=.25); ax.legend(); fig.tight_layout(); fig.savefig(figures/"adice_bwtr.png",dpi=180); plt.close(fig)
    if args.scenario=="domain":
        fig,ax=plt.subplots(figsize=(5.8,4.0)); ax.bar([x[0] for x in scatter],[x[3] for x in scatter]); ax.set(ylabel="E-FWT",title="Domain forward transfer"); ax.tick_params(axis="x",rotation=20); fig.tight_layout(); fig.savefig(figures/"efwt.png",dpi=180); plt.close(fig)
    else:
        fig,ax=plt.subplots(figsize=(5.8,4.4))
        for run,manifest in runs:
            _,values=matrix(run/"performance_matrix.csv"); current=np.diag(values); old=np.asarray([np.nan if stage==0 else np.nanmean(values[stage,:stage]) for stage in range(len(values))]); ax.plot(current,old,marker="o",label=manifest["method"])
        ax.set(xlabel="Current-task Dice",ylabel="Mean old-task Dice",title="Current-vs-old trade-off"); ax.grid(alpha=.25); ax.legend(); fig.tight_layout(); fig.savefig(figures/"current_vs_old.png",dpi=180); plt.close(fig)


if __name__ == "__main__":
    main()
