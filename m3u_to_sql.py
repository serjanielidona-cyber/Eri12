#!/usr/bin/env python3
# m3u_to_sql.py
# Reads an M3U file and writes an SQL file with INSERT statements for a `channels` table.
# Usage: python3 m3u_to_sql.py input.m3u channels.sql

import sys
import re
import html

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


def sql_escape(s):
    if s is None:
        return 'NULL'
    # Trim and escape single quotes and backslashes
    s = s.strip()
    s = s.replace('\\', '\\\\')
    s = s.replace("'", "\\'")
    return "'" + s + "'"


def write_sql(channels, out_path='channels.sql', table='channels', batch_size=200):
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write('-- Generated SQL to import channels into table: {}\n'.format(table))
        f.write("-- Columns: name, stream_url, logo, tvg_id, category\n")
        f.write('START TRANSACTION;\n')
        count = 0
        batch = []
        for c in channels:
            name = c.get('name','')
            url = c.get('url','')
            logo = c.get('logo','')
            tvg_id = c.get('tvg_id','')
            group = c.get('group','')
            # skip entries without url
            if not url:
                continue
            vals = (
                sql_escape(name),
                sql_escape(url),
                sql_escape(logo),
                sql_escape(tvg_id),
                sql_escape(group)
            )
            row = '(' + ','.join(vals) + ')'
            batch.append(row)
            count += 1
            if len(batch) >= batch_size:
                f.write('INSERT INTO {} (name, stream_url, logo, tvg_id, category) VALUES\n'.format(table))
                f.write(',\n'.join(batch) + ';\n')
                batch = []
        if batch:
            f.write('INSERT INTO {} (name, stream_url, logo, tvg_id, category) VALUES\n'.format(table))
            f.write(',\n'.join(batch) + ';\n')
        f.write('COMMIT;\n')
    print(f'Wrote {count} channels to {out_path}')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python3 m3u_to_sql.py input.m3u [output.sql]')
        sys.exit(1)
    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else 'channels.sql'
    print('Parsing', input_path)
    channels = parse_m3u(input_path)
    print(f'Found {len(channels)} entries; writing SQL to {output_path}')
    write_sql(channels, output_path)
