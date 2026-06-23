"""
SQL analysis (DuckDB) of Westbrook's 2016-17 season — the same kind of aggregation work
done in BigQuery, run locally over the game-log CSV. Each query answers one question about
the historic triple-double season and saves a CSV for the charts / README.
"""
import os
import duckdb
import common as C

CSV = os.path.join(C.PROC, "westbrook_2016_17_gamelog.csv")
con = duckdb.connect()
con.execute(f"CREATE VIEW g AS SELECT * FROM read_csv_auto('{CSV}', header=true)")

QUERIES = {
"season_summary": """
    SELECT COUNT(*) AS games,
           SUM(triple_double::INT) AS triple_doubles,
           ROUND(AVG(PTS),1) AS ppg, ROUND(AVG(TRB),1) AS rpg, ROUND(AVG(AST),1) AS apg,
           ROUND(100.0*SUM(triple_double::INT)/COUNT(*),1) AS td_rate_pct
    FROM g
""",
# Did the triple-doubles translate to wins?
"triple_double_impact": """
    SELECT CASE WHEN triple_double THEN 'Triple-double' ELSE 'No triple-double' END AS game_type,
           COUNT(*) AS games,
           SUM(win::INT) AS wins,
           SUM((NOT win)::INT) AS losses,
           ROUND(100.0*SUM(win::INT)/COUNT(*),1) AS win_pct
    FROM g GROUP BY 1 ORDER BY win_pct DESC
""",
# scoring volume buckets
"scoring_buckets": """
    SELECT CASE WHEN PTS>=50 THEN '50+' WHEN PTS>=40 THEN '40-49'
                WHEN PTS>=30 THEN '30-39' WHEN PTS>=20 THEN '20-29' ELSE 'under 20' END AS pts_bucket,
           COUNT(*) AS games
    FROM g GROUP BY 1
    ORDER BY MIN(PTS) DESC
""",
# month-by-month (ordered by first game of each month)
"by_month": """
    SELECT month,
           COUNT(*) AS games,
           SUM(triple_double::INT) AS triple_doubles,
           ROUND(AVG(PTS),1) AS ppg, ROUND(AVG(TRB),1) AS rpg, ROUND(AVG(AST),1) AS apg
    FROM g GROUP BY month ORDER BY MIN(game_no)
""",
}


def run():
    summary = {}
    for name, sql in QUERIES.items():
        df = con.execute(sql).df()
        summary[name] = df
        df.to_csv(os.path.join(C.PROC, f"q_{name}.csv"), index=False)
        print(f"\n=== {name} ===")
        print(df.to_string(index=False))

    imp = summary["triple_double_impact"].set_index("game_type")
    td_wp = imp.loc["Triple-double", "win_pct"] if "Triple-double" in imp.index else 0
    print("\n" + "=" * 56)
    print("HEADLINE: Westbrook's 2016-17 MVP season")
    print("  First player since Oscar Robertson (1961-62) to average a triple-double")
    print("  42 triple-doubles in 81 games — a single-season record")
    print(f"  Thunder won {td_wp}% of his triple-double games")
    return summary


if __name__ == "__main__":
    run()
