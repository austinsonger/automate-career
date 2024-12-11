# Consolidated Code

## File: /workspaces/automate-career/config.py

```# Constants
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

## File: /workspaces/automate-career/merge.py

```import os

def create_markdown_from_directory(root_directory, output_markdown):
    """
    Walks through a directory and subdirectories, extracting code from all files
    and creating a markdown file that consolidates all the code.

    Parameters:
    root_directory (str): The root directory to traverse.
    output_markdown (str): The path to the output markdown file.
    """
    with open(output_markdown, 'w', encoding='utf-8') as markdown_file:
        # Write header to markdown file
        markdown_file.write("# Consolidated Code\n\n")

        for dirpath, _, filenames in os.walk(root_directory):
            if '/virtual/' in dirpath:
                continue

            for filename in filenames:
                file_path = os.path.join(dirpath, filename)

                # Skip files that are not code (you can customize this filter)
                if not filename.endswith(('.py', '.js', '.html', '.css', '.java', '.cpp', '.txt')):
                    continue

                markdown_file.write(f"## File: {file_path}\n\n```")

                try:
                    with open(file_path, 'r', encoding='utf-8') as code_file:
                        markdown_file.write(code_file.read())
                except Exception as e:
                    markdown_file.write(f"Error reading file: {e}")

                markdown_file.write("\n````\n\n")

if __name__ == "__main__":
    root_dir = "/workspaces/automate-career"  # Replace with your root directory path
    output_file = "output.md"  # Replace with your desired output file path

    create_markdown_from_directory(root_dir, output_file)
    print(f"Markdown file created at {output_file}")

````

## File: /workspaces/automate-career/main.py

```import pandas as pd
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

````

## File: /workspaces/automate-career/utils/yaml_loader.py

```import yaml

def load_applicant_data(filepath):
    """Load applicant data from a YAML file."""
    with open(filepath, 'r') as file:
        data = yaml.safe_load(file)
    return data

````

## File: /workspaces/automate-career/utils/__init__.py

```
````

## File: /workspaces/automate-career/utils/browser.py

```from playwright.async_api import async_playwright

async def init_browser():
    """Initialize and return a Playwright browser and page."""
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=False)
    page = await browser.new_page()
    return playwright, browser, page

````

## File: /workspaces/automate-career/handlers/__init__.py

```from .lever import handle_lever_application
from .workable import handle_workable_application
from .bamboohr import handle_bamboohr_application


````

## File: /workspaces/automate-career/handlers/jobvite.py

```async def handle_lever_application(page, data):
    try:
        await page.fill('input[name="name"]', data["applicant"]["name"])
        await page.fill('input[name="email"]', data["applicant"]["email"])
        await page.fill('input[name="phone"]', data["applicant"]["phone"])
        await page.set_input_files('input[name="resume"]', data["applicant"]["resume_path"])
        await page.click('button[type="submit"]')
        await asyncio.sleep(2)
        print("Application submitted successfully on Lever.")
    except Exception as e:
        print(f"Error on Lever: {e}")

````

## File: /workspaces/automate-career/handlers/applytojob.py

```async def handle_lever_application(page, data):
    try:
        await page.fill('input[name="name"]', data["applicant"]["name"])
        await page.fill('input[name="email"]', data["applicant"]["email"])
        await page.fill('input[name="phone"]', data["applicant"]["phone"])
        await page.set_input_files('input[name="resume"]', data["applicant"]["resume_path"])
        await page.click('button[type="submit"]')
        await asyncio.sleep(2)
        print("Application submitted successfully on Lever.")
    except Exception as e:
        print(f"Error on Lever: {e}")

````

## File: /workspaces/automate-career/handlers/workable.py

```async def handle_lever_application(page, data):
    try:
        await page.fill('input[name="name"]', data["applicant"]["name"])
        await page.fill('input[name="email"]', data["applicant"]["email"])
        await page.fill('input[name="phone"]', data["applicant"]["phone"])
        await page.set_input_files('input[name="resume"]', data["applicant"]["resume_path"])
        await page.click('button[type="submit"]')
        await asyncio.sleep(2)
        print("Application submitted successfully on Lever.")
    except Exception as e:
        print(f"Error on Lever: {e}")

````

## File: /workspaces/automate-career/handlers/breezy.py

```async def handle_lever_application(page, data):
    try:
        await page.fill('input[name="name"]', data["applicant"]["name"])
        await page.fill('input[name="email"]', data["applicant"]["email"])
        await page.fill('input[name="phone"]', data["applicant"]["phone"])
        await page.set_input_files('input[name="resume"]', data["applicant"]["resume_path"])
        await page.click('button[type="submit"]')
        await asyncio.sleep(2)
        print("Application submitted successfully on Lever.")
    except Exception as e:
        print(f"Error on Lever: {e}")

````

## File: /workspaces/automate-career/handlers/bamboohr.py

```async def handle_lever_application(page, data):
    try:
        await page.fill('input[name="name"]', data["applicant"]["name"])
        await page.fill('input[name="email"]', data["applicant"]["email"])
        await page.fill('input[name="phone"]', data["applicant"]["phone"])
        await page.set_input_files('input[name="resume"]', data["applicant"]["resume_path"])
        await page.click('button[type="submit"]')
        await asyncio.sleep(2)
        print("Application submitted successfully on Lever.")
    except Exception as e:
        print(f"Error on Lever: {e}")

````

## File: /workspaces/automate-career/handlers/greenhouse.py

```async def handle_lever_application(page, data):
    try:
        await page.fill('input[name="name"]', data["applicant"]["name"])
        await page.fill('input[name="email"]', data["applicant"]["email"])
        await page.fill('input[name="phone"]', data["applicant"]["phone"])
        await page.set_input_files('input[name="resume"]', data["applicant"]["resume_path"])
        await page.click('button[type="submit"]')
        await asyncio.sleep(2)
        print("Application submitted successfully on Lever.")
    except Exception as e:
        print(f"Error on Lever: {e}")

````

## File: /workspaces/automate-career/handlers/lever.py

```async def handle_lever_application(page, data):
    try:
        await page.fill('input[name="name"]', data["applicant"]["name"])
        await page.fill('input[name="email"]', data["applicant"]["email"])
        await page.fill('input[name="phone"]', data["applicant"]["phone"])
        await page.set_input_files('input[name="resume"]', data["applicant"]["resume_path"])
        await page.click('button[type="submit"]')
        await asyncio.sleep(2)
        print("Application submitted successfully on Lever.")
    except Exception as e:
        print(f"Error on Lever: {e}")

````

