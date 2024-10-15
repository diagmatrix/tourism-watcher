import csv
import logging
import time
from datetime import datetime
from typing import List, Dict
from bs4 import BeautifulSoup
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from airbnb.exceptions import BrowserNotSupported, NullBrowserSession
from airbnb.types import Browser, ListingData
from airbnb.utils import start_selenium
from airbnb.vars import (
    AIRBNB_URL,
    CSS_NEXT_PAGE,
    URL_SELECTOR,
    CSS_LISTINGS,
    CSS_PERMIT,
    CSS_HOSTNAME,
    HOST_SELECTOR,
    CSV_HEADERS,
)


class AirbnbScrapper:
    """
    Class responsible for scraping Airbnb listing pages

    Attributes:
        logger          (logging.Logger): logger instance for the class
        browser_name    (str): Name of the browser to use
        browser_args    (tuple): Arguments to pass to the browser when initialized
        browser         (WebDriver): Selenium driver
        results         (List[BeautifulSoup]): List containing the raw airbnb pages
        listings        (List[ListingData]): List containing the data of the listings
    """

    logger = logging.getLogger("AirbnbScrapper")

    def __init__(self, browser: Browser, arguments=("--headless", "--no-sandbox")) -> None:
        # Browser
        self.browser_name = browser
        self.browser_args = arguments
        self.browser = None
        self.open()
        # Pages
        self.results: List[BeautifulSoup] = []
        # Listings
        self.listings: List[ListingData] = []

    def extract(self, url=AIRBNB_URL, filename: str = None, **kwargs) -> None:
        """
        Extract the data from an Airbnb page and save it in a csv file
        :param url: The url of the page to extract data from
        :param filename: The name for the csv file
        :param kwargs: Additional arguments to pass to the scraping function. Possible arguments are:
            - load_time: Time in seconds to wait for the pages to load
            - click_time: Time in seconds to wait after clicking the 'Next page' button
            - css_next_page: CSS classname of the 'Next page' button
            - css_listings: CSS classname of the individual listings in a page
            - url_selector: Selector (html tag & attributes) to get the url of a listing
            - host_selector: Selector (html tag & attributes) to get the host information of a listing
            - css_hostname: CSS classname of the hostname of a listing
            - css_permit: CSS classname of the tourism's lodging permit of a listing
            - csv_headers: Headers of the csv file
        """
        # Arguments
        load_time = kwargs.get('load_time', 8)  # 8 is an arbitrary time (works well with 300Mbps connection)
        click_time = kwargs.get('click_time', 1)
        css_next_page = kwargs.get('css_next_page', CSS_NEXT_PAGE)
        css_listings = kwargs.get('css_listings', CSS_LISTINGS)
        url_selector = kwargs.get('url_selector', URL_SELECTOR)
        host_selector = kwargs.get('host_selector', HOST_SELECTOR)
        css_hostname = kwargs.get('css_hostname', CSS_HOSTNAME)
        css_permit = kwargs.get('css_permit', CSS_PERMIT)
        csv_headers = kwargs.get('csv_headers', CSV_HEADERS)

        # Scrape
        self.extract_soup(url, load_time, click_time, css_next_page)
        self.scrape_listings_links(css_listings, url_selector)
        self.extract_listing_data(load_time, host_selector, css_hostname, css_permit)
        self.to_csv(csv_headers, filename)

    def extract_soup(self, url: str, load_time: int, click_time: int, css_next_page: str) -> None:
        """
        Extracts the all the result pages for the Airbnb website
        :param url: Airbnb search URL from which to extract the pages
        :param load_time: Time in seconds to wait for the page to load
        :param click_time: Time in seconds to wait after clicking the 'Next page' button
        :param css_next_page: CSS classname of the 'Next page' button
        """
        self.results.append(self._get_page(url, load_time))
        current_url = self.browser.current_url

        more_pages = True
        i = 2
        # Go to next results page
        while more_pages:
            self.logger.info("Going to page %s", i)
            i += 1
            try:  # Try to click to the next page
                self.browser.find_element(
                    by=By.CLASS_NAME, value=css_next_page
                ).click()
                time.sleep(click_time)
            except NoSuchElementException:
                self.logger.info("No more pages")
                more_pages = False

            # Check the URLs differ
            url_after = self.browser.current_url
            if url_after == current_url:
                if more_pages: # Prevent double logging when 'NoSuchElementException' was raised before
                    self.logger.info("No more pages")
                more_pages = False
            else:
                current_url = url_after
                self.results.append(self._get_page(current_url, load_time))

    def scrape_listings_links(self, css_listings: str, url_selector: Dict) -> List[str]:
        """
        Scrapes the results of the Airbnb listings page to get the links to the individual listings
        :param css_listings: CSS class of the individual listings
        :param url_selector: Selector for the URL contained in the listing HTML tag
        :return: List of links to the individual listings
        """
        links = []
        self.logger.info("Scraping listings' urls from the pages")

        if self.results:
            # Parsing the URLS
            i = 1
            for page in self.results:
                listings = page.findAll(class_=css_listings)
                try:
                    urls = [
                        "https://" + listing.find(**url_selector)["content"]
                        for listing in listings
                    ]
                    links.extend(urls)
                except TypeError:
                    self.logger.warning("No links found in page %s", i)
                i += 1

            # Set the urls of the listings
            self.listings = [ListingData(url=url) for url in links]
        else:
            self.logger.warning("No pages found. Try calling 'extract_soup' first")

        return links

    def extract_listing_data(
        self,
        load_time: int,
        host_selector: Dict,
        css_hostname,
        css_permit,
        listings: List[str] = None,
    ) -> List[ListingData]:
        """
        Extracts the data from the listings
        :param load_time: Time in seconds to wait for the page to load
        :param host_selector: Selector to get the host info
        :param css_hostname: CSS classname for the host username
        :param css_permit: CSS classname for the tourism's lodging permit
        :param listings: List of URLs of the listings
        :return: A list containing the data from the listings
        """
        self.listings = (
            [ListingData(url=url) for url in listings] if listings else self.listings
        )
        self.logger.info("Extracting the data from the listings")

        for listing in self.listings:
            soup = self._get_page(listing.url, load_time)
            # Host name
            try:
                host_soup = soup.find(**host_selector)
                host_name = host_soup.find("div", class_=css_hostname).text
                listing.host = host_name.split(": ")[-1]
            except AttributeError:
                self.logger.warning("Host username couldn't be extracted")
            # Tourism permit
            try:
                permit_soup = soup.find(class_=css_permit)
                permit = permit_soup.text
                listing.permit = permit.split(" ")[-1]
            except AttributeError:
                self.logger.warning("Tourism's lodging permit couldn't be extracted")

        return self.listings

    def to_csv(self, headers: List[str], filename: str = None) -> None:
        """
        Save the listings to a csv file
        :param headers: Header names for the file
        :param filename: Name of the csv file (yyyy-mm-dd_listings.csv as default)
        :return:
        """
        data = [headers]
        for listing in self.listings:
            data.append(listing.to_list())

        file = filename if filename is not None else datetime.now().strftime('%Y-%m-%d') + "_listings.csv"
        self.logger.info(f"Saving listings to {file}")
        with open(file, mode="a", newline="", encoding="UTF-8") as f:
            writer = csv.writer(f)
            writer.writerows(data)
            f.close()

    def _get_page(self, url: str, load_time: int) -> BeautifulSoup:
        """
        Gets HTML page and returns it as a BeautifulSoup object
        :param url: URL to get
        :param load_time: Time in seconds to wait for the page to load
        :return: BeautifulSoup object
        """
        self.logger.info("Fetching page %s", url)
        if self.browser:
            self.browser.get(url)
            time.sleep(load_time)
            html = self.browser.page_source
            return BeautifulSoup(html, features="html.parser")
        else:
            self.logger.exception("No browser session")
            raise NullBrowserSession()

    def open(self) -> None:
        """Initializes Selenium browser"""
        self.logger.info("Initializing browser: %s", self.browser_name)
        try:
            self.browser = start_selenium(self.browser_name, self.browser_args)
        except BrowserNotSupported:
            self.logger.exception("Browser not supported")
            raise

    def close(self) -> None:
        """Explicitly close the browser session."""
        if self.browser:
            self.logger.info("Closing browser session")
            self.browser.quit()
            self.browser = None
        else:
            self.logger.warning("Trying to close a null browser session")

    def __enter__(self) -> "AirbnbScrapper":
        """Start the resource when entering a context."""
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """Ensure the browser closes when the context ends."""
        self.close()
