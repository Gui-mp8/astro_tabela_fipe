from datetime import datetime
from typing import List, Dict, Any

import asyncio
from aiohttp import ClientSession

from include.emplacamentos.contracts.ano_modelo import AnoModelo
from include.emplacamentos.interfaces.asyncio_endpoints import IAsyncEndpoint

class ConsultarAnoModeloPeloCodigoFipe(IAsyncEndpoint):
    def __init__(self, **kwargs) -> None:
        self.codigo_tabela_referencia = kwargs.get("codigo_tabela_referencia")
        self.mes_referencia = kwargs.get("mes_referencia")

    def task_list(self, session: ClientSession) -> list:
        tasks = []

        for index, row in self.dataframe.iterrows():
            print(f"Working on fipe code: {row.iloc[0]}")
            payload = {
                'codigoTipoVeiculo': '1',
                'codigoTabelaReferencia': self.codigo_tabela_referencia,
                'codigoModelo': '',
                'codigoMarca': '',
                'ano': '',
                'codigoTipoCombustivel': '',
                'anoModelo': '',
                'tipoVeiculo': '',
                'modeloCodigoExterno': f'{row.iloc[0]}',
            }
            request = session.post(self.endpoint_url, data=payload, ssl=False)
            tasks.append(
                {
                    "task": request,
                    "fipe_code": row.iloc[0]
                }
            )
        return tasks

    async def get_endpoint_data(self) -> List[Dict[str, Any]]:
        data = []
        async with ClientSession() as session:
            tasks = self.task_list(session)
            awaiting_tasks = [(task['task'], task['fipe_code']) for task in tasks] # list of tuples

            responses = await asyncio.gather(*[task[0] for task in awaiting_tasks])
            for response, fipe_code in zip(responses, [task[1] for task in awaiting_tasks]):
                if response.status == 200:
                    json_data = await response.json()
                    for item in json_data:
                        item["codigo_fipe"]=fipe_code
                        data.append(item)
                else:
                    print("Skipping response")
        return data

    def validated_data(self) -> List[Dict[str, Any]]:
        validated_data = []
        json_data = asyncio.run(self.get_endpoint_data())
        for item in json_data:
            carro = AnoModelo(
            value=item["Value"],
            ano_modelo=item["Value"].split("-")[0],
            codigo_tipo_combustivel=item["Value"].split("-")[1],
            codigo_tabela_referencia = self.codigo_tabela_referencia,
            codigo_fipe=item["codigo_fipe"],
            mes_referencia=self.mes_referencia,
            extraction_date=datetime.now().strftime("%Y-%m-%d")
            )

            validated_data.append(carro.model_dump())

        return validated_data