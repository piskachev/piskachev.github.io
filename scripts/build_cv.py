#!/usr/bin/env python3
"""Build files/cv.pdf from the site data.

Reads _data/cv.yml, _data/service.yml, _publications/ and _talks/, writes
cv/cv.json and compiles cv/cv.typ with Typst.

Usage: pip install pyyaml typst && python scripts/build_cv.py
"""
import glob
import json
import os
import re
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF_CATEGORIES = ('manuscripts', 'conferences')
MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
          'August', 'September', 'October', 'November', 'December']


def load_yaml(path):
    with open(os.path.join(ROOT, path), encoding='utf-8') as f:
        return yaml.safe_load(f)


def front_matter(path):
    with open(path, encoding='utf-8') as f:
        text = f.read()
    m = re.match(r'---\n(.*?)\n---\n', text, re.S)
    return yaml.safe_load(m.group(1)) if m else {}


def plain(s):
    """Drop Markdown links, keeping the link text."""
    s = re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', s)
    return s.replace('**', '')


def venue_year(venue, year):
    """Append the year unless the venue text already contains it."""
    return venue if year in venue else '%s, %s' % (venue, year)


def publications():
    rows = []
    for path in glob.glob(os.path.join(ROOT, '_publications', '*.md')):
        fm = front_matter(path)
        if fm.get('category') not in PDF_CATEGORIES:
            continue
        citation = fm.get('citation', '')
        authors = citation.split('. "')[0] if '. "' in citation else ''
        excerpt = fm.get('excerpt', '') or ''
        note = excerpt[len(authors) + 1:].strip() if authors and excerpt.startswith(authors) else excerpt
        date = fm['date']
        rows.append({
            'date': str(date),
            'authors': authors,
            'title': fm['title'],
            'venue': fm.get('venue', ''),
            'venue_year': venue_year(fm.get('venue', ''), str(date)[:4]),
            'note': plain(note),
        })
    rows.sort(key=lambda r: r['date'], reverse=True)
    return rows


def talks():
    rows = []
    for path in glob.glob(os.path.join(ROOT, '_talks', '*.md')):
        fm = front_matter(path)
        d = str(fm['date'])
        rows.append({
            'date': '%s %s' % (MONTHS[int(d[5:7]) - 1], d[:4]),
            'sort': d,
            'title': fm['title'],
            'venue': fm.get('venue', ''),
            'location': fm.get('location', '') or '',
        })
    rows.sort(key=lambda r: r['sort'], reverse=True)
    return rows


def short_service_item(item, section_title):
    """Condense a Service line to 'NAME years' for the PDF."""
    text = plain(item)
    m = re.match(r'^(.*): ((?:\d{4})(?:, \d{4})*)$', text)
    if m:
        return '%s %s' % (m.group(1).split(' \u2013 ')[0], m.group(2))
    if section_title in ('Organizing', 'Editorial'):
        return text
    return text.split(' \u2013 ')[0]


def main():
    cv = load_yaml('_data/cv.yml')
    service = load_yaml('_data/service.yml')

    data = {
        'name': cv['name'],
        'email': cv['email'],
        'website': cv['website'],
        'orcid': cv['orcid'],
        'scholar': cv['scholar'],
        'github': cv['github'],
        'linkedin': cv['linkedin'],
        'location': cv['location'],
        'languages': cv['languages'],
        'experience': cv['experience'],
        'education': cv['education'],
        'awards': [plain(a) for a in cv['awards']],
        'supervision': [plain(a) for a in cv['supervision']],
        'teaching_assistance': [plain(a) for a in cv['teaching_assistance']],
        'publications': publications(),
        'talks': talks(),
        'service': [
            {'title': s['title'], 'items': [short_service_item(i, s['title']) for i in s['items']]}
            for s in service
        ],
    }
    cv_dir = os.path.join(ROOT, 'cv')
    with open(os.path.join(cv_dir, 'cv.json'), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=1)

    import typst
    out = os.path.join(ROOT, 'files', 'cv.pdf')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    typst.compile(os.path.join(cv_dir, 'cv.typ'), output=out, root=ROOT)
    print('wrote', out)


if __name__ == '__main__':
    sys.exit(main())
