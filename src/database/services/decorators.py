from functools import wraps


def transactional(func):
    """Decorator to handle database transactions.

    This decorator ensures that database changes are committed on success
    and rolled back on failure.
    """

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            result = func(self, *args, **kwargs)
            self.db.commit()
            return result
        except Exception:
            self.db.rollback()
            raise

    return wrapper
