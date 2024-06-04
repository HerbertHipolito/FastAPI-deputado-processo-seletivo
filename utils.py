from schemas.discurso import Discurso
from typing import List

def contem_palavras_especial(texto: str, palavras_filtrar: set) -> bool:
    return any(palavra in texto.lower() for palavra in palavras_filtrar)

# Filtrar os elementos com base nas palavras-chave
def filtrar_array(array:List[Discurso],palavras_especial:str) -> List[Discurso]:

    palavras_especial = palavras_especial.split(',')
    return [elemento for elemento in array if contem_palavras_especial(elemento['transcricao'], palavras_especial)]
