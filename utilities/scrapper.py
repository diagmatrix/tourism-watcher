import logging
import time

from bs4 import BeautifulSoup

from exceptions.browser import NullBrowserSession, BrowserNotSupported
from utilities import Browser, start_selenium


class Scrapper:
    """
    Abstract class for scrappers.

    Attributes:
        logger          (logging.Logger): logger instance for the class
        browser_name    (str): Name of the browser to use
        browser_args    (tuple): Arguments to pass to the browser when initialized
        browser_options (dict): Options for the browser when initialized
        browser         (WebDriver): Selenium driver
    """

    __abstract__ = True
    logger = logging.getLogger("Default Scrapper")

    def __init__(self, browser: Browser, arguments=("--headless", "--no-sandbox"), options=None) -> None:
        # Browser
        self.browser_name = browser
        self.browser_args = arguments
        self.browser_options = options if options else {}
        self.browser = None
        self.open()

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
            self.browser = start_selenium(self.browser_name, self.browser_args, self.browser_options)
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

    def __enter__(self) -> "Scrapper":
        """Start the resource when entering a context."""
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """Ensure the browser closes when the context ends."""
        self.close()