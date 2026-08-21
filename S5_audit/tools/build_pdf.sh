#!/usr/bin/env bash
# Compile tous les .tex de S5_cloture. Moteur : pdflatex via latexmk.
# Le style partagé est trouvé via TEXINPUTS, sans duplication de fichier.
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export PYTHONDONTWRITEBYTECODE=1
export TEXINPUTS="$ROOT/_common:${TEXINPUTS:-}"
LOGDIR="$ROOT/_build_logs"
mkdir -p "$LOGDIR"
fail=0; ok=0
while IFS= read -r tex; do
  dir="$(dirname "$tex")"; base="$(basename "$tex" .tex)"
  if (cd "$dir" && latexmk -pdf -interaction=nonstopmode -halt-on-error -silent \
        -jobname="$base" "$base.tex" >"$LOGDIR/$base.build.log" 2>&1); then
    ok=$((ok+1))
  else
    fail=$((fail+1)); echo "ECHEC : $tex (voir $LOGDIR/$base.build.log)"
  fi
  (cd "$dir" && latexmk -c -silent "$base.tex" >/dev/null 2>&1)
done < <(find "$ROOT" -name '*.tex' | sort)
echo "compilation : $ok réussites, $fail échecs"
exit $((fail>0))
