from pydantic import BaseModel

class AnoModelo(BaseModel):
    value: str
    ano_modelo: str
    codigo_tipo_combustivel: str
    codigo_tabela_referencia: int
    codigo_fipe: str
    mes_referencia: str
    extraction_date: str

    class Config:
        from_attributes = True