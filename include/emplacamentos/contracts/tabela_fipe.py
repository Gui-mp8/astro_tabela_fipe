from pydantic import BaseModel

class TabelaFipe(BaseModel):
    valor: str
    marca: str
    modelo: str
    ano_modelo: str
    combustivel: str
    codigo_fipe: str
    mes_referencia: str
    extraction_date: str

    class Config:
        from_attributes = True
