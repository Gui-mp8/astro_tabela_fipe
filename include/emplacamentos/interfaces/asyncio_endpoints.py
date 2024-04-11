from abc import ABC, abstractmethod
from typing import List, Dict, Any
from pandas import DataFrame

from aiohttp import ClientSession

class IAsyncEndpoint(ABC):
    def __init__(self) -> None:
        self._endpoint_url = "https://veiculos.fipe.org.br/api/veiculos/"
        self._dataframe = None

    @property
    def endpoint_url(self) -> str:
        return self._endpoint_url

    @endpoint_url.setter
    def endpoint_url(self, endpoint: str):
        self._endpoint_url = "https://veiculos.fipe.org.br/api/veiculos/" + endpoint

    @property
    def dataframe(self) -> DataFrame:
        return self._dataframe

    @dataframe.setter
    def dataframe(self, df: DataFrame):
        self._dataframe = df

    @abstractmethod
    def task_list(self, session:ClientSession) -> list:
        pass

    @abstractmethod
    async def get_endpoint_data(self) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def validated_data(self) -> List[Dict[str, Any]]:
        pass
