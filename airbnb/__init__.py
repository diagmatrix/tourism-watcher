"""
Airbnb scrapping module

Classes:
    AirbnbScrapper: Class responsible for scraping Airbnb listing pages

    ListingData: Class containing the data from an Airbnb listing
"""

from .airbnb import AirbnbScrapper
from .types import ListingData

__all__ = ["AirbnbScrapper", "ListingData"]
