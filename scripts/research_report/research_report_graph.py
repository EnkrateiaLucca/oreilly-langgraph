"""LangGraph Research Report Generator — main graph definition.

This module wires all nodes into a StateGraph with conditional edges,
parallel fan-out, and quality loops.  It can be:
  - Imported: `from scripts.research_report.research_report_graph import graph`
  - Run as CLI: `python -m scripts.research_report.research_report_graph "Your Topic Here"`

Graph topology:
                                    ┌──────────────────────┐
  START → research_planner ─┬─→ web_researcher → check_sufficiency ─┬─→ data_analyst → chart_generator
                            │                        ↑ (loop)       │
                            └─→ screenshot_collector ───────────────┘
                                                                          ↓
                              ┌──── web_researcher (loop) ←──┐   report_writer → check_quality ─→ report_compiler → END
                              │                               │                     │
                              └──── data_analyst (loop) ←─────┘─────────────────────┘
"""

import argparse
import sys
from typing import Literal

from dotenv import load_dotenv
from langgraph.graph import END, START, StateGraph

from scripts.research_report.models import ResearchState
from scripts.research_report.nodes import (
    chart_generator,
    data_analyst,
    report_compiler,
    report_writer,
    research_planner,
    screenshot_collector,
    web_researcher,
)

load_dotenv()


# ---------------------------------------------------------------------------
# Conditional edge functions
# ---------------------------------------------------------------------------

def check_research_sufficiency(state: ResearchState) -> Literal["data_analyst", "web_researcher"]:
    """After web_researcher: do we have enough search results?

    Routes back to web_researcher if we have very few results and haven't
    exceeded iteration limits.  Otherwise proceeds to data_analyst.
    """
    results_count = len(state.get("search_results", []))
    iteration = state.get("iteration_count", 0)
    max_iter = state.get("max_iterations", 3)

    if results_count < 5 and iteration < max_iter:
        print(f"  ↻ Only {results_count} results — researching more...")
        return "web_researcher"
    return "data_analyst"


def check_quality(state: ResearchState) -> Literal["report_compiler", "web_researcher", "data_analyst"]:
    """After report_writer: route based on the quality self-review.

    The report_writer sets `status` to one of:
      'compiler'        → report is ready, proceed to final assembly
      'web_researcher'  → sections need more source material
      'data_analyst'    → need more quantitative analysis/charts

    Safety: force finish if we've hit max_iterations.
    """
    iteration = state.get("iteration_count", 0)
    max_iter = state.get("max_iterations", 3)

    if iteration >= max_iter:
        print(f"  ⚑ Max iterations ({max_iter}) reached — finishing report")
        return "report_compiler"

    status = state.get("status", "compiler")
    route_map = {
        "compiler": "report_compiler",
        "web_researcher": "web_researcher",
        "data_analyst": "data_analyst",
    }
    dest = route_map.get(status, "report_compiler")
    if dest != "report_compiler":
        print(f"  ↻ Quality loop → {dest}")
    return dest


# ---------------------------------------------------------------------------
# Build the graph
# ---------------------------------------------------------------------------

def build_graph() -> StateGraph:
    """Construct and compile the research report StateGraph."""
    builder = StateGraph(ResearchState)

    # --- Add nodes ---
    builder.add_node("research_planner", research_planner)
    builder.add_node("web_researcher", web_researcher)
    builder.add_node("screenshot_collector", screenshot_collector)
    builder.add_node("data_analyst", data_analyst)
    builder.add_node("chart_generator", chart_generator)
    builder.add_node("report_writer", report_writer)
    builder.add_node("report_compiler", report_compiler)

    # --- Edges ---

    # 1. START → planner
    builder.add_edge(START, "research_planner")

    # 2. Planner fans out to researcher AND screenshot collector (parallel)
    builder.add_edge("research_planner", "web_researcher")
    builder.add_edge("research_planner", "screenshot_collector")

    # 3. After researcher: conditional — enough data or loop?
    builder.add_conditional_edges(
        "web_researcher",
        check_research_sufficiency,
        ["data_analyst", "web_researcher"],
    )

    # 4. Screenshots join at data_analyst
    builder.add_edge("screenshot_collector", "data_analyst")

    # 5. Linear: analyst → chart generator → report writer
    builder.add_edge("data_analyst", "chart_generator")
    builder.add_edge("chart_generator", "report_writer")

    # 6. After report writer: quality routing (3 possible destinations)
    builder.add_conditional_edges(
        "report_writer",
        check_quality,
        ["report_compiler", "web_researcher", "data_analyst"],
    )

    # 7. Compiler → END
    builder.add_edge("report_compiler", END)

    return builder.compile()


# Module-level graph instance for easy import
graph = build_graph()


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Generate a structured research report using LangGraph"
    )
    parser.add_argument("topic", help="Research topic (e.g. 'AI Coding Assistants in 2026')")
    parser.add_argument("--max-iterations", type=int, default=3,
                        help="Max quality-loop iterations (default: 3)")
    args = parser.parse_args()

    print(f"\n{'='*60}")
    print(f"  Research Report Generator")
    print(f"  Topic: {args.topic}")
    print(f"{'='*60}\n")

    result = graph.invoke({
        "topic": args.topic,
        "research_plan": None,
        "search_results": [],
        "analysis": None,
        "charts": [],
        "screenshots": [],
        "report_sections": {},
        "final_report_html": "",
        "iteration_count": 0,
        "max_iterations": args.max_iterations,
        "status": "",
    })

    print(f"\n{'='*60}")
    print(f"  ✓ Report generation complete!")
    print(f"  Status: {result.get('status')}")
    print(f"  Sections: {list(result.get('report_sections', {}).keys())}")
    print(f"  Charts: {len(result.get('charts', []))}")
    print(f"  Screenshots: {len(result.get('screenshots', []))}")
    print(f"  Check the output/ directory for HTML (and optional PDF)")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
