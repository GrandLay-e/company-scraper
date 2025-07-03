# -*- coding: utf-8 -*-

import tempfile
import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import StaleElementReferenceException

import time
import logging
from pathlib import Path

from SELECTORS import *
from Company import Company
from Companies import Companies

# Logger initialization
try:
    logging.basicConfig(
        filemode='w',
        filename= LOGGING_FILE,
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
    )
except FileNotFoundError:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
    )
logger = logging.getLogger(__name__)

def init_driver():
    """
    Initialize a Chrome WebDriver instance.

    Returns:
        webdriver.Chrome: The initialized Chrome WebDriver object.
        None: If initialization fails.
    """
    options = webdriver.ChromeOptions()
    try:
        return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    except Exception as e:
        logger.error(f"ERROR INITIALIZING THE WEBDRIVER, message : {e}")
        return None

    
def get_url(driver, url):
    """
    Load the specified URL using the provided WebDriver.

    Args:
        driver (webdriver.Chrome): The WebDriver instance.
        url (str): The URL to load.
    """
    try:
        driver.get(url)
    except Exception as e:
        logger.error(f"ERROR TRYING TO GET URL, CHECK YOUR URL : {e}")

def find_element(driver, selectors_key, number="one", timeout=10):
    """
    Find an element or elements by CSS selector with an explicit wait.

    Args:
        driver (webdriver.Chrome): The WebDriver instance.
        selectors_key (int): The key for the CSS selector.
        number (str): "one" for a single element, otherwise multiple.
        timeout (int): The maximum time to wait for the element(s) to be found.

    Returns:
        WebElement or list: The found element(s), or None if not found.
    """
    try:
        if number == "one":
            logger.info(f"Finding element with selector: {CSS_SELECTORS[selectors_key]}")
            return WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, CSS_SELECTORS[selectors_key]))
            )
        else:
            logger.info(f"Finding elements with selector: {CSS_SELECTORS[selectors_key]}")
            return WebDriverWait(driver, timeout).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, CSS_SELECTORS[selectors_key]))
            )
    except Exception as e:
        logger.error(f"ERROR FINDING ELEMENT, message : {e}")
        return None

def click_on_element(driver, element):
    """
    Click on the specified element using JavaScript.

    Args:
        driver (webdriver.Chrome): The WebDriver instance.
        element (WebElement): The element to click.
    """
    try:
        time.sleep(3)
        driver.execute_script("arguments[0].click();", element)
        return True
    except Exception as e:
        logger.error(f"CLICK ON THE ELEMENT : {element} field. Message : {e}")
        return False


# def click_on_element(driver, element):
#     """
#     Click on the specified element using JavaScript.

#     Args:
#         driver (webdriver.Chrome): The WebDriver instance.
#         element (WebElement): The element to click.

#     Returns:
#         bool: True if the click was successful, False otherwise.
#     """
#     max_attempts = 3
#     for attempt in range(max_attempts):
#         try:
#             # Wait for the element to be clickable
#             WebDriverWait(driver, 10).until(EC.element_to_be_clickable(element))
#             driver.execute_script("arguments[0].click();", element)
#             return True
#         except StaleElementReferenceException:
#             logger.warning(f"Stale element reference for {element}. Retrying... (Attempt {attempt + 1})")
#             # Re-locate the element if it becomes stale
#             element = find_element(driver, element)  # You may need to adjust this line to re-find the element
#         except Exception as e:
#             logger.error(f"Failed to click on the element: {e}")
#             return False
#     logger.error("Maximum attempts reached. Could not click on the element.")
#     return False


def get_number_of_pages(driver, url, timeout=15):
    """
    Get the number of pages for pagination.

    Args:
        driver (webdriver.Chrome): The WebDriver instance.
        url (str): The URL to check.
        timeout (int): Timeout for waiting elements.

    Returns:
        int or None: The maximum page number, or None if not found.
    """
    driver.get(url)
    try:
        wait = WebDriverWait(driver, timeout)
        wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, CSS_SELECTORS[5]))
        )
        li_items = driver.find_elements(By.CSS_SELECTOR, CSS_SELECTORS[6])
        page_numbers = []
        for li in li_items:
            try:
                a_tag = li.find_element(By.TAG_NAME, "a")
                text = a_tag.text.strip()
                if text.isdigit():
                    page_numbers.append(int(text))
            except:
                continue
        if page_numbers:
            return max(page_numbers)
        return None
    except Exception as e:
        logger.error(f"[!] Error retrieving pagination: {e}")
        return None

