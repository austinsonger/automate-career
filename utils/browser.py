from playwright.async_api import async_playwright

async def init_browser():
    """Initialize and return a Playwright browser and page."""
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=False)
    page = await browser.new_page()
    return playwright, browser, page
