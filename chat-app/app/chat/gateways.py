import requests

from app.chat.exceptions import GatewayEndpointNotFoundException
from flask import current_app


class CounterAppGateway:
    _endpoints_map = {
        'count_all': 'api/v1/user/{user_id}/chats',
        'incr': 'api/v1/chat/{chat_id}/messages/{user_id}/incr',
        'decr': 'api/v1/chat/{chat_id}/messages/{user_id}/decr',
    }

    def __init__(self):
        host = current_app.config.get('COUNTER_APP_URL')
        self.url = f'http://{host}'

    def _get_endpoint_url(self, name: str, **kwargs) -> str:
        endpoint = self._endpoints_map.get(name, False)
        if not endpoint:
            raise GatewayEndpointNotFoundException('Endpoint not found')
        return f'{self.url}/{endpoint.format_map(kwargs)}'

    def count_all(self, user_id) -> dict:
        try:
            response = requests.get(self._get_endpoint_url('count_all', user_id=user_id))
        except Exception as e:
            current_app.logger.exception(e)
            return {}

        return response.json()['items'] or {}

    def incr(self, chat_id, user_id) -> bool:
        try:
            requests.post(self._get_endpoint_url('incr', chat_id=chat_id, user_id=user_id))
        except Exception as e:
            current_app.logger.exception(e)
            return False
        return True

    def decr(self, chat_id, user_id) -> bool:
        try:
            requests.post(self._get_endpoint_url('decr', chat_id=chat_id, user_id=user_id))
        except Exception as e:
            current_app.logger.exception(e)
            return False
        return True
