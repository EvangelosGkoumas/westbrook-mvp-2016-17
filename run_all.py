"""
Run the whole Westbrook 2016-17 pipeline end to end:
  1. build_dataset  -> fetch Basketball-Reference game log, clean, validate, write CSV
  2. analyze_sql    -> DuckDB SQL aggregations -> data/processed/q_*.csv
  3. viz            -> charts -> outputs/01..06

Usage:  python run_all.py
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
import build_dataset, analyze_sql, viz

if __name__ == "__main__":
    print("\n[1/3] Building dataset ...");   build_dataset.build()
    print("\n[2/3] Running SQL analysis ..."); analyze_sql.run()
    print("\n[3/3] Charts ...");               viz.run()
    print("\nDone. See outputs/ for charts and data/processed/ for tables.")
