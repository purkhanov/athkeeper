
class DataOutdatedError(Exception):
    def __init__(
            self, message = "Data is outdated",
            auth_date = None,
            current_time = None
    ) -> None:
        super().__init__(message)
        self.auth_date = auth_date
        self.current_time = current_time
    

class InitDataHashMismatch(Exception):
    def __init__(self, message = "Data validation failed: hash mismatch") -> None:
        super().__init__(message)
