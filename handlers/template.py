import asyncio
import pandas as pd
import yaml
from playwright.async_api import async_playwright

# Function to load YAML data
def load_applicant_data(yaml_file):
    with open(yaml_file, 'r') as file:
        data = yaml.safe_load(file)
    return data

# Function to load job details from Excel
def load_job_urls(excel_file):
    # Read the Excel file into a DataFrame
    df = pd.read_excel(excel_file)
    # Assuming the Excel sheet has columns "Company" and "JobID"
    jobs = [{"company": row["Company"], "job_id": row["JobID"]} for _, row in df.iterrows()]
    return jobs

# Function to handle PLATFORM application
async def handle_PLACEHOLDER_application(page, applicant_data, company, job_id):
    try:
        # Build the job URL dynamically
        job_url = f"https://URL_PLACEHOLDER/{company}/j/{job_id}/"
        await page.goto(job_url)

        # Click "Apply for this job" button
        await page.get_by_role('button', { 'name': 'Apply for this job' }).click()

        # Fill out the application form
        await page.get_by_label('First name').fill(applicant_data["first_name"])
        await page.get_by_label('First name').press('Tab')
        await page.get_by_label('Last name').fill(applicant_data["last_name"])
        await page.get_by_label('Email').fill(applicant_data["email"])
        await page.get_by_label('*Phone+1United States+1United').fill(applicant_data["phone"])
        await page.get_by_label('Address 1').fill(applicant_data["address"])
        await page.get_by_label('Province / State (abbreviated)').fill(applicant_data["state"])

        # Select "United States" as the country
        await page.get_by_placeholder('Select an option…').click()
        await page.get_by_role('option', { 'name': applicant_data["country"] }).locator('div').first().click()

        # Fill out the postal code
        await page.get_by_label('Postal / Zip Code').fill(applicant_data["zip_code"])

        # Upload the resume
        await page.get_by_role('button', { 'name': 'Upload a file' }).click()
        await page.get_by_label('Resume').set_input_files(applicant_data["resume_path"])

        # Answer the radio button question
        await page.get_by_role('radio', { 
            'name': 'Are you legally entitled to work in United States ? YES',
            'exact': True
        }).click()

        # Fill the referral field
        await page.get_by_label('If you have been referred by').fill(applicant_data.get("referral", "N/A"))

        # Submit the application
        await page.click('button[type="submit"]')

        await asyncio.sleep(2)  # Optional delay to ensure submission is complete
        print(f"Application submitted successfully for company {company}, job ID {job_id}.")
    except Exception as e:
        print(f"Error on PLATFORM for company {company}, job ID {job_id}: {e}")

# Main function
async def main():
    # Load applicant data from YAML
    applicant_data = load_applicant_data("applicant/applicant_data.yaml")
    applicant_data["resume_path"] = "resume.pdf"  # Add dynamic path for the resume

    # Load job details from Excel
    job_list = load_job_urls("jobs/JobURLs.xlsx")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # Set headless=True for non-UI execution
        page = await browser.new_page()

        # Loop through jobs and apply for each
        for job in job_list:
            await handle_PLACEHOLDER_application(page, applicant_data, job["company"], job["job_id"])

        await browser.close()

# Run the script
asyncio.run(main())
