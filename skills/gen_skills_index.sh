#!/usr/bin/env bash
# gen_skills_index.sh - regenerate the AUTO-INDEX table in the root SKILLS.md
# so every agent-sync commit carries an up-to-date catalog. Scans
# skills/*/SKILL.md (+ VERSION). Hand-written SKILLS.md sections are kept;
# only the block between the AUTO-INDEX markers is rewritten.

set -u -o pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO"

PY3=""
for cand in python3 python; do
  if command -v "$cand" >/dev/null 2>&1 && "$cand" -c 'import sys; sys.exit(0)' >/dev/null 2>&1; then
    PY3="$cand"; break
  fi
done
[ -n "$PY3" ] || { echo "[gen-skills] no working python3 - index not refreshed" >&2; exit 0; }

MD="SKILLS.md"
BEGIN_MARK="<!-- BEGIN:AUTO-INDEX -->"
END_MARK="<!-- END:AUTO-INDEX -->"
[ -f "$MD" ] || { echo "[gen-skills] $MD missing - nothing to do" >&2; exit 0; }

TMP="$(mktemp)"
{
  echo "| 技能 | 版本 | 说明 |"
  echo "|---|---|---|"
  for d in skills/*/; do
    name="$(basename "$d")"
    s="${d}SKILL.md"
    [ -f "$s" ] || continue
    ver="-"
    [ -f "${d}VERSION" ] && ver="$(head -1 "${d}VERSION" | tr -d '[:space:]')"
    fname="$(grep -m1 '^name:' "$s" 2>/dev/null | sed 's/^name:[[:space:]]*//')"
    [ -z "$fname" ] && fname="$(grep -m1 '^# ' "$s" | sed 's/^# //')"
    # description: plain value, OR a YAML block scalar (> >- | |-) whose text
    # lives on the following indented lines - Light's own skills use the block
    # form, and reading only the first line used to print a bare ">-"
    fdesc="$(awk '
      BEGIN { block = 0 }
      {
        if (block == 1) {
          if ($0 ~ /^[ \t]*$/) next
          if ($0 ~ /^[ \t]/) { line = $0; sub(/^[ \t]+/, "", line); printf "%s ", line; next }
          printf "\n"; exit
        }
        if ($0 ~ /^description:/) {
          val = $0; sub(/^description:[ \t]*/, "", val)
          if (val ~ /^[>|][-+]?[ \t]*$/) { block = 1; next }
          gsub(/^"|"$/, "", val); print val; exit
        }
      }
      END { if (block == 1) printf "\n" }
    ' "$s" 2>/dev/null)"
    if [ -z "$fdesc" ]; then
      fdesc="$(grep -m1 '^> ' "$s" | sed 's/^> //; s/\*\*//g')"
    fi
    # character-safe truncation (cut -c would split multibyte CJK in a C locale)
    fdesc="$(printf '%s' "$fdesc" | "$PY3" -c 'import sys
s = " ".join(sys.stdin.read().split())
print(s[:160] + "\u2026" if len(s) > 160 else s)')"
    fname="${fname//|/\\|}"
    fdesc="${fdesc//|/\\|}"
    echo "| **$name** | $ver | $fname — $fdesc |"
  done
} > "$TMP"

python3 - "$MD" "$TMP" "$BEGIN_MARK" "$END_MARK" <<'PY'
import sys, io
md, tbl, b, e = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
s = io.open(md, encoding='utf-8').read()
new = io.open(tbl, encoding='utf-8').read().rstrip('\n')
if b not in s or e not in s:
    sys.exit('markers missing in ' + md)
i = s.index(b) + len(b)
j = s.index(e)
io.open(md, 'w', encoding='utf-8').write(s[:i] + '\n' + new + '\n' + s[j:])
print('[gen-skills] index refreshed')
PY
rm -f "$TMP"
