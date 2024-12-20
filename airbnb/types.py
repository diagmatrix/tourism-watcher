from dataclasses import dataclass
from typing import List


@dataclass
class ListingData:
    """
    Class representing the relevant data for an Airbnb listing

    Attributes:
        url (str): URL of the Airbnb listing
        host (str): Username of the host of the Airbnb listing
        permit (str): Tourism's lodging permit of the Airbnb listing
    """

    url: str  # Listing url
    host: str = None
    permit: str = None

    def to_list(self) -> List[str]:
        """
        Converts the data to a list of strings
        :return: List of strings containing the data ['url', 'host', 'permit']
        """
        return [self.url, self.host, self.permit]
