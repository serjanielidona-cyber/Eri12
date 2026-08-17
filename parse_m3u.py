#!/usr/bin/env python3
# parse_m3u.py
# Reads an M3U file and writes channels.csv with columns: name,tvg_id,logo,group,url
# Usage: python3 parse_m3u.py input.m3u

import sys
import re
import csv

EXTINF_RE = re.compile(r'#EXTINF:-?\d+(?:\s+(.*))?,\s*(.*)$')
ATTR_RE = re.compile(r'(\w[\w\-]*)="([^"]*)"')


def parse_m3u(path):
    channels = []
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = [l.rstrip('\n') for l in f]

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith('#EXTINF'):
            m = EXTINF_RE.match(line)
            if m:
                attr_str = m.group(1) or ""
                name_field = m.group(2) or ""
                attrs = dict(ATTR_RE.findall(attr_str))
                tvg_id = attrs.get('tvg-id', '').strip()
                logo = attrs.get('tvg-logo', '').strip()
                group = attrs.get('group-title', '').strip()
                name = name_field.strip() or attrs.get('tvg-name', '').strip() or ''
                # next non-empty non-comment line is usually URL
                url = ''
                j = i + 1
                while j < len(lines):
                    l2 = lines[j].strip()
                    if l2 == '' or l2.startswith('#'):
                        j += 1
                        continue
                    url = l2
                    break
                channels.append({
                    'name': name,
                    'tvg_id': tvg_id,
                    'logo': logo,
                    'group': group,
                    'url': url
                })
                i = j
            else:
                i += 1
        else:
            i += 1
    return channels


def write_csv(channels, out_path='channels.csv'):
    with open(out_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['name','tvg_id','logo','group','url']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for c in channels:
            writer.writerow(c)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python3 parse_m3u.py input.m3u')
        sys.exit(1)
    input_path = sys.argv[1]
    print('Parsing', input_path)
    channels = parse_m3u(input_path)
    print(f'Found {len(channels)} channels; writing channels.csv')
    write_csv(channels)
    print('Done.')
