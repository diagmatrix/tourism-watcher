"""
Global constants used in the module
"""

AIRBNB_URL = "https://www.airbnb.es/s/Granada--España/homes"
""" Airbnb URL to scrape """

CSS_LISTINGS = "c1l1h97y"
""" CSS classname of airbnb listings """

URL_SELECTOR = {"name": "meta", "attrs": {"itemprop": "url"}}
""" Selector to get the url of the listings """

CSS_NEXT_PAGE = "c1ytbx3a"
""" CSS classname of the next page button in the listings page """

CSS_PERMIT = "c2a9hgn"
""" CSS classname of a listing's tourism lodging permit """

HOST_SELECTOR = {"name": "div", "attrs": {"data-section-id": "HOST_OVERVIEW_DEFAULT"}}
""" Selector to get the host information """

CSS_HOSTNAME = "t1pxe1a4"
""" CSS classname of a listing's host username """

CSV_HEADERS = ["URL", "ANFITRION", "PERMISO"]
""" Headers for the csv file with the data """
