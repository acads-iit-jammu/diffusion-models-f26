"""Nest the book's generated probability-flow sidebar group under Lecture Notes.

Quarto book navigation flattens parts even with explicit sidebar contents.
Move the complete generated list item; preserve links and collapse targets.
"""
from pathlib import Path
import re

MARKER = '<li class="sidebar-item sidebar-item-section">'

def group_span(html, label):
    pos = html.find(f'<span class="menu-text">{label}</span>')
    if pos < 0:
        return None
    start = html.rfind(MARKER, 0, pos)
    if start < 0:
        raise ValueError(f'Missing sidebar group for {label}')
    depth = 0
    for token in re.finditer(r'<li\b[^>]*>|</li\s*>', html[start:]):
        depth += -1 if token.group().startswith('</') else 1
        if depth == 0:
            return start, start + token.end()
    raise ValueError(f'Unclosed sidebar group for {label}')

count = 0
for path in Path('_site').rglob('*.html'):
    html = path.read_text()
    lecture = group_span(html, 'Lecture Notes')
    flow = group_span(html, 'Probability-Flow ODE')
    if lecture is None or flow is None:
        continue
    if lecture[0] < flow[0] < flow[1] < lecture[1]:
        continue  # Idempotent on repeated builds.
    block = html[flow[0]:flow[1]].replace('sidebar-section depth1', 'sidebar-section depth2')
    html = html[:flow[0]] + html[flow[1]:]
    lecture = group_span(html, 'Lecture Notes')
    insert = html.rfind('</ul>', lecture[0], lecture[1])
    if insert < 0:
        raise ValueError(f'Missing lecture list: {path}')
    html = html[:insert] + block + '\n' + html[insert:]
    lecture, flow = group_span(html, 'Lecture Notes'), group_span(html, 'Probability-Flow ODE')
    assert lecture[0] < flow[0] < flow[1] < lecture[1], path
    path.write_text(html)
    count += 1
print(f'Nested probability-flow navigation in {count} pages.')
