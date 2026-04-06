"""Report Compiler node — assembles everything into a self-contained HTML report.

Teaches: final node, Jinja2 templating, END edge.

Optionally generates a PDF via WeasyPrint (wrapped in try/except because
WeasyPrint requires system libraries that not all environments have).
"""

import datetime
import os
from pathlib import Path

import jinja2
import pandas as pd

from scripts.research_report.models import ResearchState

TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "templates"
OUTPUT_DIR = Path(__file__).resolve().parent.parent.parent.parent / "output"


def _build_summary_table_html(analysis) -> str:
    """Convert the analysis summary_table dict into styled HTML."""
    if not analysis or not analysis.summary_table:
        return ""

    table_data = analysis.summary_table
    columns = table_data.get("columns", [])
    rows = table_data.get("rows", [])
    if not columns or not rows:
        return ""

    df = pd.DataFrame(rows, columns=columns)
    styled = (
        df.style
        .set_table_styles([
            {"selector": "th", "props": [
                ("background-color", "#2c3e50"),
                ("color", "white"),
                ("padding", "10px 14px"),
                ("font-weight", "bold"),
                ("text-align", "left"),
            ]},
            {"selector": "td", "props": [
                ("padding", "8px 14px"),
                ("border-bottom", "1px solid #dee2e6"),
            ]},
            {"selector": "tr:nth-child(even)", "props": [
                ("background-color", "#f8f9fa"),
            ]},
        ])
        .hide(axis="index")
    )
    return styled.to_html()


def report_compiler(state: ResearchState) -> dict:
    """Assemble the final HTML report from all gathered materials."""
    plan = state["research_plan"]
    sections = state.get("report_sections", {})
    charts = state.get("charts", [])
    screenshots = state.get("screenshots", [])
    analysis = state.get("analysis")

    # Group charts by section
    charts_by_section: dict[str, list] = {}
    for chart in charts:
        charts_by_section.setdefault(chart.section, []).append(chart)

    # Build section data for the template
    template_sections = []
    for title, content in sections.items():
        template_sections.append({
            "title": title,
            "content": content,
            "charts": charts_by_section.get(title, []),
        })

    # Collect unique sources from search results
    seen_urls: set[str] = set()
    sources = []
    for r in state.get("search_results", []):
        if r.url and r.url not in seen_urls:
            seen_urls.add(r.url)
            sources.append({"title": r.title, "url": r.url})

    # Build summary table HTML
    summary_table_html = _build_summary_table_html(analysis)

    # Render Jinja2 template
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(str(TEMPLATE_DIR)),
        autoescape=jinja2.select_autoescape(["html"]),
    )
    template = env.get_template("report.html")

    html = template.render(
        title=plan.title,
        topic=state["topic"],
        generated_date=datetime.date.today().isoformat(),
        executive_summary=sections.get("Executive Summary", ""),
        summary_table=summary_table_html,
        sections=template_sections,
        screenshots=screenshots,
        sources=sources,
        key_findings=analysis.key_findings if analysis else [],
    )

    # Save HTML output
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    safe_name = "".join(c if c.isalnum() or c in "-_ " else "" for c in plan.title)
    safe_name = safe_name.strip().replace(" ", "-")[:80]
    html_path = OUTPUT_DIR / f"{safe_name}.html"
    html_path.write_text(html, encoding="utf-8")
    print(f"  ✓ Report saved: {html_path}")

    # Optional: PDF via WeasyPrint
    try:
        from weasyprint import HTML as WeasyHTML
        pdf_path = OUTPUT_DIR / f"{safe_name}.pdf"
        WeasyHTML(string=html).write_pdf(str(pdf_path))
        print(f"  ✓ PDF saved: {pdf_path}")
    except ImportError:
        print("  ℹ WeasyPrint not installed — skipping PDF. "
              "Install with: pip install weasyprint (requires cairo/pango system libs)")
    except Exception as e:
        print(f"  ⚠ PDF generation failed: {e}")

    return {
        "final_report_html": html,
        "status": "complete",
    }
