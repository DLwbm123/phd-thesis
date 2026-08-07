# Static ZS v2 run status

`DECISION: NO-GO-ZS`

This is an interim execution record, not the final `ZS_STATIC_TASK1_GATE_V2.md` decision.

- Exact source commit: `960017d18ff9a3d36bec6422fa8cc25715cd11bd`
- Remote code snapshot: `/remote-home/wangbomin/ScribbleCL/experiments/scribblecl_zs_v2_commit960017d`
- Run root: `/remote-home/wangbomin/ScribbleCL/static_task1_zs_v2_commit960017d`
- Queue PID file: `/remote-home/wangbomin/ScribbleCL/static_task1_zs_v2_commit960017d/queue.pid`
- Queue log: `/remote-home/wangbomin/ScribbleCL/static_task1_zs_v2_commit960017d/queue.log`
- Machine-readable queue record: `/remote-home/wangbomin/ScribbleCL/static_task1_zs_v2_commit960017d/queue_run.json`
- Monitor: `ssh root@10.12.208.231 -p 20048 'pid=$(cat /remote-home/wangbomin/ScribbleCL/static_task1_zs_v2_commit960017d/queue.pid); ps -p "$pid" -o pid,etime,stat,cmd; tail -40 /remote-home/wangbomin/ScribbleCL/static_task1_zs_v2_commit960017d/queue.log'`

Completed at this snapshot:

- exact-commit pytest: 60 passed, one upstream NumPy compatibility warning from `gco`;
- repeated two-batch A0, A, C1, C2, C3, D and E smoke runs;
- C1/C2/C3/D/E smoke reports: all `PASS`, with bit-exact repeated losses and parameters;
- A 20-epoch diagnostic: `PASS`, best foreground patient mean `0.4251763709` at epoch 14.

Running at this snapshot:

- C1 20-epoch validation-only diagnostic.

Not yet run:

- C2/C3/D/E 20-epoch diagnostics;
- full A, C1, C2, C3, D and E 150-epoch runs;
- final pairwise collapse gates and `ZS_STATIC_TASK1_GATE_V2.md`.

The queue is sequential and exits immediately on a smoke, diagnostic, or full-run gate failure. It contains no Task-1 seed 43, ScribbleMiB-v2, Task 2/3, core seed 42, or core seed 43/44 command.

## Missing required external input

`ScribbleCL_ZS_CODE_REVIEW_REPORT.md` was not present in Downloads, the thesis checkout, the local workspace, the remote review bundle, `/root`, or `/remote-home/wangbomin` at audit time. The task file's explicit defect list, the complete review bundle, the original source, and the paper were used; no contents were invented for the missing report.
