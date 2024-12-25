from functools import wraps

from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from .exceptions import RetrievalError
from database.services import EntityNotFoundError

def error_handler(func):
    """A decorator that provides comprehensive error handling for database-related methods.

    It catches and handles various database and retrieval exceptions,
    displaying appropriate error messages and managing database session rollbacks.
    The decorator wraps method calls to intercept and gracefully handle different types of exceptions
    that may occur during database operations, ensuring consistent error reporting and session management.

    Examples:
        # Applying the decorator to a database method
        @error_handler
        def save_device(self, device):
            # Method implementation that might raise database exceptions
            self.session.add(device)
            self.session.commit()
    """
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except RetrievalError as e:
            self.show_error("ValueError", e)
        except RetrievalError as e:
            self.show_error("RetrievalError", e)
        except IntegrityError as e:
            self.show_error("IntegrityError", e)
            self.app.session.rollback()
        except SQLAlchemyError as e:
            self.show_error("SQLAlchemyError", e)
            self.app.session.rollback()
        except Exception as e:
            self.show_error("UKNOWN ERROR", e)
            self.app.session.rollback()

    return wrapper