def is_url_valid(url):
    """
    Check if a URL is valid and reachable.

    Args:
        url (str): The URL to check.

    Returns:
        bool: True if the URL is valid, False otherwise.
    """
    try:
        response = requests.head(url)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def get_all_pages_url(main_url, number_of_pages):
    """
    Construct URLs for all pages based on the main URL and number of pages.

    Args:
        main_url (str): The main URL.
        number_of_pages (int): The total number of pages.

    Returns:
        list: List of all page URLs.
    """
    all_pages = [main_url]
    all_pages.extend([main_url.replace(f"page=1", f"page={i+1}") for i in range(1, number_of_pages)])
    return all_pages

def get_element_by_requests(url, wait_time=0):
    """
    Get the HTML content of a URL using requests and parse it with BeautifulSoup.

    Args:
        url (str): The URL to fetch.
        wait_time (int): Time to wait after fetching.

    Returns:
        BeautifulSoup: Parsed HTML content.
    """
    try:
        with requests.session() as Session:
            response = Session.get(url)
            time.sleep(wait_time)
            return BeautifulSoup(response.text, 'html.parser')
    except Exception as e:
        logger.error(f"Error getting element by requests! \n Message : {e}")

def construct_company_object(infos):
    """
    Construct a Company object from the provided information dictionary.

    Args:
        infos (dict): Dictionary containing company information.

    Returns:
        Company: The constructed Company object.
        int: 0 if initialization fails.
    """
    try:
        name = infos.get("Name", None)
        url_vitrine = infos.get("Url", None)
        url_web_site = infos.get("Web Site", None)
        domain = infos.get("Domain", None)
        location = infos.get("Location", None)
        number_salaries = infos.get("Collaborateurs", None)
        average_age = infos.get("Âge moyen", None)
        offers = infos.get("Offer", None)
        all_offers = infos.get("Offres", [])
        spontaneous_application = infos.get("Candidature spontanée", "Non")

        return Company(
            name,
            url_vitrine,
            url_web_site,
            domain,
            location,
            int(number_salaries) if str(number_salaries).isdigit() else None,
            int(str(average_age).split(' ')[0]) if str(str(average_age).split(' ')[0]).isdigit() else None,
            int(str(offers.split(' '))[0]) if str(str(offers.split(' '))[0]).isdigit() else 1 if spontaneous_application == "Oui" else None,
            all_offers,
            spontaneous_application
        )
    except Exception as e:
        logger.error(f"Error initialising Company Object. : {e}")
        return 0

def get_element_by_web_driver(driver, url, wait_time=0):
    """
    Get the HTML content of a URL using Selenium WebDriver and parse it with BeautifulSoup.

    Args:
        driver (webdriver.Chrome): The WebDriver instance.
        url (str): The URL to fetch.
        wait_time (int): Time to wait after loading.

    Returns:
        BeautifulSoup or None: Parsed HTML content, or None if failed.
    """
    try:
        get_url(driver, url)
        if wait_time > 0:
            time.sleep(wait_time)
        html = driver.page_source
        return BeautifulSoup(html, "html.parser")
    except Exception as e:
        logger.error(f"[!] Erreur chargement page WebDriver : {url}, {e}")
        return None

def get_companys_blocks(driver, url):
    """
    Get the blocks of companies from the specified URL.

    Args:
        driver (webdriver.Chrome): The WebDriver instance.
        url (str): The URL to fetch.

    Returns:
        list: List of company blocks.
    """
    soup = get_element_by_web_driver(driver, url, 5)
    if not soup:
        return []
    try:
        return soup.select(CSS_SELECTORS[7])
    except Exception as e:
        logger.error(f"Error getting company blocks: {e}")
        return []

def get_companys_infos(driver, block):
    """
    Extract company information from a block.

    Args:
        driver (webdriver.Chrome): The WebDriver instance.
        block (Tag): The HTML block containing company info.

    Returns:
        dict: Dictionary of company information.
    """
    try:
        name = block.select_one(CSS_SELECTORS[8]).text
        details = block.select(CSS_SELECTORS[9])
        domain = details[-3].text
        location = details[-2].text
        offer = block.select_one(CSS_SELECTORS[10]).text
        link = urljoin(MAIN_URL, block.select_one(CSS_SELECTORS[11])['href'])

        infos = {
            "Name": name,
            "Domain": domain.replace("\u00e9", "é"),
            "Location": location,
            "Offer": offer,
            "Link ": link
        }

        temp_jobs_link = link.split("?")[0] + "/jobs?" + link.split("?")[1]
        if is_url_valid(temp_jobs_link):
            jobs_link = temp_jobs_link
        else:
            jobs_link = link

        offres = offres_emploi(driver, jobs_link)
        infos["Offres"] = offres

        if "Candidature spontanée" in offres:
            infos["Candidature spontanée"] = "Oui"
        else:
            infos["Candidature spontanée"] = "Non"

        infos = infos | get_other_infos(link)
        return infos

    except Exception as e:
        logger.error(f"Erreur récupèration des informations de {block.select_one(CSS_SELECTORS[8]).text} \n Message {e}")
        return {}

