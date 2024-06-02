from pydantic import BaseModel, Field, constr, conint
from datetime import date
from typing import Optional

class Discurso(BaseModel):
    transcricao:str
    keywords: str | None = None
    tipoDiscurso: str | None = None
    titulo: str | None = None
    dataHoraInicio: str | None = None
