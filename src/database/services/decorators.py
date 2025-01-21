from functools import wraps


def transactional(func):
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
