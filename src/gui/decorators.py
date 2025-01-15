from functools import wraps

from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from database.services import EntityNotFoundError


def error_handler(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except EntityNotFoundError as e:
            self.show_error("EntityNotFoundError", e)
        except IntegrityError as e:
            self.show_error("IntegrityError", e)
            self.app.session.rollback()
        except SQLAlchemyError as e:
            self.show_error("SQLAlchemyError", e)
            self.app.session.rollback()
        except Exception as e:
            self.show_error(type(e).__name__, e)
            self.app.session.rollback()

    return wrapper


def apply_error_handler(cls):
    for attr_name, attr_value in cls.__dict__.items():
        if callable(attr_value):
            setattr(cls, attr_name, error_handler(attr_value))
    return cls
