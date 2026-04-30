"""Generate the token-cost/DFS/CNR scatter plot for the paper."""

from __future__ import annotations

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import FancyBboxPatch


CONFIGS = ["Fixed-5", "Full-15", "Domain-opt", "Phase0-Auto"]
CASES = ["AD", "ATM", "Library", "RollCall", "Bookkeep."]

TOKENS = [
    [20, 18, 18, 16, 16],
    [62, 58, 53, 47, 47],
    [23, 21, 19, 23, 17],
    [36, 34, 27, 33, 32],
]

DFS = [
    [0.55, 0.36, 0.00, 0.00, 0.40],
    [0.57, 0.57, 0.50, 0.50, 0.50],
    [0.83, 0.83, 0.73, 0.73, 0.73],
    [0.86, 0.77, 0.64, 0.66, 0.78],
]

CNR = [
    [0.11, 0.00, 0.60, 0.50, 0.60],
    [0.65, 0.67, 0.33, 1.00, 0.80],
    [0.22, 0.33, 0.00, 0.20, 0.00],
    [0.13, 0.00, 0.11, 0.30, 0.33],
]


MARKERS = {
    "Fixed-5": "s",
    "Full-15": "^",
    "Domain-opt": "D",
    "Phase0-Auto": "o",
}

EDGE_COLORS = {
    "Fixed-5": "#8c2d2d",
    "Full-15": "#5e3c99",
    "Domain-opt": "#1b7837",
    "Phase0-Auto": "#2166ac",
}

FACE_COLORS = {
    "Fixed-5": "#d95f5f",
    "Full-15": "#8e6cc8",
    "Domain-opt": "#4daf7c",
    "Phase0-Auto": "#3b9edb",
}


def bubble_size(cnr: float) -> float:
    return 20 + cnr * 180


def configure_matplotlib() -> None:
    mpl.rcParams.update(
        {
            "font.family": "serif",
            "font.serif": ["Times New Roman", "DejaVu Serif", "Times"],
            "font.size": 9,
            "axes.labelsize": 9,
            "xtick.labelsize": 8,
            "ytick.labelsize": 8,
            "legend.fontsize": 7.2,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "svg.fonttype": "none",
            "axes.linewidth": 0.7,
        }
    )


def build_plot() -> tuple[plt.Figure, plt.Axes]:
    configure_matplotlib()
    fig, ax = plt.subplots(figsize=(3.5, 2.8))
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    ideal_region = FancyBboxPatch(
        (14, 0.58),
        30,
        0.44,
        boxstyle="round,pad=0.015,rounding_size=0.03",
        linewidth=0.7,
        edgecolor="#7fbf7b",
        facecolor="#c7e9c0",
        alpha=0.32,
        zorder=0,
    )
    ax.add_patch(ideal_region)
    ax.text(
        15.3,
        0.955,
        "Ideal region",
        fontsize=8,
        fontstyle="italic",
        color="0.20",
        zorder=1,
    )

    for cfg_idx, cfg in enumerate(CONFIGS):
        ax.scatter(
            TOKENS[cfg_idx],
            DFS[cfg_idx],
            s=[bubble_size(v) for v in CNR[cfg_idx]],
            marker=MARKERS[cfg],
            facecolors=FACE_COLORS[cfg],
            edgecolors=EDGE_COLORS[cfg],
            linewidths=0.8,
            alpha=0.86 if cfg != "Phase0-Auto" else 0.92,
            zorder=3 if cfg == "Phase0-Auto" else 2,
            clip_on=False,
        )

    ax.annotate(
        "DFS = 0\n(Library, RollCall)",
        xy=(17.1, 0.0),
        xytext=(31.5, 0.145),
        textcoords="data",
        fontsize=7.3,
        ha="left",
        va="center",
        arrowprops={
            "arrowstyle": "->",
            "color": "0.20",
            "lw": 0.7,
            "shrinkA": 2,
            "shrinkB": 4,
        },
        bbox={"boxstyle": "round,pad=0.18", "fc": "white", "ec": "0.82", "alpha": 0.92, "lw": 0.5},
        zorder=5,
    )

    ax.annotate(
        "Full-15: high cost,\nhigh noise",
        xy=(58.5, 0.56),
        xytext=(40.2, 0.315),
        textcoords="data",
        fontsize=7.3,
        ha="left",
        va="center",
        arrowprops={
            "arrowstyle": "->",
            "color": "0.20",
            "lw": 0.7,
            "shrinkA": 2,
            "shrinkB": 4,
        },
        bbox={"boxstyle": "round,pad=0.18", "fc": "white", "ec": "0.82", "alpha": 0.92, "lw": 0.5},
        zorder=5,
    )

    ax.set_xlim(10, 68)
    ax.set_ylim(0, 1.0)
    ax.set_xlabel("Token Cost (K)")
    ax.set_ylabel("Domain Fit Score (DFS)")
    ax.set_xticks([10, 20, 30, 40, 50, 60])
    ax.set_yticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax.grid(True, color="0.88", linewidth=0.55, linestyle="-", zorder=0)
    ax.set_axisbelow(True)

    config_handles = [
        Line2D(
            [0],
            [0],
            marker=MARKERS[cfg],
            linestyle="",
            markerfacecolor=FACE_COLORS[cfg],
            markeredgecolor=EDGE_COLORS[cfg],
            markeredgewidth=0.8,
            markersize=5.1,
            label=cfg,
        )
        for cfg in CONFIGS
    ]
    fig.legend(
        handles=config_handles,
        loc="lower left",
        bbox_to_anchor=(0.13, 0.015),
        ncol=4,
        frameon=True,
        framealpha=0.94,
        facecolor="white",
        edgecolor="0.78",
        borderpad=0.25,
        columnspacing=0.75,
        handletextpad=0.35,
    )

    size_handles = [
        plt.scatter(
            [],
            [],
            s=bubble_size(v) * 0.55,
            marker="o",
            facecolors="white",
            edgecolors="0.25",
            linewidths=0.8,
            label=label,
        )
        for v, label in [(0.0, "CNR=0%"), (0.5, "CNR=50%"), (1.0, "CNR=100%")]
    ]
    ax.legend(
        handles=size_handles,
        loc="upper right",
        bbox_to_anchor=(0.995, 0.99),
        frameon=True,
        framealpha=0.94,
        facecolor="white",
        edgecolor="0.78",
        borderpad=0.35,
        labelspacing=0.45,
        handletextpad=0.9,
        title="Noise",
        title_fontsize=7.2,
    )

    for spine in ax.spines.values():
        spine.set_color("0.20")
        spine.set_linewidth(0.7)

    fig.subplots_adjust(left=0.17, right=0.985, top=0.965, bottom=0.285)
    return fig, ax


def main() -> None:
    output_dir = Path("experiments/results")
    output_dir.mkdir(parents=True, exist_ok=True)
    base = output_dir / "dfs_token_cnr_scatter"

    fig, _ = build_plot()
    fig.savefig(f"{base}.pdf", dpi=600, bbox_inches="tight")
    fig.savefig(f"{base}.png", dpi=300, bbox_inches="tight")
    fig.savefig(f"{base}.svg", bbox_inches="tight")
    plt.close(fig)

    print(f"Wrote {base}.pdf")
    print(f"Wrote {base}.png")
    print(f"Wrote {base}.svg")


if __name__ == "__main__":
    main()
