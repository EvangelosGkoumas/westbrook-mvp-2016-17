# 🧭 GUIDE — running this & building your own basketball projects

This is the basketball counterpart to the Ronaldo project — same four-step recipe, a
different sport and data source.

## Run it
```bash
python -m venv .venv && .venv\Scripts\activate     # Windows (source .venv/bin/activate on Mac/Linux)
pip install -r requirements.txt
python run_all.py
```
Charts land in `outputs/`, tables in `data/processed/`. First run downloads + caches the
data; later runs are offline. Run a single step with e.g. `python src/viz.py`.

## The recipe (same as every data project)
```
1. GET     →  download the data            (build_dataset.py)
2. CLEAN   →  one tidy table (CSV)          (build_dataset.py)
3. ANALYZE →  ask questions in SQL          (analyze_sql.py)
4. SHOW    →  charts + README               (viz.py)
```
Plus the two professional habits: **a correctness gate** (validate a known number — here
42 triple-doubles — before trusting anything) and **written-down sources** (`SOURCES.md`).

## How to get NBA data (important)
- **Basketball-Reference** (used here): pull any player's game log / season tables with
  `pandas.read_html`. Works from a normal PC. URL pattern:
  `basketball-reference.com/players/<initial>/<id>/gamelog/<year>/`
  (Westbrook = `westbru01`, 2016-17 season = year `2017`).
- **nba_api** (`pip install nba_api`): official NBA data incl. **shot charts** and
  play-by-play. Best run from your **own computer** — the NBA blocks cloud servers.
- **Kaggle**: ready-made NBA CSVs if you want to skip scraping.

## Make a new basketball project — change three things
1. **Player / season** in `src/common.py` (`PLAYER`, `SEASON_END`, and the `KNOWN` facts
   for the correctness gate).
2. **Questions** in `analyze_sql.py` (new SQL).
3. **Charts** in `viz.py`.

## Ideas to extend this
- Add **shot charts** with `nba_api` (from your PC) — where his points came from.
- Compare Westbrook's 2016-17 to **Oscar Robertson 1961-62** or to other MVP seasons.
- Build an **efficiency** view (TS%, usage rate) to engage the "empty stats?" debate.
- Pull **career game logs** to chart triple-doubles per season across his whole career.

See the big **`Sports-Analytics-Field-Guide.pdf`** in the portfolio folder for the full
catalogue of data sources, tools, books and a 90-day plan.
