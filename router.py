from fastapi import APIRouter, HTTPException

from schemas.deputado import Deputado
from schemas.discurso import Discurso
from schemas.ordemTipo import ordemTipo
from schemas.despesa import Despesa

from pydantic import BaseModel,validator
from datetime import date, datetime
from typing import List
from utils import filtrar_array

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
    ordernar: ordemTipo | None = None,
    idLegislatura: int | None = None
    ) -> List[Deputado]:

    new_url = url+'?'

    if nome is not None: new_url+=f'nome={nome}&'    
    if idLegislatura is not None: new_url+=f'idLegislatura={idLegislatura}&'    
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
def discursos(
    deputado_id:str,
    dataInicio:str = '2022-01-01',
    dataFim:str| None = None, 
    palavraBusca:str| None = None, 
    ordernar: ordemTipo | None = None,
    itens: int | None = None,
    idLegislatura: int | None = None
    )->List[Discurso]:

    parameters = ''

    if dataInicio is not None: parameters+=f'dataInicio={dataInicio}&'    
    if dataFim is not None: parameters+=f'dataFim={dataFim}&'    
    if idLegislatura is not None: parameters+=f'idLegislatura={idLegislatura}&'    
    if ordernar is not None: parameters+=f'ordem={ordernar.value}&'    
    if itens is not None: parameters+=f'itens={itens}&'    
    
    response = requests.get(url+f"/{deputado_id}/discursos?{parameters}")

    print(response)
    if response.status_code == 400:
        raise HTTPException(
            status_code=400, detail=f"Solicitação enviada pelo usuário inválida"
        )
    deputado_discursos = response.json()['dados']

    if palavraBusca is not None: deputado_discursos = filtrar_array(deputado_discursos,palavraBusca)

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

@router.get("/deputados/{deputado_id}/despesas")
def despesas(
    deputado_id:str,
    cnpjCpfFornecedor:str | None = None,
    ano:int | None = None,
    mes:int | None = None,
    itens:int| None = None,
    ordernar: ordemTipo | None = None,
    idLegislatura: int | None = None
    ) -> List[Despesa]:
    
    #fazer as funções de agregação

    parameters = ''    

    if cnpjCpfFornecedor is not None: parameters+=f'dataInicio={cnpjCpfFornecedor }&'    
    if idLegislatura is not None: parameters+=f'idLegislatura={idLegislatura}&'    
    if ano is not None: parameters+=f'ano={ano}&'    
    if mes is not None: parameters+=f'mes={mes}&'    
    if ordernar is not None: parameters+=f'ordem={ordernar.value}&'    
    if itens is not None: parameters+=f'itens={itens}&'    

    response = requests.get(url+f"/{deputado_id}/despesas?{parameters}")
    print(response)
    if response.status_code == 400:
        raise HTTPException(
            status_code=400, detail=f"Solicitação enviada pelo usuário inválida"
        )
    print(response.json())    
    deputado_despesas = response.json()['dados']

    if len(deputado_despesas) == 0:
        raise HTTPException(
            status_code=403, detail=f"discurso não achado com base no id {deputado_id=}"
        )
    
    campos_para_deletar = ['codDocumento','codTipoDocumento','numDocumento','valorGlosa','numRessarcimento']
    despesas = []
    
    for discursos in deputado_despesas:

        tempo_formatado = datetime.strptime(discursos['dataDocumento'], "%Y-%m-%d")
        discursos['dataDocumento'] = tempo_formatado.strftime("%d/%m/%Y")

        for campo in campos_para_deletar:
            del discursos[campo]
        
        despesas.append(discursos)
    
    return despesas
