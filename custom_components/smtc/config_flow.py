"""Configuration flow for the card."""

from homeassistant.core import callback
from SMcommonHA.config_flow import SequentConfigFlow as SharedConfigFlow
from SMcommonHA.config_flow import SequentOptionsFlow

from . import CARD, DOMAIN


class SequentConfigFlow(SharedConfigFlow, domain=DOMAIN):
    """Configure this card."""

    card = CARD

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return SequentOptionsFlow(CARD)
