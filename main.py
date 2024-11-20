import logging
import os

from airbnb import AirbnbScrapper
from ja import JAScrapper


def start_logger(log_file: str = None) -> logging.Logger:
    """
    Start the logger
    :param log_file: Name of the log file to write to
    """
    program_logger = logging.getLogger("TourismWatcher")
    if log_file is not None:
        logging.basicConfig(
            format="[%(asctime)s] %(levelname)s %(name)s: %(message)s",
            filename=log_file,
            datefmt="%Y-%m-%d %H:%M:%S",
            level=logging.INFO,
        )
    else:
        logging.basicConfig(
            format="[%(asctime)s] %(levelname)s %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            level=logging.INFO,
        )
    return program_logger


if __name__ == "__main__":
    # Start logger
    logger = start_logger()

    # Firefox download options
    download_dir = os.path.abspath("./data/ja_raw")
    options = {
        "browser.download.folderList": 2,
        "browser.download.dir": download_dir,  # TODO: Add from env
        "browser.helperApps.neverAsk.saveToDisk": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,application/vnd.ms-excel",
    }

    logger.info("Starting scrapping")

    with JAScrapper("firefox", options, download_dir, ("--no-sandbox")) as scrapper:  # TODO: Add browser type from argument list
        scrapper.extract(activities=["Vivienda turística de alojamiento rural"])
    with AirbnbScrapper("firefox") as scrapper:
        scrapper.extract()

    logger.info("Ending scrapping")
