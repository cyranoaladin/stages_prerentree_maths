"""Normalize pseudo-LaTeX (...)/[...] math delimiters to real $...$/$$...$$ for Pandoc.

Only touches spans that actually contain a LaTeX signal (backslash command, ^, _, or
the French decimal macro {,}) -- i.e. spans that would otherwise leak raw LaTeX code
to the reader. Plain parenthetical text like "(5)" or "(voir plus loin)" is untouched.
"""
import re
import sys
from pathlib import Path

MATH_SIGNAL = re.compile(r'\\[a-zA-Z]|[\^_]|\{,\}')

def is_math(content: str) -> bool:
    return bool(MATH_SIGNAL.search(content))

def find_balanced(text: str, open_ch: str, close_ch: str, start: int):
    """Return the index just after the matching close_ch for an open at `start`, or None."""
    depth = 0
    i = start
    while i < len(text):
        if text[i] == open_ch:
            depth += 1
        elif text[i] == close_ch:
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    return None

def convert_inline_parens(line: str) -> tuple[str, int]:
    out = []
    i = 0
    n = 0
    in_math = False
    while i < len(line):
        if line[i] == '$':
            in_math = not in_math
            out.append(line[i])
            i += 1
            continue
        if not in_math and line[i] == '(' and (i == 0 or line[i-1] != ']'):
            end = find_balanced(line, '(', ')', i)
            if end is not None:
                inner = line[i+1:end-1]
                if is_math(inner):
                    out.append('$' + inner.strip() + '$')
                    n += 1
                    i = end
                    continue
        out.append(line[i])
        i += 1
    return ''.join(out), n

BLOCK_OPEN = re.compile(r'^(\s*)\[\s*$')
BLOCK_CLOSE = re.compile(r'^\s*\]\s*$')

def convert_display_blocks(lines: list[str]) -> tuple[list[str], int]:
    out = []
    i = 0
    n = 0
    while i < len(lines):
        open_match = BLOCK_OPEN.match(lines[i])
        if open_match:
            indent = open_match.group(1)
            j = i + 1
            content_lines = []
            found_close = False
            while j < len(lines):
                if BLOCK_CLOSE.match(lines[j]):
                    found_close = True
                    break
                content_lines.append(lines[j])
                j += 1
            if found_close:
                content = ' '.join(l.strip() for l in content_lines if l.strip())
                # A prior pass (bare-line/inline tiers) may have already wrapped the
                # formula itself in $...$ -- in that case just drop the [ ] wrapper
                # instead of nesting a second, invalid pair of math delimiters.
                if '$' in content:
                    out.append(indent + content)
                else:
                    out.append(indent + '$$' + content + '$$')
                n += 1
                i = j + 1
                continue
        out.append(lines[i])
        i += 1
    return out, n

# Tier 3: bare formula lines/blockquotes not wrapped in ( ) or [ ].
# Conservative: only fires when, after stripping backslash-commands, digits, operators,
# spaces and single-letter variable tokens, no run of >=2 letters remains (i.e. no
# leftover French prose word) AND the line actually contains a backslash command.
WORDY = re.compile(r'[A-Za-zÀ-ÿ]{2,}')
CMD = re.compile(r'\\[a-zA-Z]+(\{[^{}]*\})*')

def strip_math_tokens(s: str) -> str:
    s = CMD.sub(' ', s)
    # Replace (not delete) stripped math punctuation so unrelated single-letter
    # variables either side of a removed span never fuse into a fake "word".
    s = re.sub(r'[0-9+\-*/=<>≤≥°%.,{}^_|\s]', ' ', s)
    return s

def bare_formula_candidate(text: str) -> bool:
    if '\\' not in text:
        return False
    remainder = strip_math_tokens(text)
    return not WORDY.search(remainder)

def convert_bare_lines(lines: list[str]) -> tuple[list[str], int]:
    out = []
    n = 0
    for line in lines:
        stripped = line
        prefix = ''
        m = re.match(r'^(>\s*)', line)
        if m:
            prefix = m.group(1)
            stripped = line[len(prefix):]
        # skip lines that are already inside $...$ or already processed, or empty, or pure prose
        if stripped.strip() and '$' not in stripped and bare_formula_candidate(stripped):
            leading_ws = stripped[:len(stripped) - len(stripped.lstrip(' '))]
            core = stripped.strip()
            trailing = ''
            if core.endswith('.') and not core.endswith('\\.'):
                trailing = '.'
                core = core[:-1]
            out.append(prefix + leading_ws + '$' + core + '$' + trailing)
            n += 1
        else:
            out.append(line)
    return out, n

def process_file(path: Path) -> dict:
    text = path.read_text(encoding='utf-8')
    lines = text.split('\n')
    lines, n_blocks = convert_display_blocks(lines)
    lines, n_bare = convert_bare_lines(lines)
    new_lines = []
    n_inline = 0
    for line in lines:
        if line.startswith('$$') and line.endswith('$$'):
            new_lines.append(line)
            continue
        converted, n = convert_inline_parens(line)
        n_inline += n
        new_lines.append(converted)
    new_text = '\n'.join(new_lines)
    changed = new_text != text
    if changed:
        path.write_text(new_text, encoding='utf-8')
    return {"path": str(path), "blocks": n_blocks, "bare": n_bare, "inline": n_inline, "changed": changed}

if __name__ == "__main__":
    results = []
    for arg in sys.argv[1:]:
        results.append(process_file(Path(arg)))
    for r in results:
        if r["blocks"] or r["bare"] or r["inline"]:
            print(r)
