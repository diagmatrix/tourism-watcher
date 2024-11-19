from typing import Tuple, Dict

from selenium import webdriver

from exceptions.browser import BrowserNotSupported, BrowserOptionsNotSupported
from utilities.types import Browser, WebDriver, Options


def start_selenium(browser: Browser, arguments: Tuple[str], browser_options: Dict) -> WebDriver:
    """
    Initializes a webdriver object
    :param browser: The browser to use
    :param arguments: The arguments to pass to the browser
    :param browser_options: The options to pass to the browser (only for Chrome and Firefox)
    :return: A webdriver object for the given browser
    """
    match browser:
        case "chrome":
            options = webdriver.ChromeOptions()
            add_browser_options(options, browser_options)
            for arg in arguments:
                options.add_argument(arg)
            return webdriver.Chrome(options=options)
        case "firefox":
            options = webdriver.FirefoxOptions()
            add_browser_options(options, browser_options)
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


def add_browser_options(options: Options, browser_options: Dict) -> None:
    """
    Applies browser options to an Options instance
    :param options: Options instance
    :param browser_options: Browser options to add
    """
    match options:
        case webdriver.ChromeOptions():
            options.add_experimental_option("prefs", browser_options)
            return
        case webdriver.FirefoxOptions():
            options.profile = webdriver.FirefoxProfile()
            for key, value in browser_options.items():
                options.profile.set_preference(key, value)
            return
        case _:
            raise BrowserOptionsNotSupported()
