import logging

from .templates import TemplateTab

logger = logging.getLogger(__name__)


class InterfacesTab(TemplateTab):
    """Displays and manages interface configurations.

    Provides a tab for configuring network interfaces, inheriting from TemplateTab
    and filtering for interface-specific templates.
    """

    def __init__(self, parent, name, **kwargs):
        """Initializes the InterfacesTab.

        Args:
            parent: The parent widget.
            name: The name of the tab.
        """
        logger.debug("Initializing InterfacesTab...")
        super().__init__(parent, name, **kwargs)
        self._template_filter = lambda x: x["type"] == "interface"
        logger.debug("InterfacesTab initialized successfully.")

    def update_config(self):
        """Updates the interface configuration."""
        logger.debug("Updating InterfacesTab configuration...")
        super().update_config()
        logger.debug("InterfacesTab configuration updated successfully.")
