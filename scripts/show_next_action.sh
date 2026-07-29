#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
sed -n '/当前小节/ p; /下一动作/ p; /当前编译状态/ p' "$ROOT/STATE.md"
