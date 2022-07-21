import logging
from spaceone.core.manager import BaseManager
from spaceone.core.utils import random_string
from spaceone.monitoring.model.event_response_model import EventModel
from spaceone.monitoring.error.event import *

_LOGGER = logging.getLogger(__name__)
DEFAULT_TITLE = 'Generate Notification'


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

            event_dict = {
                'event_key': self._generate_event_key(data.get('run_id')),
                'event_type': 'ALERT',
                'severity': self._set_severity(data.get('run_status')),
                'resource': {},
                'description': self._set_description(data),
                'title': self._set_title(data),
                'rule': '',
                'occurred_at': data.get('run_created_at', ''),
                'additional_info': self._set_additional_info(data)
            }

            event_model = EventModel(event_dict, strict=False)
            event_model.validate()
            return [event_model.to_native()]

        except Exception as e:
            raise ERROR_EVENT_PARSE()

    @staticmethod
    def _generate_event_key(run_id):
        if run_id:
            return run_id
        else:
            return random_string()

    @staticmethod
    def _set_severity(run_status):
        severity = 'INFO'

        if run_status and run_status.lower() == 'errored':
            severity = 'ERROR'

        return severity

    @staticmethod
    def _set_title(data):
        notifications = data.get('notifications', [])

        if notifications:
            _notification = notifications[0]
            message = f'[Terraform Cloud] {_notification.get("message", DEFAULT_TITLE)}'
        else:
            message = f'[Terraform Cloud] {DEFAULT_TITLE}'

        if data.get('workspace_name'):
            message = f'{message} in Workspace "{data["workspace_name"]}"'

        return message

    @staticmethod
    def _set_description(data):
        description = ""
        notifications = data.get('notifications', [])
        _notification = None

        if notifications:
            _notification = notifications[0]
            description = f'{_notification.get("message", "")}\n\n'

        if data.get('organization_name'):
            description = f'{description} - Organization Name: {data["organization_name"]}\n'

        if data.get('workspace_name'):
            description = f'{description} - Workspace Name: {data["workspace_name"]}\n'

        if data.get('run_id'):
            description = f'{description} - Run ID: {data["run_id"]}\n'

        if _notification and _notification.get('run_status'):
            description = f'{description} - Run Status: {_notification.get("run_status")}\n'

        if data.get('run_created_by'):
            description = f'{description} - Run By: {data["run_created_by"]}\n'

        if data.get('run_url'):
            description = f'{description} - Run URL: {data["run_url"]}\n'

        return description

    @staticmethod
    def _set_additional_info(data):
        info = {}

        if data.get('organization_name'):
            info.update({'organization_name': data['organization_name']})

        if data.get('workspace_id'):
            info.update({'workspace_id': data['workspace_id']})

        if data.get('workspace_name'):
            info.update({'workspace_name': data['workspace_name']})

        if data.get('notification_configuration_id'):
            info.update({'notification_configuration_id': data['notification_configuration_id']})

        if data.get('run_url'):
            info.update({'run_url': data['run_url']})

        return info
