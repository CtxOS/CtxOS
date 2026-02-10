import logging
import traceback
from datetime import datetime


class CtxosError(Exception):
    """Base exception for all CtxOS errors."""

    def __init__(self, message, code="INTERNAL_ERROR", context=None, original_exception=None):
        super().__init__(message)
        self.message = message
        self.code = code
        self.context = context or {}
        self.original_exception = original_exception
        self.timestamp = datetime.utcnow().isoformat()

    def as_dict(self):
        """Returns a JSON-serializable representation of the error."""
        return {
            "error": {
                "code": self.code,
                "message": self.message,
                "context": self.context,
                "timestamp": self.timestamp,
            }
        }


class DependencyError(CtxosError):
    """Raised when dependency resolution fails."""

    def __init__(self, message, context=None):
        super().__init__(message, code="DEPENDENCY_ERROR", context=context)


class ProviderError(CtxosError):
    """Raised when a package provider fails."""

    def __init__(self, message, context=None):
        super().__init__(message, code="PROVIDER_ERROR", context=context)


class InstallationError(CtxosError):
    """Raised when installation/removal fails."""

    def __init__(self, message, context=None):
        super().__init__(message, code="INSTALL_ERROR", context=context)


class ValidationError(CtxosError):
    """Raised when input validation fails."""

    def __init__(self, message, context=None):
        super().__init__(message, code="VALIDATION_ERROR", context=context)


class NotFoundError(CtxosError):
    """Raised when a resource is not found."""

    def __init__(self, resource_type, resource_id, context=None):
        super().__init__(
            f"{resource_type} not found: {resource_id}", code="NOT_FOUND", context=context
        )


def handle_error(e):
    """Orchestrates standard error handling, logging, and response formatting."""
    logger = logging.getLogger("ctxos.errors")

    if isinstance(e, CtxosError):
        # Already normalized
        logger.error(f"CtxOS Error: {e.as_dict()}")
        return (
            e.as_dict(),
            400 if e.code == "VALIDATION_ERROR" or e.code == "DEPENDENCY_ERROR" else 500,
        )

    # Unexpected exception
    unexpected = CtxosError(str(e), original_exception=e)
    logger.error(f"Unexpected Error: {unexpected.as_dict()}")
    logger.error(traceback.format_exc())

    return unexpected.as_dict(), 500
