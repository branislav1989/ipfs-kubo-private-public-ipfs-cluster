"""DataHosting IPFS Client SDK - Connect to datahosting.company"""
from .client import DataHostingClient
from .exceptions import DataHostingError, AuthenticationError, UploadError
__version__ = "1.0.0"
__all__ = ["DataHostingClient", "DataHostingError", "AuthenticationError", "UploadError"]
