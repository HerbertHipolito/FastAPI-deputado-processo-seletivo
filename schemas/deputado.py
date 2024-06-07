from pydantic import BaseModel
from typing import Optional

class Deputado(BaseModel):
    nome:str
    id:int
    idLegislatura:int
    siglaUf:str
    siglaPartido:str
    urlFoto:str
    email:str | None = None
