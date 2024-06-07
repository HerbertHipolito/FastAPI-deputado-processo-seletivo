from schemas.deputado import Deputado
from typing import List

class DeputadoCompleto(Deputado):
    redeSocial:List[str]
    municipioNascimento:str
    telefone:str
    escolaridade:str
    situacao:str
    dataNascimento:str             
    nomeCivil:str               
    cpf:str