class RenameFileException(Exception):
    """
    Exception raised when a file cannot be renamed

    Attributes:
        filename: The name of the file (optional)
        base_error: The base error that occurred when renaming the file (optional)
        message: Explanation of the exception (optional)
    """

    def __init__(self, filename: str = None, base_error: Exception = None, message: str = None):
        self.filename = filename
        self.base_error = base_error
        if not message:
            match self.base_error:
                case FileNotFoundError():
                    self.message = f"No such file or directory: '{self.filename}'"
                case PermissionError():
                    self.message = f"Not allowed to access: '{self.filename}'"
                case _:
                    self.message = f"Unexpected error renaming file: '{self.filename}'"
        else:
            self.message = message

        super().__init__(self.message)