def get_other_infos(url):
    """
    Extract additional company information from the given URL.

    Args:
        url (str): The URL to fetch.

    Returns:
        dict: Dictionary of additional company information.
    """
    block_dict = {}
    soup = get_element_by_requests(url, 1)
    if not soup:
        return block_dict

    try:
        web_site_tag = soup.select_one(CSS_SELECTORS[12])
        if web_site_tag:
            block_dict["Web Site"] = web_site_tag['href']
    except:
        pass

    block_details = soup.select(CSS_SELECTORS[13])
    for block in block_details:
        try:
            titre = block.select_one(CSS_SELECTORS[14]).text
            contenu = block.select_one(CSS_SELECTORS[15]).text
            block_dict[titre] = contenu
        except:
            continue
    return block_dict

def offres_emploi(driver, urljobs):
    """
    Get the list of job offers from the specified jobs URL.

    Args:
        driver (webdriver.Chrome): The WebDriver instance.
        urljobs (str): The jobs URL.

    Returns:
        list: List of job offer texts.
    """
    soup = get_element_by_web_driver(driver, urljobs, 2)
    if not soup:
        return []
    jobs = soup.select(CSS_SELECTORS[16])
    return [job.text for job in jobs]

def error_finding_element(element):
    """
    Log an error message if an element is not found.

    Args:
        element : The name of the element that was not found.
    """
    logger.error(f"Element {element} not found. Please check the CSS selector or the page structure.")
    return 0

def main():
    """
    Main function to scrape company data and save it to SQLite and JSON files.
    """
    companies = Companies([]) # Initialize an empty Companies object
    driver = init_driver() # Initialize the WebDriver

    if not driver:
        # If driver initialization fails, log the error and exit
        logger.error("Failed to initialize the web driver. Exiting.")
        return
    try:
        # Access the companies URL and wait for the sector element to be present
        get_url(driver, COMPANIES_URL)
        logger.info(f"Accessing companies URL: {COMPANIES_URL}")
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, CSS_SELECTORS[1]))
        )

        # Find the sector element and click on it to select the Tech category
        sector = find_element(driver, 1)
        if not sector:
            logger.error("Sector element not found. Exiting.")
            return
        logger.info("Sector element found, clicking to select Tech category.")
        time.sleep(2)
        # Click on the sector element to open the dropdown
        if click_on_element(driver, sector) == True:
            time.sleep(1) # Wait for the list of sectors to open
        else:
            logger.error("Failed to click on the sector element. Exiting.")
            return

        # Find the Tech category element and click on it
        tech_category = find_element(driver, 2)
        if not tech_category:
            logger.error("Tech category element not found. Exiting.")
            return
        check_tech = find_element(tech_category, 3)
        if not check_tech:
            logger.error("Checkbox for Tech category not found. Exiting.")
            return
        logger.info("Tech category element found, clicking to select it.")
        click_on_element(driver, check_tech)

        # Find the search button and click on it to apply the filter
        search_button = find_element(driver, 4)
        if not search_button:
            logger.error("Search button element not found. Exiting.")
            return
        logger.info("Search button element found, clicking to apply the filter.")
        click_on_element(driver, search_button)

        #get the first page URL and the number of pages
        tech_first_page_url = driver.current_url
        number_of_pages = get_number_of_pages(driver, tech_first_page_url)
        logger.info(f"Number of pages found: {number_of_pages}")

        all_pages = get_all_pages_url(tech_first_page_url, number_of_pages)
        blocks = get_companys_blocks(driver, tech_first_page_url)
        logger.info(f"Number of company blocks found on the first page: {len(blocks)}")
        for page in all_pages:
            logger.info(f"Processing page: {page}")
            blocks = get_companys_blocks(driver, page)
            for block in blocks:
                infos = get_companys_infos(driver, block)
                if infos:
                    companies.companies.append(construct_company_object(infos))
                time.sleep(1)
    finally:
        if driver is not None:
            driver.quit()

    if len(companies.companies) > 0:
        logger.info(f"Total companies found: {len(companies.companies)}")
        # Save the companies data to SQLite and JSON files
        try:
            companies.save_companies_to_sqlite(DB_FILE)
            companies.save_companies_to_json(JSON_FILE)
            logger.info(f"Companies data saved to {DB_FILE} and {JSON_FILE}")
        except FileExistsError or FileNotFoundError :
            logger.error(f"Error saving companies data to files: {DB_FILE} or {JSON_FILE}. Please check the file paths.")
            companies.save_companies_to_json("data.json")
            companies.save_companies_to_sqlite("data.db")
        except Exception as e:
            logger.error(f"An unexpected error occurred while saving companies data: {e}")
    else:
        logger.warning("No companies found during the scraping process.")

if __name__ == "__main__":
    main()