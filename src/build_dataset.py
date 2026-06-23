"""
Build Russell Westbrook's 2016-17 MVP season dataset from Basketball-Reference.

Source: his game log (https://www.basketball-reference.com/players/w/westbru01/gamelog/2017/)
— one row per game with points, rebounds, assists, etc. We clean it, flag triple-doubles,
parse the win/loss result, and tag the month, then validate against the season's famous
facts (81 games, 42 triple-doubles, 31.6 / 10.7 / 10.4) before writing the CSV.

Also pulls his career per-game table for one "scoring in context" chart.

Outputs: data/processed/westbrook_2016_17_gamelog.csv
         data/processed/westbrook_career_pergame.csv  (best-effort; for context chart)
"""
import io, os, re
import pandas as pd
import common as C


def load_game_log():
    html = C.http_get(
        f"https://www.basketball-reference.com/players/w/{C.PLAYER}/gamelog/{C.SEASON_END}/",
        cache_name=f"gamelog_{C.SEASON_END}.html")
    tables = pd.read_html(io.StringIO(html))
    gl = next(t for t in tables if {"PTS", "TRB", "AST", "Rk"}.issubset(t.columns))
    # drop repeated header rows (non-numeric Rk)
    gl = gl[pd.to_numeric(gl["Rk"], errors="coerce").notna()].copy()
    for c in ["Rk", "PTS", "TRB", "AST", "STL", "BLK", "TOV", "MP"]:
        if c in gl.columns:
            gl[c] = pd.to_numeric(gl[c], errors="coerce")
    gl = gl[gl["PTS"].notna()].copy()          # games actually played
    gl["game_no"] = range(1, len(gl) + 1)
    gl["triple_double"] = (gl["PTS"] >= 10) & (gl["TRB"] >= 10) & (gl["AST"] >= 10)
    gl["win"] = gl["Result"].astype(str).str.startswith("W")
    gl["month"] = pd.to_datetime(gl["Date"], errors="coerce").dt.strftime("%b %Y")
    gl["home"] = gl["Unnamed: 5"].isna() if "Unnamed: 5" in gl.columns else None  # '@' marks away
    return gl


def load_career_pergame():
    """Best-effort: per-game averages by season for a 'scoring in context' chart."""
    try:
        html = C.http_get(
            f"https://www.basketball-reference.com/players/w/{C.PLAYER}.html",
            cache_name="player_page.html")
        tables = pd.read_html(io.StringIO(html))
        pg = next(t for t in tables if "PTS" in t.columns and "Season" in t.columns)
        pg = pg[pg["Season"].astype(str).str.match(r"\d{4}-\d{2}")].copy()
        pg = pg.groupby("Season", as_index=False).first()  # collapse multi-team rows
        for c in ["PTS", "TRB", "AST"]:
            pg[c] = pd.to_numeric(pg[c], errors="coerce")
        return pg[["Season", "PTS", "TRB", "AST"]].dropna()
    except Exception as e:
        print("  (career table unavailable, skipping context chart):", e)
        return None


def build():
    gl = load_game_log()
    cols = ["game_no", "Date", "month", "Opp", "Result", "win", "MP",
            "PTS", "TRB", "AST", "STL", "BLK", "TOV", "FG%", "3P%", "triple_double"]
    cols = [c for c in cols if c in gl.columns]
    out = os.path.join(C.PROC, "westbrook_2016_17_gamelog.csv")
    gl[cols].to_csv(out, index=False)

    career = load_career_pergame()
    if career is not None:
        career.to_csv(os.path.join(C.PROC, "westbrook_career_pergame.csv"), index=False)

    # ---- correctness gate ----
    games = len(gl)
    td = int(gl["triple_double"].sum())
    ppg, rpg, apg = gl["PTS"].mean(), gl["TRB"].mean(), gl["AST"].mean()
    print("=== Russell Westbrook, 2016-17 — correctness gate ===")
    checks = [
        ("games played", games, C.KNOWN["games"], games == C.KNOWN["games"]),
        ("triple-doubles", td, C.KNOWN["triple_doubles"], td == C.KNOWN["triple_doubles"]),
        ("points/game", round(ppg, 1), C.KNOWN["ppg"], round(ppg, 1) == C.KNOWN["ppg"]),
        ("rebounds/game", round(rpg, 1), C.KNOWN["rpg"], round(rpg, 1) == C.KNOWN["rpg"]),
        ("assists/game", round(apg, 1), C.KNOWN["apg"], round(apg, 1) == C.KNOWN["apg"]),
    ]
    ok = True
    for name, got, exp, good in checks:
        ok = ok and good
        print(f"  {name:16}: {got:<7} (expected {exp})  {'OK' if good else '!! MISMATCH'}")
    print(f"\nWrote {games} games -> {out}")
    if not ok:
        raise SystemExit("Correctness gate FAILED.")
    return gl


if __name__ == "__main__":
    build()
