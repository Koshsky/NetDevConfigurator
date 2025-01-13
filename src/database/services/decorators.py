from functools import wraps


def transactional(func):
    """A decorator that wraps database transaction methods to automatically handle commit and rollback operations.

    It ensures that database transactions are properly managed,
    committing successful operations and rolling back in case of exceptions.

    Example:
        @transactional
        def some_database_method(self, ...):
            # Method implementation
            # Commits automatically if no exception occurs
            # Rolls back if an exception is raised
    """

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            result = func(self, *args, **kwargs)
            self.db.commit()
            return result
        except Exception as e:
            self.db.rollback()
            raise

    return wrapper
