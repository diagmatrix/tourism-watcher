"""
Airbnb scrapping module

Classes:
    AirbnbScrapper: Class responsible for scraping Airbnb listing pages

    ListingData: Class containing the data from an Airbnb listing

Exceptions:
    BrowserNotSupported: Exception raised when trying to initialize a browser that is not supported

    NullBrowserSession: Exception raised when trying to use a browser session that does not exist
"""

from .airbnb import AirbnbScrapper
from .types import ListingData
from .exceptions import BrowserNotSupported, NullBrowserSession

__all__ = ["AirbnbScrapper", "ListingData", "BrowserNotSupported", "NullBrowserSession"]
