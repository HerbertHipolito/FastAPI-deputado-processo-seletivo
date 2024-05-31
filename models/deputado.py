from pydantic import BaseModel, Field, constr, conint
from typing import Optional

class Deputado(BaseModel):
    nome:str
    id:int
    idLegislatura:int
    telefone:Optional[str] = None
    siglaUf:str
    siglaPartido:str
    urlFoto:str
    email:str 
    situacao:Optional[str] = None

#criar uriPartido
#criar uriDiscursos