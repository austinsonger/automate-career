async def handle_breezy_application(page, data):
    try:
        await page.fill('input[name="name"]', data["applicant"]["name"])
        await page.fill('input[name="email"]', data["applicant"]["email"])
        await page.fill('input[name="phone"]', data["applicant"]["phone"])
        await page.set_input_files('input[name="resume"]', data["applicant"]["resume_path"])
        await page.click('button[type="submit"]')
        await asyncio.sleep(2)
        print("Application submitted successfully on breezy.")
    except Exception as e:
        print(f"Error on breezy: {e}")
