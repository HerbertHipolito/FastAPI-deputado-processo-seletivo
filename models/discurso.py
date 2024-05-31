from pydantic import BaseModel, Field, constr, conint
from datetime import date
from typing import Optional

class Discurso(BaseModel):
    transcricao:str
    dataInicio: Optional[date] = None
    dataFinal: Optional[date] = None
    keywords: str | None = None
    tipoDiscurso: str | None = None
