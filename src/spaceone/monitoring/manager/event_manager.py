import logging
import hashlib
from datetime import datetime

from spaceone.core.manager import BaseManager
from spaceone.monitoring.model.event_response_model import EventModel
from spaceone.monitoring.error.event import *

_LOGGER = logging.getLogger(__name__)


class EventManager(BaseManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def parse(self, options, data):
        """ data sample
            "event": {}
        """
        try:
            _LOGGER.debug("-----")
            _LOGGER.debug(data)
            _LOGGER.debug("-----")
            return []
        except Exception as e:
            raise ERROR_EVENT_PARSE()
