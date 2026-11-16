"""Sequent Microsystems integration."""

from SMcommonHA import Card
from SMcommonHA import setup as shared_setup

from . import data

DOMAIN = data.DOMAIN
LEGACY_DOMAIN = "SMtc"
SM_MAP = data.SM_MAP
CARD = Card(DOMAIN, LEGACY_DOMAIN, data.NAME_PREFIX, data.FULL_NAME, SM_MAP, data.API)
CONFIG_SCHEMA = shared_setup.config_schema(CARD)


async def async_setup(hass, config):
    return await shared_setup.async_setup(hass, config, CARD)


async def async_setup_entry(hass, entry):
    return await shared_setup.async_setup_entry(hass, entry, CARD)


async def async_unload_entry(hass, entry):
    return await shared_setup.async_unload_entry(hass, entry, CARD)
