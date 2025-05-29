from urllib.parse import urljoin

LOGGING_FILE = "../log/Sites.log"
JSON_FILE = "../data/data.json"
DB_FILE = "../data/data.db"

MAIN_URL = "https://www.welcometothejungle.com/"
COMPANIES_URL = urljoin(MAIN_URL, "fr/companies")

test = "header[data-testid='companies-search-search-widget-sectors']"
SECTOR_CSS_SELECTOR = "header[data-testid='companies-search-search-widget-sectors']"

# CSS Selectors for the Tech sector
TECH_CSS_SELECTOR = "span[data-testid='companies-search-search-widgets-sectors_name-19-trigger']"
CHECKBOX_TECH_SELECTOR = "input[type='checkbox']"
SEARCH_BUTTON_CSS_SELECTOR = "button[type='submit'].sc-bkUKrm"

# CSS Selectors as constants
PAGINATION_NAV_SELECTOR = "[data-testid='companies-search-pagination'] nav ul"
PAGINATION_LI_SELECTOR = PAGINATION_NAV_SELECTOR + " li"
COMPANY_BLOCK_SELECTOR = "article[data-role='companies:thumb'][data-testid='company-card']"
COMPANY_NAME_SELECTOR = "div header a span"
COMPANY_DETAILS_SELECTOR = "ul li"
COMPANY_OFFER_SELECTOR = "footer a span"
COMPANY_LINK_SELECTOR = "a"
COMPANY_WEBSITE_SELECTOR = "div div p a"
COMPANY_DETAILS_BLOCK_SELECTOR = "div.sc-iqrLza.hGwRdy.showcase-block.block.block-span-1 div div section"
COMPANY_DETAILS_TITLE_SELECTOR = "h4"
COMPANY_DETAILS_CONTENT_SELECTOR = "span"
COMPANY_JOBS_SELECTOR = "div div a h4"


CSS_SELECTORS = {
    1: SECTOR_CSS_SELECTOR,
    2: TECH_CSS_SELECTOR,
    3: CHECKBOX_TECH_SELECTOR,
    4: SEARCH_BUTTON_CSS_SELECTOR,
    5: PAGINATION_NAV_SELECTOR,
    6: PAGINATION_LI_SELECTOR,
    7: COMPANY_BLOCK_SELECTOR,
    8: COMPANY_NAME_SELECTOR,
    9: COMPANY_DETAILS_SELECTOR,
    10: COMPANY_OFFER_SELECTOR,
    11: COMPANY_LINK_SELECTOR,
    12: COMPANY_WEBSITE_SELECTOR,
    13: COMPANY_DETAILS_BLOCK_SELECTOR,
    14: COMPANY_DETAILS_TITLE_SELECTOR,
    15: COMPANY_DETAILS_CONTENT_SELECTOR,
    16: COMPANY_JOBS_SELECTOR
}


MAIN_TECH_PAGE_URL = "https://www.welcometothejungle.com/fr/companies?page=1&query=&refinementList%5Bsectors_name.fr.Tech%5D%5B%5D=SaaS%20%2F%20Cloud%20Services&refinementList%5Bsectors_name.fr.Tech%5D%5B%5D=Logiciels&refinementList%5Bsectors_name.fr.Tech%5D%5B%5D=Intelligence%20artificielle%20%2F%20Machine%20Learning&refinementList%5Bsectors_name.fr.Tech%5D%5B%5D=Application%20mobile&refinementList%5Bsectors_name.fr.Tech%5D%5B%5D=Big%20Data&refinementList%5Bsectors_name.fr.Tech%5D%5B%5D=Cybers%C3%A9curit%C3%A9&refinementList%5Bsectors_name.fr.Tech%5D%5B%5D=Objets%20connect%C3%A9s&refinementList%5Bsectors_name.fr.Tech%5D%5B%5D=Robotique&refinementList%5Bsectors_name.fr.Tech%5D%5B%5D=Blockchain"