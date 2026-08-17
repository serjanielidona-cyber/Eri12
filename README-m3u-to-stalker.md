# M3U → Stalker/Ministra import helpers

This branch contains a small utility to parse an M3U playlist (like mag420_shqip_...m3u) and produce a CSV file suitable for manual import into a Stalker/Ministra portal or for further SQL conversion.

Files added:
- parse_m3u.py — Python script that reads an M3U and writes channels.csv with columns: name,tvg_id,logo,group,url

How to use (locally):
1. Download the M3U file from the repository (Raw URL), or clone the repo.
   Example raw URL (from your repo):
   https://raw.githubusercontent.com/serjanielidona-cyber/Eri12/main/mag420_shqip_sport_filma_nen1mb%20%282%29.m3u

2. Run the parser:
   python3 parse_m3u.py "mag420_shqip_filma_nen1mb (2).m3u"

3. The script will produce channels.csv in the current directory.

Importing into Ministra/Stalker:
- If your Ministra admin panel supports CSV import, map the CSV columns (name -> channel name, url -> stream URL, logo -> logo URL, tvg_id -> external id, group -> category) and import.
- If it doesn't, you can use the CSV to generate SQL INSERTs for your Ministra database. Be sure to BACK UP your database before importing.

SQL template example (adapt to your DB schema):

```sql
-- Example template: adjust table/column names to your Ministra installation
-- Back up your DB before running any inserts.
INSERT INTO channels (name,stream_url,logo,tvg_id,category) VALUES
-- one row per channel, e.g.:
('Channel 1', 'http://stream.example/1', 'http://logo.example/1.png', 'ch1', 'Sport');
```

Notes & warnings:
- Many streams in public M3U lists may be copyrighted or require subscriptions. Make sure you have the right to use/distribute any streams you import.
- Always back up Ministra DB before importing.

If you want, I can:
- Run the parser for you and commit channels.csv into this repo (large file). Say "Please add channels.csv" and I'll push it.
- Or generate SQL INSERTs tailored to your Ministra DB schema if you provide table/column names or a schema dump.
