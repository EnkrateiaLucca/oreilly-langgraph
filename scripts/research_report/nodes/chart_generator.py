"""Chart Generator node — renders matplotlib charts from structured specs.

Teaches: pure Python nodes (no LLM call), side effects, try/except resilience.

The LLM in the analyst node specifies *what* to chart via ChartSpec;
this node handles *how* using deterministic matplotlib code.
"""

import base64
import io

import matplotlib
matplotlib.use("Agg")  # non-interactive backend for headless rendering
import matplotlib.pyplot as plt
import seaborn as sns

from scripts.research_report.models import ChartData, ChartSpec, ResearchState

sns.set_theme(style="whitegrid", palette="muted")

# Colour palette for consistent branding
COLORS = ["#2c3e50", "#3498db", "#e74c3c", "#2ecc71", "#f39c12",
          "#9b59b6", "#1abc9c", "#e67e22", "#34495e", "#16a085"]


def _render_bar(spec: ChartSpec) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(10, 5))
    labels = spec.data.get("labels", [])
    values = spec.data.get("values", [])
    bars = ax.bar(labels, values, color=COLORS[: len(labels)])
    ax.set_title(spec.title, fontsize=14, fontweight="bold")
    ax.set_ylabel("")
    # Add value labels on bars
    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                f"{val}", ha="center", va="bottom", fontsize=9)
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    return fig


def _render_horizontal_bar(spec: ChartSpec) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(10, 5))
    labels = spec.data.get("labels", [])
    values = spec.data.get("values", [])
    y_pos = range(len(labels))
    ax.barh(y_pos, values, color=COLORS[: len(labels)])
    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels)
    ax.set_title(spec.title, fontsize=14, fontweight="bold")
    for i, val in enumerate(values):
        ax.text(val, i, f" {val}", va="center", fontsize=9)
    plt.tight_layout()
    return fig


def _render_line(spec: ChartSpec) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(10, 5))
    labels = spec.data.get("labels", [])
    values = spec.data.get("values", [])
    ax.plot(labels, values, marker="o", linewidth=2, color=COLORS[0])
    ax.fill_between(labels, values, alpha=0.1, color=COLORS[0])
    ax.set_title(spec.title, fontsize=14, fontweight="bold")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    return fig


def _render_pie(spec: ChartSpec) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(8, 8))
    labels = spec.data.get("labels", [])
    sizes = spec.data.get("sizes", [])
    ax.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=140,
           colors=COLORS[: len(labels)])
    ax.set_title(spec.title, fontsize=14, fontweight="bold")
    plt.tight_layout()
    return fig


def _render_scatter(spec: ChartSpec) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(10, 6))
    x = spec.data.get("x", [])
    y = spec.data.get("y", [])
    ax.scatter(x, y, color=COLORS[0], s=80, alpha=0.7, edgecolors="white")
    ax.set_title(spec.title, fontsize=14, fontweight="bold")
    plt.tight_layout()
    return fig


def _render_heatmap(spec: ChartSpec) -> plt.Figure:
    import numpy as np
    fig, ax = plt.subplots(figsize=(10, 8))
    labels = spec.data.get("labels", [])
    matrix = np.array(spec.data.get("matrix", [[]]))
    sns.heatmap(matrix, annot=True, fmt=".1f", xticklabels=labels,
                yticklabels=labels, cmap="YlOrRd", ax=ax)
    ax.set_title(spec.title, fontsize=14, fontweight="bold")
    plt.tight_layout()
    return fig


_RENDERERS = {
    "bar": _render_bar,
    "horizontal_bar": _render_horizontal_bar,
    "line": _render_line,
    "pie": _render_pie,
    "scatter": _render_scatter,
    "heatmap": _render_heatmap,
}


def _fig_to_base64(fig: plt.Figure) -> str:
    """Encode a matplotlib figure as a base64 PNG string."""
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight")
    buf.seek(0)
    encoded = base64.b64encode(buf.read()).decode("utf-8")
    plt.close(fig)
    return encoded


def chart_generator(state: ResearchState) -> dict:
    """Generate charts from the analyst's ChartSpec list — no LLM needed."""
    analysis = state.get("analysis")
    if not analysis or not analysis.chart_specs:
        print("  ⚠ No chart specs to render")
        return {"charts": [], "status": "charts_generated"}

    charts: list[ChartData] = []
    for spec in analysis.chart_specs:
        renderer = _RENDERERS.get(spec.chart_type)
        if not renderer:
            print(f"  ⚠ Unknown chart type '{spec.chart_type}', skipping")
            continue
        try:
            fig = renderer(spec)
            b64 = _fig_to_base64(fig)
            charts.append(ChartData(
                title=spec.title,
                base64_png=b64,
                description=spec.description,
                section=spec.section,
            ))
            print(f"  ✓ Rendered {spec.chart_type} chart: {spec.title}")
        except Exception as e:
            print(f"  ⚠ Failed to render '{spec.title}': {e}")
            plt.close("all")

    return {"charts": charts, "status": "charts_generated"}
