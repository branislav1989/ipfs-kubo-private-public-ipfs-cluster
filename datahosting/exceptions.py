class DataHostingError(Exception):
    pass
class AuthenticationError(DataHostingError):
    pass
class UploadError(DataHostingError):
    pass
