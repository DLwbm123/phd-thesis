#!/usr/bin/env bash
set -euo pipefail
for seed in 42 43 44; do
  sed "s/--seed 42/--seed $seed/g; s#/42/#/$seed/#g" "$(dirname "$0")/run_core_pilot.sh" | bash -s -- "$@"
done
