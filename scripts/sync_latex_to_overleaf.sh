#!/usr/bin/env bash
set -euo pipefail

project_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
overleaf_url="${OVERLEAF_REMOTE_URL:-https://git@git.overleaf.com/6a69ac75d6170c19b9e2711a}"
overleaf_branch="${OVERLEAF_BRANCH:-main}"
skip_local_build=0

if [[ $# -gt 0 && "$1" == "--skip-local-build" ]]; then
  skip_local_build=1
  shift
fi

if ! git -C "$project_root" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "The thesis workspace is not a Git repository." >&2
  exit 2
fi

if [[ -n "$(git -C "$project_root" status --porcelain)" ]]; then
  echo "The thesis workspace has uncommitted changes. Commit and push GitHub before syncing Overleaf." >&2
  exit 3
fi

github_commit="$(git -C "$project_root" rev-parse --short=12 HEAD)"
commit_message="${1:-Sync LaTeX from GitHub ${github_commit}}"
sync_root="$(mktemp -d /tmp/phd-thesis-overleaf.XXXXXX)"
deploy_repo="$sync_root/repo"

cleanup() {
  python3 - "$sync_root" <<'PY'
from pathlib import Path
import shutil
import sys

target = Path(sys.argv[1]).resolve()
tmp_root = Path('/tmp').resolve()
if target.parent == tmp_root and target.name.startswith('phd-thesis-overleaf.'):
    shutil.rmtree(target, ignore_errors=True)
PY
}
trap cleanup EXIT

GIT_TERMINAL_PROMPT=0 GCM_INTERACTIVE=never \
  git clone --branch "$overleaf_branch" --single-branch "$overleaf_url" "$deploy_repo"

# Replace only the paths owned by the Overleaf deployment.  The Overleaf
# repository also retains project-management material that is intentionally
# GitHub-only/local-only; deleting the whole clone would turn that material
# into an accidental deployment change.
git -C "$deploy_repo" rm -rq --ignore-unmatch -- \
  .gitignore \
  main.tex \
  latexmkrc \
  Makefile \
  FDSDSthesis.cls \
  fig \
  macros.tex \
  SRC \
  fduthesis.cls \
  fduthesis-en.cls \
  fduthesis.def \
  fudan-emblem.pdf \
  fudan-emblem-new.pdf \
  fudan-name.pdf \
  chapters \
  config \
  bibliography \
  figures \
  tables \
  scripts/run_bibtex.sh
install -d \
  "$deploy_repo/fig" \
  "$deploy_repo/SRC" \
  "$deploy_repo/chapters" \
  "$deploy_repo/bibliography" \
  "$deploy_repo/figures" \
  "$deploy_repo/tables" \
  "$deploy_repo/scripts"

rsync -a \
  "$project_root/.gitignore" \
  "$project_root/main.tex" \
  "$project_root/latexmkrc" \
  "$project_root/Makefile" \
  "$project_root/FDSDSthesis.cls" \
  "$project_root/macros.tex" \
  "$deploy_repo/"
rsync -a "$project_root/fig/" "$deploy_repo/fig/"
rsync -a --include='*.tex' --exclude='*' "$project_root/SRC/" "$deploy_repo/SRC/"
rsync -a --include='*.tex' --exclude='*' "$project_root/chapters/" "$deploy_repo/chapters/"
rsync -a "$project_root/bibliography/references.bib" "$deploy_repo/bibliography/"
rsync -a "$project_root/figures/" "$deploy_repo/figures/"
rsync -a "$project_root/tables/" "$deploy_repo/tables/"
rsync -a "$project_root/scripts/run_bibtex.sh" "$deploy_repo/scripts/"

git -C "$deploy_repo" add -A

if git -C "$deploy_repo" diff --cached --name-only | grep -Eq \
  '^(sources|handoff|qa|evidence|prompts|tasks|drafts)/'; then
  echo "Refusing to sync a GitHub-only or local-only path to Overleaf." >&2
  exit 4
fi

if git -C "$deploy_repo" diff --cached --quiet; then
  echo "Overleaf is already synchronized with GitHub commit ${github_commit}."
  exit 0
fi

if [[ "$skip_local_build" -eq 1 ]]; then
  fingerprint="$(python3 "$project_root/scripts/latex_input_fingerprint.py")"
  marker="/tmp/phd-thesis-local-build.$fingerprint.ok"
  if [[ ! -f "$marker" ]]; then
    echo "No matching verified local-build fingerprint; refusing to skip deployment build." >&2
    exit 5
  fi
  now="$(date +%s)"
  verified_at="$(cat "$marker")"
  if ! [[ "$verified_at" =~ ^[0-9]+$ ]] || (( now - verified_at > 1800 )); then
    echo "Matching local-build fingerprint is older than 30 minutes; refusing to skip deployment build." >&2
    exit 5
  fi
  echo "Reusing local build verified at $verified_at; Overleaf will compile after the non-force push."
else
  (
    cd "$deploy_repo"
    latexmk -xelatex -interaction=nonstopmode -file-line-error main.tex
  )

  if grep -Eqi \
    'undefined citations?|undefined references?|Citation .* undefined|Reference .* undefined|multiply defined|LaTeX Error' \
    "$deploy_repo/main.log"; then
    echo "The deployment build contains unresolved LaTeX errors or references; refusing to push." >&2
    exit 6
  fi
fi

git -C "$deploy_repo" commit --no-gpg-sign -m "$commit_message"
GIT_TERMINAL_PROMPT=0 GCM_INTERACTIVE=never git -C "$deploy_repo" push origin "$overleaf_branch"

local_head="$(git -C "$deploy_repo" rev-parse HEAD)"
remote_head="$(GIT_TERMINAL_PROMPT=0 GCM_INTERACTIVE=never \
  git -C "$deploy_repo" ls-remote origin "refs/heads/${overleaf_branch}" | awk '{print $1}')"
if [[ "$local_head" != "$remote_head" ]]; then
  echo "Overleaf push completed but remote verification failed." >&2
  exit 7
fi

echo "Overleaf synchronized at ${remote_head} from GitHub commit ${github_commit}."
