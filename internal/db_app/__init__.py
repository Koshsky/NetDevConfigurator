from .database_app import DatabaseApp
from .connection_tab import ConnectionTab
from .base_tab import BaseTab, RetrievalError

from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import SQLAlchemyError  # base SQL exception

def error_handler(func):
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