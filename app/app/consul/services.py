import random
from dataclasses import dataclass

from flask_consulate import Consul
from injector import inject

from app.consul.exceptions import ServiceNotFoundException


@dataclass
class ServiceInstanceDTO:
    id: str = None
    address: str = None


class ServiceDiscovery:

    @inject
    def __init__(self, consul: Consul):
        self.consul = consul

    def get(self, name: str) -> ServiceInstanceDTO:
        return random.choice(self.get_all_alive(name))

    def get_all(self, name: str) -> list:
        services = self.consul.session.catalog.service(name)
        if not services:
            raise ServiceNotFoundException('Service instances not found')
        return [ServiceInstanceDTO(
            id=v.get('ServiceID'),
            address=v.get('ServiceAddress', '')
        ) for v in services]

    def get_all_alive(self, name: str) -> list:
        return [v for v in self.get_all(name) if v.id in self._get_alive_node_names(name)]

    def _get_alive_node_names(self, name: str) -> list:
        services_checks = self.consul.session.health.checks(name)
        return [v.get('ServiceID') for v in services_checks if v.get('Status') == 'passing']
