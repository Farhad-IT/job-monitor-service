
class AppException(Exception):
    status_code = 400
    def __init__(self, detail: str) -> None:
        self.detail = detail


class NotFoundException(AppException):
    status_code = 404
