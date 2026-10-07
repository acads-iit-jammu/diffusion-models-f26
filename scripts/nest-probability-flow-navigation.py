"""Nest the book's generated topic groups under Lecture Notes.

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
    changed = False
    for label in ('Probability-Flow ODE', 'Score Matching and Stochastic Sampling'):
        lecture = group_span(html, 'Lecture Notes')
        topic = group_span(html, label)
        if lecture is None or topic is None:
            continue
        if lecture[0] < topic[0] < topic[1] < lecture[1]:
            continue  # Idempotent on repeated builds.
        block = html[topic[0]:topic[1]].replace('sidebar-section depth1', 'sidebar-section depth2')
        html = html[:topic[0]] + html[topic[1]:]
        lecture = group_span(html, 'Lecture Notes')
        insert = html.rfind('</ul>', lecture[0], lecture[1])
        if insert < 0:
            raise ValueError(f'Missing lecture list: {path}')
        html = html[:insert] + block + '\n' + html[insert:]
        lecture, topic = group_span(html, 'Lecture Notes'), group_span(html, label)
        assert lecture[0] < topic[0] < topic[1] < lecture[1], path
        changed = True
    if changed:
        path.write_text(html)
        count += 1
print(f'Nested topic navigation in {count} pages.')
