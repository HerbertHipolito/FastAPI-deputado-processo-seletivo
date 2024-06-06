from typing import List
from fastapi import HTTPException

def solicitacao_erro(status_code:str):
    if status_code == 400:
        raise HTTPException(
            status_code=400, detail=f"Solicitação enviada pelo usuário inválida"
        )

def entidade_nao_encontrada(array: List | None = None,elemento:str = ''):
    if len(array) == 0:
        raise HTTPException(
            status_code=404, detail=f"{elemento} não achado com base nos parametros passados"
        )