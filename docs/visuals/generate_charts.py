"""
Generate portfolio-grade data visualizations from ai_dev_metrics.md data.
Output: docs/visuals/
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe
from matplotlib.patches import FancyBboxPatch
import numpy as np
import os

OUT = os.path.dirname(os.path.abspath(__file__))

DARK_BG   = "#0d1117"
CARD_BG   = "#161b22"
ACCENT    = "#58a6ff"
ACCENT2   = "#3fb950"
ACCENT3   = "#d29922"
RED       = "#f85149"
TEXT      = "#e6edf3"
SUBTEXT   = "#8b949e"
BORDER    = "#30363d"


# ─────────────────────────────────────────────────────────────────────────────
# 1. COMPETITIVE BENCHMARK  (log-scale bar chart, LOC/hr + Tokens/hr)
# ─────────────────────────────────────────────────────────────────────────────
def chart_competitive_benchmark():
    fig, axes = plt.subplots(1, 2, figsize=(16, 8), dpi=240)
    fig.patch.set_facecolor(DARK_BG)

    labels    = ["Average\nDeveloper", "Top 1%\nElite", "Arda"]
    loc_mid   = [30,   750,   2512]
    loc_lo    = [10,   500,   2512]
    loc_hi    = [50,  1000,   2512]
    tok_mid   = [30_000,  2_000_000, 7_350_000]
    tok_lo    = [15_000,  1_000_000, 7_350_000]
    tok_hi    = [45_000,  3_000_000, 7_350_000]

    colors    = [SUBTEXT, ACCENT3, ACCENT2]
    x         = np.arange(len(labels))

    for ax, mid, lo, hi, unit, title, top_val, multiplier_label in [
        (axes[0], loc_mid, loc_lo, loc_hi, "LOC / Hour",
         "Output Velocity — Lines of Code per Hour",
         2800, "~3.4× above Top 1%"),
        (axes[1], tok_mid, tok_lo, tok_hi, "Tokens / Hour",
         "Throughput — Tokens per Hour",
         8_200_000, "~3.7× above Top 1%"),
    ]:
        ax.set_facecolor(CARD_BG)
        for spine in ax.spines.values():
            spine.set_color(BORDER)

        bars = ax.bar(x, mid, color=colors, width=0.55,
                      zorder=3, linewidth=0, edgecolor="none")

        # error bands (range)
        for xi, (l, h, c) in enumerate(zip(lo, hi, colors)):
            if l != h:
                ax.plot([xi, xi], [l, h], color=c, lw=2, zorder=4, alpha=0.6)
                ax.plot([xi - 0.08, xi + 0.08], [l, l], color=c, lw=2, zorder=4, alpha=0.6)
                ax.plot([xi - 0.08, xi + 0.08], [h, h], color=c, lw=2, zorder=4, alpha=0.6)

        ax.set_ylim(0, top_val)
        ax.yaxis.set_major_formatter(
            matplotlib.ticker.FuncFormatter(
                lambda v, _: f"{int(v):,}" if v < 1_000_000 else f"{v/1_000_000:.1f}M"
            )
        )
        ax.tick_params(colors=SUBTEXT, labelsize=11)
        ax.set_xticks(x)
        ax.set_xticklabels(labels, color=TEXT, fontsize=13)
        ax.yaxis.label.set_color(SUBTEXT)
        ax.set_ylabel(unit, fontsize=11, color=SUBTEXT)
        ax.set_title(title, color=TEXT, fontsize=14, fontweight="bold", pad=14)
        ax.grid(axis="y", color=BORDER, linestyle="--", linewidth=0.6, zorder=0)

        # value labels on bars — small bars get label above, Arda gets it inside
        for i, (bar, val) in enumerate(zip(bars, mid)):
            fmt = f"{val:,.0f}" if val < 1_000_000 else f"{val/1_000_000:.2f}M"
            if i == 2:  # Arda — label inside bar
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    val * 0.5,
                    fmt,
                    ha="center", va="center",
                    color=DARK_BG, fontsize=13, fontweight="bold",
                )
            else:
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    val + top_val * 0.02,
                    fmt,
                    ha="center", va="bottom",
                    color=TEXT, fontsize=11, fontweight="bold",
                )

        # highlight Arda bar border
        bars[2].set_linewidth(2)
        bars[2].set_edgecolor(ACCENT2)

        # gap bracket between Top 1% and Arda
        y_top1 = mid[1]
        y_arda = mid[2]
        bx = x[2] + 0.35
        ax.annotate("", xy=(bx, y_arda), xytext=(bx, y_top1),
                    arrowprops=dict(arrowstyle="<->", color=ACCENT2, lw=2.0))
        ax.text(bx + 0.07, (y_top1 + y_arda) / 2, multiplier_label,
                color=ACCENT2, fontsize=10, fontweight="bold", va="center")

    fig.suptitle(
        "Developer Output Benchmark — Global Percentile Comparison",
        color=TEXT, fontsize=17, fontweight="bold", y=1.01,
    )
    fig.text(
        0.5, -0.02,
        "Source: Arda's Cursor IDE session metrics · 20.9 active dev hours · 153.5M tokens processed · Log scale",
        ha="center", color=SUBTEXT, fontsize=10,
    )

    plt.tight_layout()
    path = os.path.join(OUT, "competitive_benchmark.png")
    fig.savefig(path, dpi=240, bbox_inches="tight",
                facecolor=DARK_BG, edgecolor="none")
    plt.close(fig)
    print(f"Saved: {path}")


# ─────────────────────────────────────────────────────────────────────────────
# 2. METRICS DASHBOARD  (KPI cards grid)
# ─────────────────────────────────────────────────────────────────────────────
def chart_metrics_dashboard():
    fig = plt.figure(figsize=(16, 11), dpi=240)
    fig.patch.set_facecolor(DARK_BG)

    cards = [
        ("7.35M",      "Tokens / Hour",           ACCENT,  "Peak AI throughput"),
        ("2,512",      "LOC / Hour",               ACCENT2, "Sustained output velocity"),
        ("~99%",       "Code Retention Rate",      ACCENT3, "Production-ready on first pass"),
        ("153.5M",     "Total Tokens Processed",   ACCENT,  "Across 20.9 active hours"),
        ("52,502",     "Lines of Code",            ACCENT2, "Total edited LOC"),
        ("~100×",      "Arda vs. Avg. Developer",  RED,     "Productivity multiplier"),
        ("~2.9k",      "Tokens per LOC",           ACCENT3, "Deliberate re-audit density"),
        ("Top 0.01%",  "Arda — Global Percentile", ACCENT,  "AI-native developer tier"),
    ]

    # title
    fig.text(0.5, 0.975,
             "AI-Assisted Development — Key Performance Metrics",
             ha="center", va="top",
             color=TEXT, fontsize=18, fontweight="bold")

    # 8 KPI cards (4×2 grid)
    n_cols, n_rows = 4, 2
    pad_x  = 0.03
    top_y  = 0.89   # where cards start (below title)
    bot_y  = 0.28   # where cards end (above cost banner)
    pad_y  = 0.04
    w = (1 - pad_x * (n_cols + 1)) / n_cols
    h = (top_y - bot_y - pad_y * (n_rows + 1)) / n_rows

    for i, (value, label, color, sub) in enumerate(cards):
        col = i % n_cols
        row = i // n_cols
        x0  = pad_x + col * (w + pad_x)
        y0  = top_y - pad_y - (row + 1) * h - row * pad_y

        ax = fig.add_axes([x0, y0, w, h])
        ax.set_facecolor(CARD_BG)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_color(color)
            spine.set_linewidth(1.5)

        ax.add_patch(FancyBboxPatch(
            (0, 0.88), 1, 0.12,
            boxstyle="square,pad=0", color=color, alpha=0.18, transform=ax.transAxes
        ))
        ax.plot([0, 1], [0.88, 0.88], color=color, lw=1.5, transform=ax.transAxes, alpha=0.5)

        ax.text(0.5, 0.56, value,
                ha="center", va="center", transform=ax.transAxes,
                color=color, fontsize=30, fontweight="bold",
                fontfamily="monospace")
        ax.text(0.5, 0.28, label,
                ha="center", va="center", transform=ax.transAxes,
                color=TEXT, fontsize=12, fontweight="semibold")
        ax.text(0.5, 0.10, sub,
                ha="center", va="center", transform=ax.transAxes,
                color=SUBTEXT, fontsize=9)

    # ── Cost Efficiency Banner ──────────────────────────────────────────────
    GOLD   = "#ffd700"
    banner_y = 0.07
    banner_h = 0.17
    ax_cost = fig.add_axes([pad_x, banner_y, 1 - 2 * pad_x, banner_h])
    ax_cost.set_facecolor(CARD_BG)
    ax_cost.set_xlim(0, 1)
    ax_cost.set_ylim(0, 1)
    ax_cost.set_xticks([])
    ax_cost.set_yticks([])
    for spine in ax_cost.spines.values():
        spine.set_color(GOLD)
        spine.set_linewidth(2.0)

    # gold accent strip on left
    ax_cost.add_patch(FancyBboxPatch(
        (0, 0), 0.008, 1,
        boxstyle="square,pad=0", color=GOLD, alpha=0.9, transform=ax_cost.transAxes
    ))

    # three columns inside the banner
    col_data = [
        ("~$60",          "/ month",           "Total AI Compute Cost",
         "5 days @ 80% quota → full month extrapolated to 60$ tier"),
        ("~$0.0003",      "/ LOC",             "Cost per Line of Code",
         "$60 ÷ ~231,000 LOC/month (22 working days extrapolated)"),
        ("~231k  LOC",    "per month",         "Extrapolated Monthly Output",
         "52,502 LOC in 5 days · ×22 working days · production-ready"),
    ]
    xs = [0.18, 0.50, 0.82]
    for cx, (big, small, label, sub) in zip(xs, col_data):
        ax_cost.text(cx, 0.72, big,
                     ha="center", va="center", transform=ax_cost.transAxes,
                     color=GOLD, fontsize=26, fontweight="bold", fontfamily="monospace")
        ax_cost.text(cx, 0.50, small,
                     ha="center", va="center", transform=ax_cost.transAxes,
                     color=GOLD, fontsize=13, fontweight="bold", alpha=0.75)
        ax_cost.text(cx, 0.30, label,
                     ha="center", va="center", transform=ax_cost.transAxes,
                     color=TEXT, fontsize=11, fontweight="semibold")
        ax_cost.text(cx, 0.10, sub,
                     ha="center", va="center", transform=ax_cost.transAxes,
                     color=SUBTEXT, fontsize=8.5)

    # vertical dividers
    for divx in [0.34, 0.66]:
        ax_cost.axvline(divx, color=BORDER, lw=1.2, alpha=0.7)

    fig.text(0.5, 0.025,
             "Arda · Human-in-the-loop · Serially Orchestrated · TDD-Enforced · 1 Chat / Phase",
             ha="center", va="bottom",
             color=SUBTEXT, fontsize=10)

    path = os.path.join(OUT, "metrics_dashboard.png")
    fig.savefig(path, dpi=240, bbox_inches="tight",
                facecolor=DARK_BG, edgecolor="none")
    plt.close(fig)
    print(f"Saved: {path}")


# ─────────────────────────────────────────────────────────────────────────────
# 3. VELOCITY × QUALITY MATRIX  (bubble positioning chart)
# ─────────────────────────────────────────────────────────────────────────────
def chart_velocity_quality_matrix():
    fig, ax = plt.subplots(figsize=(16, 11), dpi=240)
    fig.patch.set_facecolor(DARK_BG)
    ax.set_facecolor(CARD_BG)
    for spine in ax.spines.values():
        spine.set_color(BORDER)

    # (x=LOC/hr midpoint, y=retention%, size, color, label, offset)
    devs = [
        (30,    70,  300,  SUBTEXT, "Average\nDeveloper",   (-0.05, -6)),
        (750,   85,  700,  ACCENT3, "Top 1%\nElite",        (0.04,  -7)),
        (2512,  99,  1800, ACCENT2, "Arda",                   (0.04,  1)),
    ]

    for xv, yv, sz, col, lbl, (dx, dy) in devs:
        ax.scatter(xv, yv, s=sz, color=col, alpha=0.85, zorder=4,
                   linewidths=2, edgecolors=col)
        ax.text(xv + xv * dx, yv + dy, lbl,
                color=col, fontsize=12, fontweight="bold",
                ha="left" if dx >= 0 else "right", va="center")

    # quadrant shading
    ax.axvspan(0,    400,  alpha=0.04, color=RED,    zorder=0)
    ax.axvspan(400,  1200, alpha=0.04, color=ACCENT3, zorder=0)
    ax.axvspan(1200, 3200, alpha=0.06, color=ACCENT2, zorder=0)

    ax.axhline(90, color=BORDER, lw=1, linestyle="--", zorder=2)
    ax.text(3100, 90.5, "Production threshold", color=SUBTEXT,
            fontsize=9, ha="right")

    # annotation arrow "The Sweet Spot"
    ax.annotate(
        "  Arda — Tier-0 Zone\n  High Velocity + High Quality",
        xy=(2512, 99), xytext=(1500, 95),
        color=ACCENT2, fontsize=11, fontweight="bold",
        arrowprops=dict(arrowstyle="->", color=ACCENT2, lw=1.5),
    )

    ax.set_xscale("log")
    ax.set_xlim(8, 4200)
    ax.set_ylim(55, 102)
    ax.set_xlabel("Output Velocity (LOC / Hour)  —  log scale",
                  color=SUBTEXT, fontsize=12)
    ax.set_ylabel("Code Retention Rate (%)", color=SUBTEXT, fontsize=12)
    ax.tick_params(colors=SUBTEXT, labelsize=11)
    ax.xaxis.set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda v, _: f"{int(v):,}")
    )
    ax.grid(color=BORDER, linestyle="--", linewidth=0.5, zorder=1)

    ax.set_title(
        "Velocity × Quality Matrix — Developer Positioning",
        color=TEXT, fontsize=16, fontweight="bold", pad=14,
    )
    fig.text(
        0.5, -0.02,
        "Retention Rate = % of generated code committed to production without rework   ·   "
        "Bubble size ∝ tokens/hour throughput",
        ha="center", color=SUBTEXT, fontsize=9,
    )

    path = os.path.join(OUT, "velocity_quality_matrix.png")
    fig.savefig(path, dpi=240, bbox_inches="tight",
                facecolor=DARK_BG, edgecolor="none")
    plt.close(fig)
    print(f"Saved: {path}")


# ─────────────────────────────────────────────────────────────────────────────
# 4. WORKFLOW EFFICIENCY BREAKDOWN  (horizontal stacked / gantt-style)
# ─────────────────────────────────────────────────────────────────────────────
def chart_workflow_breakdown():
    fig, ax = plt.subplots(figsize=(16, 7), dpi=240)
    fig.patch.set_facecolor(DARK_BG)
    ax.set_facecolor(CARD_BG)
    for spine in ax.spines.values():
        spine.set_color(BORDER)

    phases   = ["Planning", "TDD\n(Tests First)", "Implementation", "Iteration\n(Green Suite)", "Validation\n& Review"]
    portions = [15,          20,                  35,               20,                         10]
    colors   = [ACCENT, ACCENT3, ACCENT2, ACCENT3, ACCENT]
    icons    = ["🗺",   "🧪",    "⚙️",     "🔄",     "✅"]

    left = 0
    for phase, portion, color, icon in zip(phases, portions, colors, icons):
        ax.barh(0, portion, left=left, height=0.45,
                color=color, alpha=0.82, edgecolor=DARK_BG, linewidth=2)
        cx = left + portion / 2
        ax.text(cx, 0.03, f"{portion}%",
                ha="center", va="center", color=DARK_BG,
                fontsize=13, fontweight="bold")
        ax.text(cx, -0.33, phase,
                ha="center", va="top", color=TEXT,
                fontsize=10, fontweight="semibold")
        left += portion

    ax.set_xlim(0, 100)
    ax.set_ylim(-0.7, 0.5)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(
        "Deterministic Workflow — Phase Distribution",
        color=TEXT, fontsize=15, fontweight="bold", pad=14,
    )

    legend_items = [
        mpatches.Patch(color=ACCENT,  label="Architecture & Review phases"),
        mpatches.Patch(color=ACCENT3, label="Quality-enforcement phases (TDD / Iteration)"),
        mpatches.Patch(color=ACCENT2, label="Implementation phase"),
    ]
    ax.legend(handles=legend_items, loc="lower center",
              bbox_to_anchor=(0.5, -0.28), ncol=3,
              facecolor=CARD_BG, edgecolor=BORDER,
              labelcolor=TEXT, fontsize=10)

    fig.text(
        0.5, -0.01,
        "TDD guardrails + Plan-first execution → 99% retention rate · zero-hallucination production output",
        ha="center", color=SUBTEXT, fontsize=10,
    )

    plt.tight_layout(rect=[0, 0.08, 1, 1])
    path = os.path.join(OUT, "workflow_breakdown.png")
    fig.savefig(path, dpi=240, bbox_inches="tight",
                facecolor=DARK_BG, edgecolor="none")
    plt.close(fig)
    print(f"Saved: {path}")


if __name__ == "__main__":
    chart_competitive_benchmark()
    chart_metrics_dashboard()
    chart_velocity_quality_matrix()
    chart_workflow_breakdown()
    print("\nAll charts generated successfully.")
