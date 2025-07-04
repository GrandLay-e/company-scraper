from datetime import datetime
import IDS
from CONST import *
from functions import *
from SELECTORS import *

def liste_postule(file, company_name):
    with open(file, "a") as f:
        f.write(f"{company_name}\n")
    
def get_applied(file):
    try:
        with open(file, "r") as f:
            return f.readlines()
    except (FileNotFoundError, UnicodeDecodeError):
        # If the file does not exist, create it and return an empty list
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


# Write email
def connect(driver):
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
    time.sleep(2)


def apply_to_company(company):
    applied = get_applied(APPLIED)
    if company.name + "\n" in applied:
        print(f"{company.name} has already been applied to.")
        return

    print(f"Applying to {company.name}...")
    link = company.url_wtj
    job_link = link.split("?")[0] + "/jobs?" + link.split("?")[1]
    get_url(driver, job_link)
    time.sleep(1)

    if not find_and_click(driver, 20, company.name):
        return

    cover_letter_area = find_element(driver, 21)
    if not cover_letter_area or not write_cover_letter(cover_letter_area, company.name):
        logger.error(f"Message textarea not found or error writing for {company.name}.")
        return

    if not find_and_click(driver, 22, company.name):
        return

    time.sleep(2)

    if not find_and_click(driver, 23, company.name):
        return

    if not find_and_click(driver, 25, company.name):
        return

    print(f"Application successfully submitted for {company.name}.")
    liste_postule(APPLIED, company.name)

    time.sleep(2)

if __name__ == "__main__":
    driver = init_driver()
    get_url(driver, "https://www.welcometothejungle.com/fr/signin")
    time.sleep(2)

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
