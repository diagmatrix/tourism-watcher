import logging
import time
from typing import Dict

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from utilities import Scrapper, Browser
from ja.vars import JA_URL, CSS_ACTIVITY, TOURIST_APARTMENTS, CSS_PROVINCE, PROVINCE_NAME, CSS_MUNICIPALITY, \
    MUNICIPALITY_NAME, CSS_SEARCH, CSS_EXCEL


class JAScrapper(Scrapper):
    """
    Class responsible for retrieving the Junta de Andalucía tourism registry data

    Attributes:
        logger          (logging.Logger): logger instance for the class
        browser_name    (str): Name of the browser to use
        browser_args    (tuple): Arguments to pass to the browser when initialized
        browser         (WebDriver): Selenium driver
        results         (List[BeautifulSoup]): List containing the raw airbnb pages
        listings        (List[ListingData]): List containing the data of the listings
    """

    logger = logging.getLogger("JAScrapper")

    def __init__(self, browser: Browser, options: Dict, arguments=("--headless", "--no-sandbox")) -> None:
        # Browser
        super().__init__(browser, arguments, options)

    def extract(self, url=JA_URL, **kwargs):
        """
        Extracts the all the excel files from the JA
        :param url: JA's URL where the data is found
        :param kwargs: Additional arguments to pass to the scraping function. Possible arguments are:
            - load_time: Time in seconds to wait for the pages to load
            - click_time: Time in seconds to wait after clicking a button
            - activity_name: Value of the activity selector
            - css_province: CSS selector of the 'Provincia' selector
            - province_name: Value of the province selector
            - css_municipality: CSS selector of the 'Municipio' selector
            - municipality_name: Value of the municipality selector
            - css_search: CSS selector of the 'Search' button
            - css_results: CSS selector of the 'Results' div
            - css_excel: CSS selector to extract the data to an Excel sheet
        """

        # Arguments
        arguments = {
            'load_time': kwargs.get('load_time', 8),  # 8 is an arbitrary time (works well with 300Mbps connection)
            'click_time': kwargs.get('click_time', 1),
            'css_activity': kwargs.get('css_activity', CSS_ACTIVITY),
            'css_province': kwargs.get('province_name', CSS_PROVINCE),
            'province_name': kwargs.get('province_name', PROVINCE_NAME),
            'css_municipality': kwargs.get('css_municipality', CSS_MUNICIPALITY),
            'municipality_name': kwargs.get('municipality_name', MUNICIPALITY_NAME),
            'css_search': kwargs.get('css_search', CSS_SEARCH),
            'css_excel': kwargs.get('css_excel', CSS_EXCEL)
        }

        # Get tourist apartments
        self.get_activity(url, **{
            **arguments,
            'activity_name': TOURIST_APARTMENTS
        })
        # TODO: Add the rest of activities

    def get_activity(self, url: str, **kwargs):
        """
        Retrieves the excel file with the list of a given activity
        :param url: JA's URL where the data is found
        :param kwargs: All arguments expected from extract plus
            - activity_name: Value of the activity selector
        :return:
        """

        # Extract the data TODO: selenium.common.exceptions.NoSuchElementException handling
        self.logger.info("Retrieving %s", kwargs['activity_name'])
        self.browser.get(url)

        time.sleep(kwargs['load_time'])
        self.browser.switch_to.frame(0)
        # Select activity
        dropdown = self.browser.find_element(By.XPATH, kwargs['css_activity'])
        selector = Select(dropdown)
        selector.select_by_visible_text(kwargs['activity_name'])
        time.sleep(kwargs['click_time'])
        # Select province & municipality
        dropdown = self.browser.find_element(By.XPATH, kwargs['css_province'])
        selector = Select(dropdown)
        selector.select_by_visible_text(kwargs['province_name'])
        time.sleep(kwargs['click_time'])
        dropdown = self.browser.find_element(By.XPATH, kwargs['css_municipality'])
        selector = Select(dropdown)
        selector.select_by_visible_text(kwargs['municipality_name'])
        time.sleep(kwargs['click_time'])
        # Click search button & Download file
        self.logger.info("Downloading excel file")
        self.browser.find_element(By.XPATH, kwargs['css_search']).click()
        time.sleep(kwargs['load_time']*2)  # TODO: Check button exist with 'wait' from selenium
        self.browser.find_element(By.CSS_SELECTOR, kwargs['css_excel']).click()
        time.sleep(kwargs['load_time']*2)  # Let time for file download
