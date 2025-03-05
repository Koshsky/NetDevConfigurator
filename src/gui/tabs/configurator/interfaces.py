import logging
from typing import Any, Dict

from .templates import TemplateTab

logger = logging.getLogger(__name__)


class InterfacesTab(TemplateTab):
    """Manages interface configurations."""

    def __init__(self, parent: Any, name: str, **kwargs: Dict[str, Any]) -> None:
        """Initializes the InterfacesTab.

        Args:
            parent: The parent widget.
            name: The name of the tab.
            **kwargs: Additional keyword arguments.
        """
        logger.debug("Initializing InterfacesTab...")
        super().__init__(parent, name, **kwargs)
        self._template_filter = lambda x: x["type"] == "interface"
        logger.debug("InterfacesTab initialized successfully.")

    def update_config(self) -> None:
        """Updates the interface configuration."""
        logger.debug("Updating InterfacesTab configuration...")
        super().update_config()
        logger.debug("InterfacesTab configuration updated successfully.")
