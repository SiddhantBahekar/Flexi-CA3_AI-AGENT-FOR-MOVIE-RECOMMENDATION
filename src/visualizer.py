"""
Visualizer Module: Generates analytics and insights charts for the movie dataset.
Uses Matplotlib with custom dark-cinema styling for Gradio integration.
"""

import matplotlib
matplotlib.use("Agg")  # Non-interactive backend
import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter

# Cinema dark mode styling with high-contrast accessibility
DARK_BG = "#0b1329"
CARD_BG = "#131d38"
TEXT_COLOR = "#ffffff"
LABEL_COLOR = "#e2e8f0"
ACCENT_CYAN = "#38bdf8"
ACCENT_PURPLE = "#a855f7"
ACCENT_AMBER = "#f59e0b"
GRID_COLOR = "#334155"
SPINE_COLOR = "#475569"

def apply_cinema_style(fig, ax):
    """Applies modern high-contrast dark cinema styling to matplotlib figures."""
    fig.patch.set_facecolor(DARK_BG)
    ax.set_facecolor(CARD_BG)
    ax.tick_params(colors=LABEL_COLOR, labelsize=10)
    ax.xaxis.label.set_color(TEXT_COLOR)
    ax.xaxis.label.set_fontweight("bold")
    ax.yaxis.label.set_color(TEXT_COLOR)
    ax.yaxis.label.set_fontweight("bold")
    ax.title.set_color(TEXT_COLOR)
    ax.title.set_fontweight("bold")
    for spine in ax.spines.values():
        spine.set_color(SPINE_COLOR)
        spine.set_linewidth(1.2)
    ax.grid(True, linestyle="--", alpha=0.45, color=GRID_COLOR)

def plot_genre_distribution(df):
    """Plots top genres bar chart with high-contrast vibrant bars."""
    all_genres = []
    for g_str in df["genre"]:
        for g in str(g_str).split(","):
            g = g.strip()
            if g:
                all_genres.append(g)

    counts = Counter(all_genres).most_common(10)
    labels = [c[0] for c in reversed(counts)]
    values = [c[1] for c in reversed(counts)]

    fig, ax = plt.subplots(figsize=(8, 4.5), dpi=100)
    apply_cinema_style(fig, ax)

    bars = ax.barh(labels, values, color="#0284c7", alpha=0.92, edgecolor="#38bdf8", linewidth=1.2)
    ax.bar_label(bars, padding=5, color="#ffffff", fontsize=9.5, weight="bold")
    ax.set_title("Top 10 Movie Genres in Catalog", fontsize=13, weight="bold", pad=12)
    ax.set_xlabel("Number of Titles", fontsize=10, labelpad=8)
    plt.tight_layout()
    return fig

def plot_rating_vs_year(df):
    """Plots scatter plot of rating versus release year with high-contrast colorbar."""
    fig, ax = plt.subplots(figsize=(8, 4.5), dpi=100)
    apply_cinema_style(fig, ax)

    scatter = ax.scatter(
        df["year"],
        df["rating"],
        c=df["rating"],
        cmap="cool",
        alpha=0.9,
        s=65,
        edgecolors="#ffffff",
        linewidths=0.8
    )
    cbar = fig.colorbar(scatter, ax=ax)
    cbar.set_label("IMDb Rating", color="#ffffff", fontsize=10, weight="bold")
    cbar.ax.yaxis.set_tick_params(color="#ffffff", labelsize=9)
    try:
        cbar.outline.set_edgecolor(SPINE_COLOR)
        cbar.outline.set_linewidth(1.2)
    except Exception:
        pass
    plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color="#ffffff", weight="bold")

    ax.set_title("Rating Distribution Across Eras (1950 - 2024)", fontsize=13, weight="bold", pad=12)
    ax.set_xlabel("Release Year", fontsize=10, labelpad=8)
    ax.set_ylabel("IMDb Score", fontsize=10, labelpad=8)
    ax.set_ylim(6.8, 9.6)
    plt.tight_layout()
    return fig

def plot_mood_distribution(df):
    """Plots the distribution of emotional mood tags."""
    all_moods = []
    for m_str in df["mood_tags"]:
        for m in str(m_str).split(","):
            m = m.strip()
            if m:
                all_moods.append(m)

    counts = Counter(all_moods).most_common(8)
    labels = [c[0] for c in counts]
    values = [c[1] for c in counts]

    fig, ax = plt.subplots(figsize=(8, 4.5), dpi=100)
    apply_cinema_style(fig, ax)

    bars = ax.bar(labels, values, color="#9333ea", alpha=0.92, edgecolor="#c084fc", linewidth=1.2)
    ax.bar_label(bars, padding=4, color="#ffffff", fontsize=9.5, weight="bold")
    ax.set_title("Catalog Breakdown by Mood / Vibe", fontsize=13, weight="bold", pad=12)
    ax.set_ylabel("Movie Count", fontsize=10, labelpad=8)
    plt.xticks(rotation=28, ha="right")
    plt.tight_layout()
    return fig

def plot_top_directors(df):
    """Plots top directors by count in dataset."""
    counts = Counter(df["director"]).most_common(7)
    labels = [c[0] for c in reversed(counts)]
    values = [c[1] for c in reversed(counts)]

    fig, ax = plt.subplots(figsize=(8, 4.5), dpi=100)
    apply_cinema_style(fig, ax)

    bars = ax.barh(labels, values, color="#d97706", alpha=0.92, edgecolor="#fbbf24", linewidth=1.2)
    ax.bar_label(bars, padding=5, color="#ffffff", fontsize=9.5, weight="bold")
    ax.set_title("Most Featured Directors", fontsize=13, weight="bold", pad=12)
    ax.set_xlabel("Number of Films", fontsize=10, labelpad=8)
    plt.tight_layout()
    return fig
