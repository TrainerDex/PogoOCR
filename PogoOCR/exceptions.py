from google.auth.exceptions import GoogleAuthError


class PogoOCRException(Exception):
    pass


class CloudVisionClientException(PogoOCRException):
    """Raised when Cloud Vision Client has failed"""

    pass


class CloudVisionAuthenticationException(CloudVisionClientException, GoogleAuthError):
    """Raised when Cloud Vision Client has failed to authenticate"""

    pass


class CloudVisionTextAnnotationException(CloudVisionClientException):
    """Raised when Cloud Vision Client has failed to annotate text"""

    pass


class OCRAttemptsExhausted(PogoOCRException):
    """Raised when OCR has exhausted all attempts"""

    pass
