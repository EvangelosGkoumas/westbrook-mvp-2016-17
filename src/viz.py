"""
Charts for Westbrook's 2016-17 MVP season. Reads the game log + query CSVs and writes
PNGs to outputs/. House style uses OKC Thunder colours (blue + sunset orange).
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import common as C

BLUE, ORANGE, NAVY, GREY = "#007AC1", "#EF3B24", "#002D62", "#9aa3b2"
plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 11, "axes.edgecolor": GREY,
    "axes.linewidth": 0.8, "axes.grid": True, "grid.color": "#eef0f4",
    "axes.spines.top": False, "axes.spines.right": False, "figure.dpi": 130,
})

GL = pd.read_csv(os.path.join(C.PROC, "westbrook_2016_17_gamelog.csv"))


def q(name):
    return pd.read_csv(os.path.join(C.PROC, f"q_{name}.csv"))


def _labels(ax, bars, fmt="{:.0f}", color=NAVY):
    for b in bars:
        ax.text(b.get_x() + b.get_width() / 2, b.get_height(), fmt.format(b.get_height()),
                ha="center", va="bottom", fontsize=10, color=color)


def chart_cumulative_td():
    g = GL.copy()
    g["cum_td"] = g["triple_double"].cumsum()
    game_42 = int(g.loc[g["cum_td"] == 42, "game_no"].min())
    fig, ax = plt.subplots(figsize=(9, 4.8))
    ax.step(g["game_no"], g["cum_td"], where="post", color=BLUE, lw=2.5)
    ax.axhline(41, color=GREY, ls="--", lw=1)
    ax.text(2, 41.6, "Oscar Robertson's record: 41 (1961-62)", color=GREY, fontsize=9)
    ax.scatter([game_42], [42], color=ORANGE, zorder=5, s=70)
    ax.annotate(f"42nd triple-double\n(new record) — game {game_42}",
                xy=(game_42, 42), xytext=(game_42 - 30, 30), color=ORANGE, fontsize=9,
                arrowprops=dict(arrowstyle="->", color=ORANGE))
    ax.set_title("Chasing history: cumulative triple-doubles, 2016-17",
                 fontweight="bold", color=NAVY)
    ax.set_xlabel("Game number"); ax.set_ylabel("Triple-doubles")
    fig.tight_layout(); fig.savefig(os.path.join(C.OUT, "01_cumulative_triple_doubles.png")); plt.close(fig)


def chart_averages():
    s = q("season_summary").iloc[0]
    cats, vals = ["Points", "Rebounds", "Assists"], [s["ppg"], s["rpg"], s["apg"]]
    fig, ax = plt.subplots(figsize=(7, 4.6))
    bars = ax.bar(cats, vals, color=[ORANGE, BLUE, NAVY])
    _labels(ax, bars, "{:.1f}")
    ax.axhline(10, color=GREY, ls="--", lw=1.2)
    ax.text(2.4, 10.4, "triple-double line (10)", color=GREY, fontsize=9, ha="right")
    ax.set_title("Averaged a triple-double — first since Oscar Robertson (1961-62)",
                 fontweight="bold", color=NAVY)
    ax.set_ylabel("Per-game average")
    fig.tight_layout(); fig.savefig(os.path.join(C.OUT, "02_season_averages.png")); plt.close(fig)


def chart_impact():
    d = q("triple_double_impact")
    fig, ax = plt.subplots(figsize=(7, 4.6))
    colors = [BLUE if "Triple" in t else GREY for t in d["game_type"]]
    bars = ax.bar(d["game_type"], d["win_pct"], color=colors, width=0.55)
    _labels(ax, bars, "{:.1f}%")
    for x, w, l in zip(range(len(d)), d["wins"], d["losses"]):
        ax.text(x, 4, f"{int(w)}-{int(l)}", ha="center", color="white", fontsize=10, fontweight="bold")
    ax.set_title("Triple-doubles won games: 78.6% vs 33.3%", fontweight="bold", color=NAVY)
    ax.set_ylabel("Team win %"); ax.set_ylim(0, 100)
    fig.tight_layout(); fig.savefig(os.path.join(C.OUT, "03_triple_double_impact.png")); plt.close(fig)


def chart_scatter():
    fig, ax = plt.subplots(figsize=(8, 5.2))
    sc = ax.scatter(GL["TRB"], GL["AST"], c=GL["PTS"], cmap="YlOrRd", s=60,
                    edgecolors=NAVY, linewidth=0.4, zorder=3)
    ax.axvline(10, color=GREY, ls="--", lw=1); ax.axhline(10, color=GREY, ls="--", lw=1)
    ax.axvspan(10, GL["TRB"].max() + 1, ymin=0, alpha=0.04, color=BLUE)
    ax.text(GL["TRB"].max(), GL["AST"].max(), "triple-double zone\n(≥10 reb & ≥10 ast)",
            ha="right", va="top", color=BLUE, fontsize=9)
    cb = fig.colorbar(sc, ax=ax); cb.set_label("Points")
    ax.set_title("Every game: rebounds vs assists (colour = points)", fontweight="bold", color=NAVY)
    ax.set_xlabel("Rebounds"); ax.set_ylabel("Assists")
    fig.tight_layout(); fig.savefig(os.path.join(C.OUT, "04_rebounds_vs_assists.png")); plt.close(fig)


def chart_by_month():
    d = q("by_month")
    fig, ax = plt.subplots(figsize=(9, 4.6))
    bars = ax.bar(d["month"], d["triple_doubles"], color=BLUE)
    _labels(ax, bars)
    ax.plot(d["month"], d["games"], color=ORANGE, marker="o", lw=2, label="Games played")
    ax.set_title("Triple-doubles by month (orange = games played)", fontweight="bold", color=NAVY)
    ax.set_ylabel("Triple-doubles"); ax.legend(frameon=False)
    fig.tight_layout(); fig.savefig(os.path.join(C.OUT, "05_triple_doubles_by_month.png")); plt.close(fig)


def chart_career_context():
    path = os.path.join(C.PROC, "westbrook_career_pergame.csv")
    if not os.path.exists(path):
        return
    d = pd.read_csv(path)
    fig, ax = plt.subplots(figsize=(10, 4.6))
    colors = [ORANGE if s == "2016-17" else BLUE for s in d["Season"]]
    bars = ax.bar(d["Season"], d["PTS"], color=colors)
    ax.set_title("Scoring in context: points per game by season (2016-17 in orange)",
                 fontweight="bold", color=NAVY)
    ax.set_ylabel("Points per game"); plt.setp(ax.get_xticklabels(), rotation=45, ha="right", fontsize=8)
    fig.tight_layout(); fig.savefig(os.path.join(C.OUT, "06_career_scoring_context.png")); plt.close(fig)


def run():
    chart_cumulative_td(); chart_averages(); chart_impact()
    chart_scatter(); chart_by_month(); chart_career_context()
    print("Saved charts -> outputs/01..06")


if __name__ == "__main__":
    run()
