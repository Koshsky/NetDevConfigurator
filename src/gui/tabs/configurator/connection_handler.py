import logging
from typing import Dict, List, Tuple, Type

from config import config
from drivers import ConnectionManager
from utils.environ import get_env, set_env

from ..base_tab import BaseTab

logger = logging.getLogger("gui")

CONNECTION_TYPES = {
    "com+ssh": "COM+SSH",
    "ssh": "SSH",
    "mock": "MOCK",
}


class ConnectionHandlerFactory:
    """Factory for creating connection handlers based on connection type."""

    def __init__(self, tab: BaseTab):
        self.tab = tab
        self.handlers: Dict[str, Type[BaseConnectionHandler]] = {
            "com+ssh": COMSSHConnectionHandler,
            "ssh": SSHConnectionHandler,
            "mock": MockConnectionHandler,
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
        self.tab = control_tab
        self.app = control_tab.app
        self.fields_config: List[str] = []
        self.env_vars: List[Tuple[str, str]] = []

    def create_widgets(self):
        """Creates widgets for connection parameters."""
        self.tab.create_block(
            "host",
            {field: tuple(getattr(config.host, field)) for field in self.fields_config},
        )
        self._actualize_values()

    def _actualize_values(self):
        """Sets initial values for connection parameters from environment variables."""
        logger.debug("Actualizing connection values...")
        for var_name, field in self.env_vars:
            if field in self.tab.fields["host"] and (value := get_env(var_name)):
                self.tab.fields["host"][field].set(value)

    def update_envs(self):
        """Updates host information based on user input."""
        logger.debug("Updating host info...")
        for var_name, field in self.env_vars:
            if field in self.tab.fields.get("host", {}):
                value = self.tab.fields["host"][field].get().strip()
                if set_env(var_name, value):
                    set_env("BASE_LOADED", "false")

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


class COMSSHConnectionHandler(BaseConnectionHandler):
    """Connection handler for COM+SSH connections."""

    def __init__(self, control_tab: BaseTab):
        super().__init__(control_tab)
        self.fields_config = ["username", "password"]
        self.env_vars = [
            ("HOST_USERNAME", "username"),
            ("HOST_PASSWORD", "password"),
        ]

    def _execute_with_driver(self, operation: str, *args):
        """Executes an operation, configuring the base connection if necessary."""
        if get_env("BASE_LOADED") == "false":
            try:
                super()._execute_with_driver(
                    "base_configure_192", connection_type="com"
                )
            except Exception:
                logger.exception("Error during base configuration.")
                raise
            else:
                set_env("BASE_LOADED", "true")
        return super()._execute_with_driver(operation, connection_type="ssh", *args)


class MockConnectionHandler(BaseConnectionHandler):
    """Connection handler for mock connections."""

    def __init__(self, control_tab: BaseTab):
        super().__init__(control_tab)
        self.fields_config = ["address", "port", "username", "password"]
        self.env_vars = [
            ("HOST_ADDRESS", "address"),
            ("HOST_PORT", "port"),
            ("HOST_USERNAME", "username"),
            ("HOST_PASSWORD", "password"),
        ]

    def _execute_with_driver(self, operation: str, *args):
        """Executes an operation using the MockDriver."""
        return super()._execute_with_driver(operation, connection_type="mock", *args)


class SSHConnectionHandler(BaseConnectionHandler):
    """Connection handler for SSH connections."""

    def __init__(self, control_tab: BaseTab):
        super().__init__(control_tab)
        self.fields_config = ["address", "port", "username", "password"]
        self.env_vars = [
            ("HOST_ADDRESS", "address"),
            ("HOST_PORT", "port"),
            ("HOST_USERNAME", "username"),
            ("HOST_PASSWORD", "password"),
        ]

    def _execute_with_driver(self, operation: str, *args):
        """Executes an operation using the SSHDriver."""
        return super()._execute_with_driver(operation, connection_type="ssh", *args)


def get_connection_handler(tab: BaseTab) -> "BaseConnectionHandler":
    """Creates and returns a connection handler using the ConnectionHandlerFactory.

    Args:
        tab: The current tab instance.

    Returns:
        A connection handler instance.
    """
    factory = ConnectionHandlerFactory(tab)
    return factory.create_handler()
