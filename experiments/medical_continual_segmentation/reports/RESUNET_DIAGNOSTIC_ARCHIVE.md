# ResUNet diagnostic archive

All runs in this file are diagnostic only and excluded from final tables. No checkpoint was removed or overwritten, and no process received `kill -9`.

| Scenario | Method | PID | Outcome | Last complete checkpoint | SHA-256 |
|---|---|---:|---|---|---|
| Domain | PCE-FT | - | completed naturally | F epoch 149 | `7875c3054857f19e999602e281bc8ad65101c7b956db893cbe67b61822bd2400` |
| Domain | PCE-EWC | 80127 | stopped after checkpoint decision | E epoch 149 | `8866b274b0ded29854c7da2219525cabcc1ad3689599012352605b0a155d2153` |
| Organ | PCE-FT | 71396 | completed naturally | T4 epoch 149 | `8387642b88b100ebf17a774522789c3a8694de00d156221883f83dbbc4e60685` |
| Organ | PCE-EWC | 80128 | stopped after checkpoint decision | T2 epoch 149 | `31b90c7604906f3f1df4e85ee9ab9eb186accc4d793be7c8f9d53250b78ed362` |

PIDs 80127 and 80128 were briefly stopped for checkpoint verification, then terminated using ordinary SIGTERM and resumed only to let the signal take effect. PID 71396 was already in its final stage and was allowed to finish naturally. A separate paused independent diagnostic PID 81051 had no complete checkpoint under the legacy runner and was terminated using ordinary SIGTERM plus SIGCONT.

The Domain EWC stage-5 model and EWC state SHA-256 are respectively `8866b...2153` and `930fee...111a`. The Organ EWC stage-2 model and EWC state are `31b90c...362` and `d0f9a4...70da`. Exact continuation commands cannot be truthfully supplied because the legacy runner did not save optimizer, scheduler and RNG state or expose a resume API. The manifests therefore store an explicit blocked resume description instead of a fabricated command.
