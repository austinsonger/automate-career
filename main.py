import pandas as pd
import asyncio
from utils.browser import init_browser
from config import JOB_APPLICATION_PLATFORMS
from handlers import handle_lever_application, handle_workable_application, handle_bamboohr_application  # and others
from utils.yaml_loader import load_applicant_data

async def apply_to_job(job_url, data):
    """Determine the platform and handle the job application."""
    playwright, browser, page = await init_browser()
    try:
        await page.goto(job_url)
        await asyncio.sleep(2)  
        for platform, pattern in JOB_APPLICATION_PLATFORMS.items():
            if re.match(pattern, job_url):
                print(f"Matched platform: {platform}")
                handler_function = globals().get(f"handle_{platform}_application")
                if handler_function:
                    await handler_function(page, data)
                else:
                    print(f"No handler implemented for platform: {platform}")
                break
        else:
            print(f"Unsupported platform for URL: {job_url}")
    except Exception as e:
        print(f"An error occurred while applying: {e}")
    finally:
        await browser.close()
        await playwright.stop()

async def main():
    
    df = pd.read_excel('jobs/jobsURL.xlsx') 
    job_urls = df['Job URLs'].tolist()

    applicant_data = load_applicant_data('applicant/applicant_data.yaml')  # Ensure the path to YAML file is correct

    for job_url in job_urls:
        print(f"Applying to: {job_url}")
        await apply_to_job(job_url, applicant_data)

if __name__ == "__main__":
    asyncio.run(main())
