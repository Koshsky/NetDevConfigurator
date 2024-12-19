from functools import wraps

def transactional(func):
    """A decorator that wraps database transaction methods to automatically handle commit and rollback operations.
    It ensures that database transactions are properly managed,
    committing successful operations and rolling back in case of exceptions.

    Args:
        func: The method to be wrapped with transaction management.

    Returns:
        A wrapped function that manages database transaction commit and rollback.

    Raises:
        Any exception that occurs during the original function's execution, after rolling back the transaction.

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