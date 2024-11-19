"""
Exceptions and warnings raised by the package
"""


class BrowserNotSupported(Exception):
    """Exception raised when a browser is not supported

    Attributes:
        message: Explanation of the exception (optional)

    """

    def __init__(self, message: str = "Unsupported browser") -> None:
        self.message = message
        super().__init__(self.message)


class BrowserOptionsNotSupported(Exception):
    """Exception raised when trying to add an option to a browser where options are not supported

    Attributes:
        message: Explanation of the exception (optional)

    """

    def __init__(self, message: str = "Browser options not supported") -> None:
        self.message = message
        super().__init__(self.message)


class NullBrowserSession(Exception):
    """Exception raised when trying to interact with an empty browser session

    Attributes:
        message: Explanation of the exception (optional)
    """

    def __init__(self, message: str = "Null browser session") -> None:
        self.message = message
        super().__init__(self.message)
