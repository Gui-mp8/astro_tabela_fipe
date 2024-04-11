from abc import ABC, abstractmethod
from typing import List, Dict, Any

import requests

class IEndpoint(ABC):
    def __init__(self) -> None:
        self._endpoint_url = "https://veiculos.fipe.org.br/api/veiculos/"
        # self._payload = kwargs.get('payload', {})

    @property
    def endpoint_url(self) -> str:
        return self._endpoint_url

    @endpoint_url.setter
    def endpoint_url(self, endpoint: str) -> str:
        self._endpoint_url = "https://veiculos.fipe.org.br/api/veiculos/" + endpoint

    @abstractmethod
    def create_session(self) -> requests.Session:
        pass

    @abstractmethod
    def get_endpoint_response(self) -> requests.Response:
        pass

    @abstractmethod
    def get_endpoint_data(self) -> List[Dict[str, Any]]:
        pass