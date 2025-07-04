# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import time
import logging

from SELECTORS import *
from CONST import *
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
        return webdriver.Chrome()
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
        logger.error(f"ERROR FINDING ELEMENT, : {e}")
        return None

def click_on_element(driver, element, name=""):
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
        logger.error(f"CLICK ON THE ELEMENT : {name} field. Message : {e}")
        return False

def find_and_click(driver, selectors_key, name="", number="one", timeout=10):
    """
    Find an element by CSS selector and click on it.

    Args:
        driver (webdriver.Chrome): The WebDriver instance.
        selectors_key (int): The key for the CSS selector.
        number (str): "one" for a single element, otherwise multiple.
        timeout (int): The maximum time to wait for the element to be found.

    Returns:
        bool: True if the click was successful, False otherwise.
    """
    element = find_element(driver, selectors_key, number, timeout)
    if element:
        return click_on_element(driver, element)
    else:
        logger.error(f"Element [{name}] not found.")
        return False
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


if __name__ == "__main__":
    # Initialize the Companies object and WebDriver
    pass