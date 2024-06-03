from fastapi import APIRouter, HTTPException
from schemas.deputado import Deputado
from schemas.discurso import Discurso
from schemas.ordemTipo import ordemTipo
from pydantic import BaseModel,validator
from datetime import date, datetime
from typing import List

from fastapi import FastAPI

import requests

url = "https://dadosabertos.camara.leg.br/api/v2/deputados"
router = APIRouter()

#add paginacao

@router.get("/deputados")
#achar um jeito de remover elementos nulos antes de enviar a resposta ao usuário
def deputados(
    nome: str | None = None,
    siglaSexo: str | None = None,
    itens: int | None = None,
    ordernar: ordemTipo | None = None
    ) -> List[Deputado]:

    new_url = url+'?'

    if nome is not None: new_url+=f'nome={nome}&'    
    if siglaSexo is not None: new_url+=f'siglaSexo={siglaSexo}&'    
    if itens is not None: new_url+=f'itens={itens}&'    
    if ordernar is not None: new_url+=f"ordem={ordernar.value}&"
    print(new_url)
    response = requests.get(new_url)
    
    if response.status_code == 400:
        raise HTTPException(
            status_code=400, detail=f"Solicitação enviada pelo usuário inválida"
        )
    print(response)
    deputados_dados = response.json()['dados']

    if len(deputados_dados) == 0:
        raise HTTPException(
            status_code=403, detail=f"Deputado não achado com base nos parametros passados "
        )

    for deputado in deputados_dados:
        del deputado['uri'] 
        del deputado['uriPartido']
        
    #print(response.json())
    return deputados_dados 

@router.get("/deputados/{deputado_id}")
def deputado(deputado_id:str)-> Deputado:

    response = requests.get(url+f"/{deputado_id}")
    if response.status_code == 400:
        raise HTTPException(
            status_code=400, detail=f"Solicitação enviada pelo usuário inválida"
        )
    if response.status_code == 403: 
        raise HTTPException(
            status_code=403, detail=f"Deputado não achado usando id {deputado_id=}"
        )
    deputado_dados = response.json()['dados']['ultimoStatus']
    
    deputado_dados['telefone'] = deputado_dados['gabinete']['telefone']

    campos_para_deletar = ['gabinete','condicaoEleitoral','descricaoStatus','data','nomeEleitoral','uri','uriPartido']
    
    for campo in campos_para_deletar:
        del deputado_dados[campo]

    return deputado_dados

@router.get("/deputados/{deputado_id}/discursos")
    #add um sistema de busca por frase ou palavra
def discursos(
    deputado_id:str,
    dataInicio:str = '2022-01-01',
    dataFim:str| None = None, 
    ordernar: ordemTipo | None = None,
    itens: int | None = None,
    )->List[Discurso]:

    parameters = ''
    # Formata a data e hora no formato desejado

    if dataInicio is not None: parameters+=f'dataInicio={dataInicio}&'    
    if dataFim is not None: parameters+=f'dataFim={dataFim}&'    
    if ordernar is not None: parameters+=f'ordem={ordernar.value}&'    
    if itens is not None: parameters+=f'itens={itens}&'    
    
    response = requests.get(url+f"/{deputado_id}/discursos?{parameters}")
    print(response)
    if response.status_code == 400:
        raise HTTPException(
            status_code=400, detail=f"Solicitação enviada pelo usuário inválida"
        )
    deputado_discursos = response.json()['dados']

    if len(deputado_discursos) == 0:
        raise HTTPException(
            status_code=403, detail=f"discurso não achado com base no id {deputado_id=}"
        )
    
    campos_para_deletar = ['dataHoraFim','faseEvento','urlTexto','urlAudio','urlVideo','uriEvento']

    for discursos in deputado_discursos:

        discursos['titulo'] = discursos['faseEvento']['titulo']
        time_formatado = datetime.strptime(discursos['dataHoraInicio'], "%Y-%m-%dT%H:%M")
        discursos['dataHoraInicio'] = time_formatado.strftime("%d/%m/%Y às %H:%M")

        for campo in campos_para_deletar:
            del discursos[campo]

    return deputado_discursos
