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
    email:str | None = None
    situacao:Optional[str] = None

#criar uriPartido
#criar uriDiscursos