import logging

from airbnb import AirbnbScrapper


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

    logger.info("Starting scrapper")

    with AirbnbScrapper("firefox") as scrapper:  # TODO: Add browser type from argument list
        scrapper.extract()

    logger.info("Ending scrapper")
