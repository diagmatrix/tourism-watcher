from typing import Literal, Union

from selenium import webdriver

Browser = Literal["chrome", "firefox", "edge", "internet explorer", "safari"]
""" Supported browsers """

WebDriver = Union[
    webdriver.Chrome, webdriver.Firefox, webdriver.Edge, webdriver.Ie, webdriver.Safari
]
""" Supported selenium drivers """

Options = Union[webdriver.ChromeOptions(), webdriver.FirefoxOptions()]
""" Supported webdriver options """

