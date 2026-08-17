Added m3u_to_sql.py — a script to convert the repository M3U into an SQL file containing INSERT statements for a default `channels` table.

How to use (locally):
1) Download the M3U raw file from the repo, for example:
   curl -L -o mag.m3u "https://raw.githubusercontent.com/serjanielidona-cyber/Eri12/main/mag420_shqip_sport_filma_nen1mb%20%282%29.m3u"

2) Run the converter:
   python3 m3u_to_sql.py mag.m3u channels.sql

3) Upload/import channels.sql into your MySQL/phpMyAdmin or adapt the INSERT template to your Ministra/Stalker schema.

Notes:
- The generated SQL uses the table name `channels` and columns: name, stream_url, logo, tvg_id, category. Adjust if your DB schema differs.
- The script batches INSERTs (200 rows per INSERT) and wraps statements in a transaction.
- Make a DB backup before importing.
