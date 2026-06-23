# Data sources & provenance

Free, public data only.

| Layer | Source | What we take |
|---|---|---|
| Game-by-game stats (2016-17) | [Basketball-Reference — Westbrook 2016-17 game log](https://www.basketball-reference.com/players/w/westbru01/gamelog/2017/) | points, rebounds, assists, result, date per game |
| Career per-game averages (context chart) | [Basketball-Reference — Westbrook player page](https://www.basketball-reference.com/players/w/westbru01.html) | PPG by season |

## Accuracy gate
`build_dataset.py` validates the parsed season against the record books before writing
any output:

| Metric | Official | Parsed |
|---|---|---|
| Games played | 81 | 81 ✅ |
| Triple-doubles | 42 (single-season record) | 42 ✅ |
| Points/game | 31.6 | 31.6 ✅ |
| Rebounds/game | 10.7 | 10.7 ✅ |
| Assists/game | 10.4 | 10.4 ✅ |

If the source page format changes and breaks parsing, the build fails loudly rather than
producing wrong charts.

## Notes
- Triple-double = ≥10 in points, rebounds and assists in a single game.
- Regular season only; playoffs excluded.
- Data © Sports Reference LLC — used here for a non-commercial personal project; please
  credit Basketball-Reference if reused.

> Tip: Basketball-Reference works fine from a normal PC. The official `stats.nba.com`
> API (and `nba_api`) is great for shot charts but tends to block cloud servers — run
> those from your own machine.
