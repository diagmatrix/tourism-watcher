from typing import Tuple

from selenium import webdriver

from airbnb.exceptions import BrowserNotSupported
from airbnb.types import Browser, WebDriver


def start_selenium(browser: Browser, arguments: Tuple[str]) -> WebDriver:
    """
    Initializes a webdriver object
    :param browser: The browser to use
    :param arguments: The arguments to pass to the browser
    :return: A webdriver object for the given browser
    """
    match browser:
        case "chrome":
            options = webdriver.ChromeOptions()
            for arg in arguments:
                options.add_argument(arg)
            return webdriver.Chrome(options=options)
        case "firefox":
            options = webdriver.FirefoxOptions()
            for arg in arguments:
                options.add_argument(arg)
            return webdriver.Firefox(options=options)
        case "edge":
            options = webdriver.EdgeOptions()
            for arg in arguments:
                options.add_argument(arg)
            return webdriver.Edge(options=options)
        case "internet explorer":
            options = webdriver.IeOptions()
            for arg in arguments:
                options.add_argument(arg)
            return webdriver.Ie(options=options)
        case "safari":
            options = webdriver.SafariOptions()
            for arg in arguments:
                options.add_argument(arg)
            return webdriver.Safari(options=options)
        case _:
            raise BrowserNotSupported(f"Browser '{browser}' not supported")
