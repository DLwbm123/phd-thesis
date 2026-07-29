#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

TASK_FILE="${1:-tasks/INBOX.md}"
REPORT_FILE="handoff/LATEST_CODEX_REPORT.md"

if [[ ! -f "$TASK_FILE" ]]; then
  echo "Task file not found: $TASK_FILE" >&2
  exit 1
fi

codex exec \
  --sandbox workspace-write \
  --ask-for-approval never \
  --output-last-message "$REPORT_FILE" \
  - < "$TASK_FILE"

echo "Codex report: $REPORT_FILE"
