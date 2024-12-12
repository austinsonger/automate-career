import asyncio
import pandas as pd
import yaml
import traceback
from playwright.async_api import async_playwright


# Function to load YAML data
async def load_applicant_data(yaml_file):
    loop = asyncio.get_event_loop()
    with open(yaml_file, 'r') as file:
        data = await loop.run_in_executor(None, yaml.safe_load, file)
    return data

async def load_job_urls(excel_file):
    df = await asyncio.to_thread(pd.read_excel, excel_file)
    # Assuming the Excel sheet has columns "Company" and "JobID"
    jobs = [{"company": row["Company"], "job_id": row["JobID"]} for _, row in df.iterrows()]
    return jobs

async def handle_level_application(page, applicant_data, company, job_id, delay=2):
    try:
        # Build the job URL dynamically
        job_url = f"https://jobs.lever.co/{company}/{job_id}"
        await page.goto(job_url)

        # Wait for the page to load
        await page.wait_for_selector('form#application-form')

        # Fill out the application form
        await page.get_by_label('Full name').fill(applicant_data["full_name"])
        await page.get_by_label('Email').fill(applicant_data["email"])
        await page.get_by_label('Phone').fill(applicant_data["phone"])
        await page.get_by_label('Current location').fill(applicant_data["location"])
        await page.get_by_label('Current company').fill(applicant_data["current_company"])

        # Upload the resume
        await page.set_input_files('input[name="resume"]', applicant_data["resume_path"])

        # Fill the additional information textarea
        await page.get_by_label('Additional information').fill(applicant_data.get("additional_info", "N/A"))


        # Submit the application
        await page.click('#btn-submit')

        await asyncio.sleep(delay)  # Optional delay to ensure submission is complete
        print(f"Application submitted successfully for company {company}, job ID {job_id}.")
    except Exception as e:
        print(f"Error on Lever for company {company}, job ID {job_id}: {e}")
        traceback.print_exc()

# Main function
async def main():
    # Load applicant data from YAML
    applicant_data = await load_applicant_data("applicant/applicant_data.yaml")
    applicant_data["resume_path"] = "resume.pdf"  # Add dynamic path for the resume

    job_list = await load_job_urls("jobs/JobURLs.xlsx")
    job_list = load_job_urls("jobs/JobURLs.xlsx")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)  # Set headless=True for non-UI execution
        page = await browser.new_page()

        # Loop through jobs and apply for each
        for job in job_list:
            await handle_level_application(page, applicant_data, job["company"], job["job_id"], delay=1)

        await browser.close()

# Run the script
asyncio.run(main())