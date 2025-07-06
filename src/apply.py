from datetime import datetime
import IDS
from CONST import *
from functions import *
from SELECTORS import *

def add_applied_company(file, company_name):
    with open(file, "a") as f:
        f.write(f"{company_name}\n")
    
def get_applied(file):
    try:
        with open(file, "r") as f:
            return f.readlines()
    except (FileNotFoundError, UnicodeDecodeError):
        logger.warning(f"File {file} not found or cannot be read. Creating a new file.")
        # If the file does not exist, create it and return an empty list
    except Exception  as e:
        logger.error(f"An error occurred while reading the file {file}: {e}")
    with open(file, "w") as f:
        return []

def write_cover_letter(element, company_name):
    try:
        element.clear()
        element.send_keys(IDS.COVER_LETTER(
            date=datetime.today().strftime("%d/%m/%Y"),
            name=company_name,
            repository_link="https://github.com/grandlay-e/company-scraper"))
        logger.info(f"Cover letter written for {company_name}.")
        return True
    except Exception as e:
        logger.error(f"Error writing cover letter for {company_name}: {e}")
        return False

def connect(driver):
    get_url(driver, LOGIN_URL)

    email_input = find_element(driver, 18)
    if not email_input:
        logger.error("Email input field not found.")
        driver.quit()
        exit(1)
    email_input.send_keys(IDS.MAIL)

    # Write password
    password_input = find_element(driver, 19)
    if not password_input:
        logger.error("Password input field not found.")
        driver.quit()
        exit(1)
    password_input.send_keys(IDS.PASSWORD)

    # Click on the login button
    driver.find_element(By.CSS_SELECTOR, CSS_SELECTORS[17]).click()

def apply_to_company(driver,company, applied : list[str] = None):
    if company.name + "\n" in applied:
        print(f"{company.name} has already been applied to.")
        return

    print(f"Applying to {company.name}...")
    link = company.url_wtj
    job_link = urljoin(link.split("?")[0]+'/', "jobs")
    get_url(driver, job_link)
    if not find_and_click(driver, 20, company.name):
        return
    cover_letter_area = find_element(driver, 21)
    if not cover_letter_area or not write_cover_letter(cover_letter_area, company.name):
        logger.error(f"Message textarea not found or error writing for {company.name}.")
        return
    if not find_and_click(driver, 22, company.name):
        return
    if not find_and_click(driver, 23, company.name):
        return
    if not find_and_click(driver, 25, company.name):
        return

    logger.info(f"Application successfully submitted for {company.name}.")
    add_applied_company(APPLIED, company.name)

if __name__ == "__main__":
    driver = init_driver()

    connect(driver)

    # Get all companies from the JSON file
    cps = Companies([])
    data = cps.get_companies_from_json(JSON_FILE).companies
    if not data:
        logger.error("No companies found in the JSON file.")
        driver.quit()
        exit(1)

    # Filter companies based on location, spontaneity, and domain
    filtered_companies = [c for c in data if "Paris" in c.location and c.spontane == "Oui" and "Logiciels" in c.domain]

    # Check if there are companies to apply to
    if not filtered_companies:
        logger.info("No companies found to apply to.")
        driver.quit()
        exit(0)

    for company in filtered_companies:
        apply_to_company(company)

    driver.quit()
    # End of the script
