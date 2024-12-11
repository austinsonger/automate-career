# Jobwright

Required:
- https://playwright.dev


## To-Do List

- [ ] Identify and test CSS selectors, XPath, or text selectors for each target job application platform.
- [ ] Implement robust and dynamic selector handling to manage variations and updates in web forms.



# Code

## File: /workspaces/jobwright/config.py

```python
JOB_APPLICATION_PLATFORMS = {
    "lever": r"https://jobs.lever.co/.+/",
    "workable": r"https://apply.workable.com/.+/",
    "breezy": r"https://.+\.breezy\.hr",
    "applytojob": r"https://.+\.applytojob\.com",
    "bamboohr": r"https://.+\.bamboohr\.com",
    "greenhouse": r"https://boards.greenhouse.io/.+/",
    "jobvite": r"https://jobs.jobvite.com/.+/",
}

RESUME_PATH = "/path/to/resume.pdf"
````


## File: /workspaces/jobwright/main.py

```python
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

    applicant_data = load_applicant_data('applicant/') 

    for job_url in job_urls:
        print(f"Applying to: {job_url}")
        await apply_to_job(job_url, applicant_data)

if __name__ == "__main__":
    asyncio.run(main())

````

## File: /workspaces/jobwright/utils/yaml_loader.py

```python
import yaml

def load_applicant_data(filepath):
    """Load applicant data from a YAML file."""
    with open(filepath, 'r') as file:
        data = yaml.safe_load(file)
    return data

````


## File: /workspaces/jobwright/utils/browser.py

```python
from playwright.async_api import async_playwright

async def init_browser():
    """Initialize and return a Playwright browser and page."""
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=False)
    page = await browser.new_page()
    return playwright, browser, page

````

## File: /workspaces/jobwright/handlers/__init__.py

```python
from .lever import handle_lever_application
from .workable import handle_workable_application
from .bamboohr import handle_bamboohr_application


````

## File: /workspaces/jobwright/handlers/jobvite.py

```python
async def handle_jobinvite_application(page, data):
    try:
        await page.fill('input[name="name"]', data["applicant"]["name"])
        await page.fill('input[name="email"]', data["applicant"]["email"])
        await page.fill('input[name="phone"]', data["applicant"]["phone"])
        await page.set_input_files('input[name="resume"]', data["applicant"]["resume_path"])
        await page.click('button[type="submit"]')
        await asyncio.sleep(2)
        print("Application submitted successfully on Jobinvite.")
    except Exception as e:
        print(f"Error on Jobinvite: {e}")

````


