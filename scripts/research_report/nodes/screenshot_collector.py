"""Screenshot Collector node — captures web page screenshots with Playwright.

Teaches: parallel execution (this node runs alongside web_researcher).

Uses playwright.sync_api so the graph can be invoked with `graph.invoke()`.
For async contexts (e.g. FastAPI), swap to `async_playwright` + `async def`.
"""

import base64

from scripts.research_report.models import ResearchState, ScreenshotData

SCREENSHOT_TIMEOUT_MS = 15_000
VIEWPORT = {"width": 1440, "height": 900}


def screenshot_collector(state: ResearchState) -> dict:
    """Take screenshots of URLs from the research plan using headless Chromium."""
    plan = state.get("research_plan")
    if not plan or not plan.urls_to_screenshot:
        print("  ⚠ No URLs to screenshot")
        return {"screenshots": []}

    screenshots: list[ScreenshotData] = []

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("  ⚠ Playwright not installed — skipping screenshots. "
              "Run: pip install playwright && playwright install chromium")
        return {"screenshots": []}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        for url in plan.urls_to_screenshot[:5]:  # cap at 5
            try:
                page = browser.new_page(viewport=VIEWPORT)
                page.goto(url, timeout=SCREENSHOT_TIMEOUT_MS)
                page.wait_for_load_state("networkidle", timeout=10_000)

                img_bytes = page.screenshot(full_page=False)
                b64 = base64.b64encode(img_bytes).decode("utf-8")

                screenshots.append(ScreenshotData(
                    url=url,
                    base64_png=b64,
                    caption=page.title() or url,
                ))
                print(f"  ✓ Screenshot: {url}")
                page.close()
            except Exception as e:
                print(f"  ⚠ Screenshot failed for {url}: {e}")

        browser.close()

    return {"screenshots": screenshots}
