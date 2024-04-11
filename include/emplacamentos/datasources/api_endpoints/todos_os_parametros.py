from datetime import datetime
from typing import List, Dict, Any

import asyncio
from aiohttp import ClientSession

from include.emplacamentos.contracts.tabela_fipe import TabelaFipe
from include.emplacamentos.interfaces.asyncio_endpoints import IAsyncEndpoint

class ConsultarValorComTodosParametros(IAsyncEndpoint):
    def __init__(self) -> None:
        self.mes_referencia = None

    def task_list(self, session: ClientSession) -> list and str:
        """
            This method returns a list of tasks for each fipe code to be conclued using
            asyncio

            Args:
                session (ClientSession): it's an aiohttp class

            Returns:
                list: It's the task list
                str: it's a string that represents the actual month of the extraction
        """
        tasks = []
        for index, row in self.dataframe.iterrows():
        # for code in fipe_codes:
            # print(f"Working on fipe code: {row.iloc[4]}")
            payload = {
                'codigoTabelaReferencia': f'{row.iloc[3]}',
                'codigoMarca': '',
                'codigoModelo': '',
                'codigoTipoVeiculo': '1',
                'anoModelo': f'{row.iloc[1]}',
                'codigoTipoCombustivel': f'{row.iloc[2]}',
                'tipoVeiculo': 'carro',
                'modeloCodigoExterno': f'{row.iloc[4]}',
                'tipoConsulta': 'codigo'
            }
            self.mes_referencia = row.iloc[5]

            tasks.append(session.post(self.endpoint_url, data=payload, ssl=False))

        return tasks

    async def get_endpoint_data(self) -> List[Dict[str, Any]]:
        """
            This method gets the endpoint data for each task in a task list and
            pass it to a list.
        """
        data = []
        async with ClientSession() as session:
            tasks = self.task_list(session)  # Unpack the return values
            responses = await asyncio.gather(*tasks)
            for response in responses:
                if response.status == 200:
                    json_data = await response.json()
                    data.append(json_data)
                else:
                    print(f"Skippiped")

        return data

    def validated_data(self) -> List[Dict[str, Any]]:

        validated_data = []
        json_data = asyncio.run(self.get_endpoint_data())
        for item in json_data:
            carro = TabelaFipe(
            valor=item["Valor"].split(" ")[1].replace(".", "").replace(',', '.'),
            marca=item["Marca"],
            modelo=item["Modelo"],
            ano_modelo=str(item["AnoModelo"]),
            combustivel=item["Combustivel"],
            codigo_fipe=item["CodigoFipe"],
            mes_referencia=self.mes_referencia,
            extraction_date=datetime.now().strftime("%Y-%m-%d")
        )
            validated_data.append(carro.model_dump())

        return validated_data
