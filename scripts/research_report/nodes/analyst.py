"""Data Analyst node — extracts structured data from raw search results.

Teaches: state accumulation with reducers, structured output for analysis.
"""

from scripts.research_report.config import get_llm
from scripts.research_report.models import DataAnalysis, ResearchState

ANALYST_SYSTEM_PROMPT = """\
You are a data analyst who extracts quantitative insights from research.

Given raw search results, produce:
1. **key_findings**: 5-10 concise bullet-point findings backed by the data.
2. **data_points**: A list of dicts with extractable quantitative facts
   (e.g. {{"metric": "market_share", "entity": "Company A", "value": 35, "unit": "%"}}).
3. **chart_specs**: 2-4 chart specifications. For each chart, choose the best type
   (bar, horizontal_bar, line, pie, scatter, heatmap) and provide real data extracted
   from the research. The data must use the correct format:
   - bar / horizontal_bar / line: {{"labels": [...], "values": [...]}}
   - pie: {{"labels": [...], "sizes": [...]}}
   - scatter: {{"x": [...], "y": [...]}}
   - heatmap: {{"labels": [...], "matrix": [[...]]}}
4. **summary_table**: A table with {{"columns": ["Col1", "Col2", ...], "rows": [["val", ...], ...]}}.

Use ONLY data that appears in or can be reasonably inferred from the search results.
Assign each chart_spec a `section` field matching the report section it belongs to.
"""


def data_analyst(state: ResearchState) -> dict:
    """Analyse search results and extract structured data for charts/tables."""
    llm = get_llm().with_structured_output(DataAnalysis, method="function_calling")

    # Build a digest of all search results grouped by section
    results_by_section: dict[str, list[str]] = {}
    for r in state["search_results"]:
        results_by_section.setdefault(r.section, []).append(
            f"[{r.title}]({r.url})\n{r.content}"
        )

    digest = "\n\n".join(
        f"## {section}\n" + "\n---\n".join(snippets)
        for section, snippets in results_by_section.items()
    )

    analysis = llm.invoke([
        {"role": "system", "content": ANALYST_SYSTEM_PROMPT},
        {"role": "user", "content": f"Analyse these research results:\n\n{digest}"},
    ])

    print(f"  ✓ Extracted {len(analysis.key_findings)} findings, "
          f"{len(analysis.chart_specs)} chart specs")
    return {
        "analysis": analysis,
        "status": "analyzed",
    }
