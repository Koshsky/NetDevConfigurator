"""Localization package for the application."""

import importlib
import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)

# Словарь для хранения переводов
translations: Dict[str, Dict[str, Any]] = {}


def load_translations(lang: str):
    """Load translations for the specified language.

    Args:
        lang: Language code (e.g., 'en', 'ru')
    """
    try:
        module = importlib.import_module(f"locales.{lang}.strings")
        translations[lang] = module
        logger.debug("Loaded translations for language: %s", lang)
    except ImportError as e:
        logger.error("Failed to load translations for language %s: %s", lang, e)
        raise


def get_string(lang: str, section: str, key: str) -> str:
    """Get a translated string.

    Args:
        lang: Language code
        section: Section name (e.g., 'TABS', 'CONNECTION')
        key: Key in the section

    Returns:
        Translated string
    """
    if lang not in translations:
        load_translations(lang)

    try:
        return getattr(translations[lang], section)[key]
    except (KeyError, AttributeError) as e:
        logger.error(
            "Translation not found for %s.%s in language %s: %s", section, key, lang, e
        )
        return f"Missing translation: {section}.{key}"
