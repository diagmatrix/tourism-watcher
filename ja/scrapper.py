import logging
import os
import time
import copy
from datetime import datetime
from typing import Dict, List

from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

import utilities
from exceptions.files import RenameFileException
from exceptions.scrapping import ElementNotFoundException, WaitTimeoutException
from utilities import Scrapper, Browser
from ja.vars import JA_URL, CSS_ACTIVITY, TOURIST_APARTMENTS, CSS_PROVINCE, PROVINCE_NAME, CSS_MUNICIPALITY, \
    MUNICIPALITY_NAME, CSS_SEARCH, CSS_EXCEL, EXPORTED_FILENAME, CSS_RESULTS, RURAL_HOMES, TOURIST_HOMES, \
    RURAL_TOURIST_HOMES


class JAScrapper(Scrapper):
    """
    Class responsible for retrieving the Junta de Andalucía tourism registry data

    Attributes:
        logger          (logging.Logger): logger instance for the class
        browser_name    (str): Name of the browser to use
        browser_args    (tuple): Arguments to pass to the browser when initialized
        browser         (WebDriver): Selenium driver
        download_dir    (str): Directory where the Excel files will be downloaded
        exported_files  (list): List of the paths of the Excel files
    """

    logger = logging.getLogger("JAScrapper")

    def __init__(self, browser: Browser, options: Dict, download_dir: str, arguments=("--headless", "--no-sandbox")) -> None:
        # Browser
        super().__init__(browser, arguments, options)
        # Data
        self.download_dir = download_dir
        self.exported_files = []

    def extract(self, url=JA_URL, activities: List[str] = None, **kwargs):
        """
        Extracts the all the excel files from the JA
        :param url: JA's URL where the data is found (optional)
        :param activities: List of activities to extract (optional)
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
            'css_results': kwargs.get('css_results', CSS_RESULTS),
            'css_excel': kwargs.get('css_excel', CSS_EXCEL)
        }

        # Get files
        if not activities:
            self.exported_files.append(self.get_activity(url, **{
                **arguments,
                'activity_name': TOURIST_APARTMENTS
            }))
            self.exported_files.append(self.get_activity(url, **{
                **arguments,
                'activity_name': RURAL_HOMES
            }))
            self.exported_files.append(self.get_activity(url, **{
                **arguments,
                'activity_name': TOURIST_HOMES
            }))
            self.exported_files.append(self.get_activity(url, **{
                **arguments,
                'activity_name': RURAL_TOURIST_HOMES
            }))
        else:
            for activity in activities:
                self.exported_files.append(self.get_activity(url, **{
                    **arguments,
                    'activity_name': activity
                }))

    def get_activity(self, url: str, **kwargs) -> str:
        """
        Retrieves the excel file with the list of a given activity
        :param url: JA's URL where the data is found
        :param kwargs: All arguments expected from extract plus
            - activity_name: Value of the activity selector
        :return: The path to the excel file
        """

        # Load the page
        self.logger.info("Retrieving %s", kwargs['activity_name'])
        self.browser.get(url)
        self.browser.switch_to.frame(0)

        # Select activity
        try:
            dropdown = WebDriverWait(self.browser, kwargs['load_time']).until(
                ec.presence_of_element_located((By.XPATH, kwargs['css_activity']))
            )
            selector = Select(dropdown)
            selector.select_by_visible_text(kwargs['activity_name'])
        except TimeoutException as e:
            self.logger.exception("Timeout waiting for activity selector to load")
            raise WaitTimeoutException(kwargs['css_activity']) from e
        except NoSuchElementException as e:
            self.logger.exception("Activity not found")
            raise ElementNotFoundException(kwargs['activity_name']) from e
        time.sleep(kwargs['click_time'])

        # Select province
        try:
            dropdown = WebDriverWait(self.browser, kwargs['load_time']).until(
                ec.presence_of_element_located((By.XPATH, kwargs['css_province']))
            )
            selector = Select(dropdown)
            selector.select_by_visible_text(kwargs['province_name'])
        except TimeoutException as e:
            self.logger.exception("Timeout waiting for province selector to load")
            raise WaitTimeoutException(kwargs['css_province']) from e
        except NoSuchElementException as e:
            self.logger.exception("Province not found")
            raise ElementNotFoundException(kwargs['province_name']) from e
        time.sleep(kwargs['click_time'])

        # Select municipality
        try:
            dropdown = WebDriverWait(self.browser, kwargs['load_time']).until(
                ec.presence_of_element_located((By.XPATH, kwargs['css_municipality']))
            )
            selector = Select(dropdown)
            selector.select_by_visible_text(kwargs['municipality_name'])
        except TimeoutException as e:
            self.logger.exception("Timeout waiting for municipality selector to load")
            raise WaitTimeoutException(kwargs['css_municipality']) from e
        except NoSuchElementException as e:
            self.logger.exception("Municipality not found")
            raise ElementNotFoundException(kwargs['municipality_name']) from e
        time.sleep(kwargs['click_time'])

        # Click search button & Download file
        self.browser.find_element(By.XPATH, kwargs['css_search']).click()
        time.sleep(kwargs['load_time']*3) # TODO: Find a better way to do this
        self.browser.find_element(By.CSS_SELECTOR, kwargs['css_excel']).click()

        # Let time for file download
        self.logger.info("Downloading excel file")
        start_time = time.time()
        file_path = os.path.join(self.download_dir, EXPORTED_FILENAME)
        timeout = kwargs['load_time']*3  # Arbitrary value
        while not os.path.exists(file_path):
            time.sleep(1)
            if time.time() - start_time > timeout:
                self.logger.exception("Timeout waiting for file to download")
                raise WaitTimeoutException(EXPORTED_FILENAME)

        # Rename file
        try:
            file_activity_name = copy.deepcopy(kwargs['activity_name'])
            new_name = datetime.now().strftime('%Y-%m-%d') + "_" + file_activity_name.replace(" ", "_") + ".xlsx"
            utilities.rename_file(file_path, new_name)
        except Exception as e:
            self.logger.exception("Error while renaming exported file")
            raise RenameFileException(EXPORTED_FILENAME, e)

        return file_path
