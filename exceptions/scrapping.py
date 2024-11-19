class ElementNotFoundException(Exception):
    """Exception raised when trying to add an option to a browser where options are not supported

    Attributes:
        element: Selector for the html element (optional)
    """

    def __init__(self, element=None):
        self.element = element
        self.message = f"Element not found: {self.element}"
        super().__init__(self.message)


class WaitTimeoutException(Exception):
    """Exception raised when a wait time is exceeded

    Attributes:
        element: Selector for the html element (optional)
    """

    def __init__(self, element=None):
        self.element = element
        self.message = f"Timed out waiting for: {self.element}. Increase timeout limit and check that the element exists"
        super().__init__(self.message)
