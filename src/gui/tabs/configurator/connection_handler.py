import logging
from typing import Dict, Type

from config import config
from drivers import ConnectionManager
from locales import get_string
from utils.environ import get_env, set_env

from ..base_tab import BaseTab

CONNECTION_TYPES = ("COM", "SSH", "MOCK")

logger = logging.getLogger("gui")


class ConnectionHandlerFactory:
    """Factory for creating connection handlers based on connection type."""

    def __init__(self, tab: BaseTab):
        self.tab = tab
        self.handlers: Dict[str, Type[BaseConnectionHandler]] = {
            "COM": ComConnectionHandler,
            "SSH": SSHConnectionHandler,
            "MOCK": MockConnectionHandler,
        }

    def create_handler(self) -> "BaseConnectionHandler":
        """Creates and returns a connection handler based on the CONNECTION_TYPE environment variable.

        Returns:
            BaseConnectionHandler: The created connection handler.

        Raises:
            ValueError: If the connection type is unknown.
        """
        conn_type = get_env("CONNECTION_TYPE")
        if not conn_type:
            raise ValueError("CONNECTION_TYPE environment variable not set.")

        handler_class = self.handlers.get(conn_type)
        if not handler_class:
            raise ValueError(f"Unknown connection type: {conn_type}")

        logger.debug(f"Creating connection handler of type: {conn_type}")
        return handler_class(self.tab)


class BaseConnectionHandler:
    """Base class for connection handlers."""

    def __init__(self, control_tab: BaseTab):
        """Initialize the connection handler.

        Args:
            control_tab: The parent tab widget.
        """
        self.tab = control_tab
        self.app = control_tab.app
        self.lang = control_tab.app.lang
        self.logger = logging.getLogger(__name__)
        self.connection_title = get_string(self.lang, "CONNECTION", "TITLE")

        self.env_vars: Dict[str, Dict[str, str]] = [
            "HOST_ADDRESS",
            "HOST_PORT",
            "HOST_USERNAME",
            "HOST_PASSWORD",
        ]

    def load_configuration(self):
        """Loads the configuration from the device."""
        self.app.prepare_configuration()
        return self.update_startup_config()

    def update_envs(self):
        """Updates host information based on user input."""
        logger.debug("Updating host info...")
        if not self.fields:
            return
        for var_name in self.env_vars:
            field = get_string(self.lang, "CONNECTION", var_name)
            value = self.fields[field].get().strip()
            if set_env(var_name, value):
                set_env("BASE_LOADED", "false")

    def actualize_values(self):
        """Actualize values from the connection handler."""
        logger.debug("Actualizing connection values...")
        for var_name in self.env_vars:
            field = get_string(self.lang, "CONNECTION", var_name)
            if field in self.tab.fields[self.connection_title]:
                value = get_env(var_name)
                if value:
                    self.fields[field].set(value)

    def create_widgets(self):
        """Creates widgets for connection parameters."""
        self.tab.create_block(
            get_string(self.lang, "CONNECTION", "TITLE"),
            {
                get_string(self.lang, "CONNECTION", field): tuple(
                    getattr(config.host, field.split("_")[1].lower())
                )
                for field in self.env_vars
            },
        )
        self.fields = self.tab.fields[self.connection_title]

    def __getattr__(self, name: str):
        """Dynamically handles SSH driver methods."""
        if hasattr(ConnectionManager, name):

            def dynamic_method(*args):
                return self._execute_with_driver(operation=name, *args)

            return dynamic_method
        raise AttributeError(
            f"'{self.__class__.__name__}' object has no attribute '{name}'"
        )

    def _execute_with_driver(self, operation: str, connection_type: str, *args):
        """Executes an operation using the specified driver.

        Args:
            operation: The name of the operation to execute.
            Driver: The driver class to use. Defaults to SSHDriver.

        Raises:
            Exception: Any exception raised by the driver.
        """
        self.app.update_envs()
        if get_env("ADVANCED_MODE") == "true":
            self.tab.display_feedback(
                f"Please wait, executing {operation} via {connection_type}..."
            )

        try:
            with ConnectionManager(
                self.app.device, connection_type, **self.app.driver
            ) as conn:
                method = getattr(conn, operation)
                result = method(*args)
                if isinstance(result, str) and get_env("ADVANCED_MODE") == "true":
                    self.tab.display_feedback(result)
                return result
        except Exception as e:
            logger.exception(
                f"Error executing operation '{operation}' with driver: {e}"
            )
            self.app.tabs["CONTROL"].show_error(type(e).__name__, e)
            raise


class ComConnectionHandler(BaseConnectionHandler):
    """Connection handler for COM connections."""

    def __init__(self, control_tab: BaseTab):
        super().__init__(control_tab)
        self.env_vars = [
            "HOST_USERNAME",
            "HOST_PASSWORD",
        ]

    def _execute_with_driver(self, operation: str, *args):
        """Executes an operation, configuring the base connection if necessary."""
        if get_env("BASE_LOADED") == "false":
            try:
                super()._execute_with_driver(
                    "base_configure_192", connection_type="COM"
                )
            except Exception:
                logger.exception("Error during base configuration.")
                raise
            else:
                set_env("BASE_LOADED", "true")
        return super()._execute_with_driver(operation, connection_type="COM", *args)


class MockConnectionHandler(BaseConnectionHandler):
    """Connection handler for mock connections."""

    def __init__(self, control_tab: BaseTab):
        super().__init__(control_tab)

    def _execute_with_driver(self, operation: str, *args):
        """Executes an operation using the MockDriver."""
        return super()._execute_with_driver(operation, connection_type="MOCK", *args)


class SSHConnectionHandler(BaseConnectionHandler):
    """Connection handler for SSH connections."""

    def __init__(self, control_tab: BaseTab):
        super().__init__(control_tab)

    def _execute_with_driver(self, operation: str, *args):
        """Executes an operation using the SSHDriver."""
        return super()._execute_with_driver(operation, connection_type="SSH", *args)


def get_connection_handler(tab: BaseTab) -> "BaseConnectionHandler":
    """Creates and returns a connection handler using the ConnectionHandlerFactory.

    Args:
        tab: The current tab instance.

    Returns:
        A connection handler instance.
    """
    factory = ConnectionHandlerFactory(tab)
    return factory.create_handler()
