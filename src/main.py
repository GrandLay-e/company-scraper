from functions import *
from IDS import *
from SELECTORS import *
from CONST import *
from apply import *

def main():
    """
    Main function to scrape company data and save it to SQLite and JSON files.
    """
    companies = Companies([])  # Initialize an empty Companies object
    logger.info("Starting the company scraping process...")
    driver = init_driver()
    if not driver:
        # If driver initialization fails, log the error and exit
        logger.error("Failed to initialize the web driver. Exiting.")
        exit(1)

    get_url(driver, COMPANIES_URL)
    time.sleep(2)
    find_and_click(driver, 1)
    find_and_click(driver, 3)
    find_and_click(driver, 4)
    tpage = driver.current_url
    number_of_pages = get_number_of_pages(driver, tpage)
    print(f"Number of pages found: {number_of_pages}")
    all_pages = get_all_pages_url(tpage, number_of_pages)
    for page in all_pages:
        logger.info(f"Processing page: {page}")
        blocks = get_companys_blocks(driver, page)
        for block in blocks:
            infos = get_companys_infos(driver, block)
            if infos:
                company = construct_company_object(infos)
                companies.companies.append(company)
                
                #Option to apply to the company
                # Uncomment the following lines to enable application functionality and add the filter conditions you need
                # try:
                #     if company.location == "Paris" and company.spontane == "Oui" and "Logiciels" in company.domain:
                #         driver_for_apply = init_driver()
                #         if not driver_for_apply:
                #             logger.error("Failed to initialize the web driver for application. Skipping application process.")
                #             continue

                #         connect(driver_for_apply, MAIL, PASSWORD)
                #         time.sleep(2)
                #         get_url(driver_for_apply, company.url_wtj)
                #         time.sleep(2)
                #         if not find_and_click(driver_for_apply, 20, company.name):
                #             logger.error(f"Applying button not found for {company.name}. Skipping application.")
                #             continue
                #         apply_to_company(company, driver)
                # except Exception as e:
                #     logger.error(f"An error occurred while applying to {company.name}: {e}")
                #     continue

            time.sleep(1)
    if len(companies.companies) > 0:
        logger.info(f"Total companies found: {len(companies.companies)}")
        # Save the companies data to SQLite and JSON files
        try:
            saved = True
            companies.save_companies_to_sqlite(DB_FILE)
            companies.save_companies_to_json(JSON_FILE)
            logger.info(f"Companies data saved to {DB_FILE} and {JSON_FILE}")
        except FileExistsError or FileNotFoundError :
            logger.error(f"Error saving companies data to files: {DB_FILE} or {JSON_FILE}. Please check the file paths.")
        except Exception as e:
            logger.error(f"An unexpected error occurred while saving companies data: {e}")
        if not saved:
            logger.error("Saved companies data to defines files failed. Saving it in othet files data.db and data.json")
            companies.save_companies_to_sqlite("data.db")
            companies.save_companies_to_json("data.json")
    else:
        logger.info("No companies found to save.")

    driver.quit()
    logger.info("Company scraping process completed successfully.")

if __name__ == "__main__":
    main()