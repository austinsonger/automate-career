import asyncio
import re
from playwright.async_api import Playwright, async_playwright, expect


async def run(playwright: Playwright) -> None:
    browser = await playwright.chromium.launch(headless=False)
    context = await browser.new_context()
    await page7.get_by_label("First Name").click()
    await page7.get_by_label("First Name").fill("Austiin")
    await page7.get_by_label("First Name").press("ArrowLeft")
    await page7.get_by_label("First Name").fill("Austin")
    await page7.get_by_label("Last Name").click()
    await page7.get_by_label("Last Name").fill("Songer")
    await page7.get_by_label("Email").click()
    await page7.get_by_label("Email").fill("career@songer.me")
    await page7.get_by_label("Phone").click()
    await page7.get_by_label("Phone").fill("708-796-3124")
    await page7.get_by_label("Location (City)*").fill("Oak Park")
    await page7.get_by_role("option", name="Oak Park, Illinois, United").click()
    await page7.get_by_label("Resume/CV*").get_by_role("button", name="Attach").click()
    await page7.get_by_label("Resume/CV*").get_by_role("button", name="Attach").set_input_files("2024-DEC-SongerResume.pdf")
    await page7.get_by_label("LinkedIn Profile").click()
    await page7.get_by_label("Toggle flyout").first.click()
    await page7.get_by_text("Are you legally authorized to").click()
    await page7.get_by_label("Toggle flyout").first.click()
    await page7.get_by_text("Will you now or in the future").click()
    await page7.get_by_label("Toggle flyout").nth(1).click()
    await page7.get_by_role("option", name="No").click()
    await page7.get_by_text("Have you been employed by").click()
    await page7.get_by_label("Toggle flyout").nth(2).click()
    await page7.get_by_role("option", name="No").click()
    await page7.get_by_label("By clicking this box and").check()

    # ---------------------
    await context.close()
    await browser.close()


async def main() -> None:
    async with async_playwright() as playwright:
        await run(playwright)


asyncio.run(main())
