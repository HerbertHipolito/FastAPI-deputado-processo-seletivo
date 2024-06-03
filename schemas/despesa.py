from pydantic import BaseModel

class Despesa(BaseModel):
    ano:int
    mes:int
    tipoDespesa:str | None = None
    dataDocumento:str
    valorDocumento:float
    valorLiquido:float
    codLote:int | None = None
    parcela:int = 0
    nomeFornecedor: str | None = None
    urlDocumento: str | None = None
