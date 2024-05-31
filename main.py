from enum import Enum

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import date
from typing import List

from models.deputado import Deputado 
from models.discurso import Discurso

import requests

#api link = https://dadosabertos.camara.leg.br/swagger/api.html

app = FastAPI(
    title="Insight - Processo seletivo",
    description="Desafio do processo seletivo para vaga de Back-end Python. A API pública a ser é a https://dadosabertos.camara.leg.br/swagger/api.html",
    version="0.0.1"
)

url = "https://dadosabertos.camara.leg.br/api/v2/deputados"

class ordemTipo(str, Enum):
    ASCENDENTE = 'asc'
    DESCENDENTE = 'desc'

@app.get("/deputados")
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
    response = requests.get(new_url).json()['dados']

    if len(response) == 0:
        raise HTTPException(
            status_code=404, detail=f"Deputado não achado com base nos parametros passados "
        )
    
    for deputado in response:
        del deputado['uri'] 
        del deputado['uriPartido']
        
    #print(response.json())
    return response

@app.get("/deputados/{deputado_id}")
def deputado(deputado_id:str)-> Deputado:

    response = requests.get(url+f"/{deputado_id}")
    if response.status_code == 404: 
        raise HTTPException(
            status_code=404, detail=f"Deputado não achado usando id {deputado_id=}"
        )
    deputado_dados = response.json()['dados']['ultimoStatus']
    
    #deputado_dados['id'] = str(deputado_dados['id'])
    #deputado_dados['idLegislatura'] = str(deputado_dados['idLegislatura'])
    deputado_dados['telefone'] = deputado_dados['gabinete']['telefone']

    del deputado_dados['gabinete'] 
    del deputado_dados['condicaoEleitoral'] 
    del deputado_dados['descricaoStatus'] 
    del deputado_dados['data'] 
    del deputado_dados['nomeEleitoral'] 
    del deputado_dados['uri'] 
    del deputado_dados['uriPartido'] 

    return deputado_dados

@app.get("/deputados/{deputado_id}/discursos")
    #add um sistema de busca por frase ou palavra
    # fazer aparecer a data que ocorreu o discurso 
    # colocar o titulo
def discursos(
    deputado_id:str,
    dataInicio:date | None = None,
    dataFim:date | None = None, 
    ordernar: ordemTipo | None = None,
    itens: int | None = None,
    )->List[Discurso]:

    parameters = ''

    if dataInicio is not None: parameters+=f'dataInicio={dataInicio}&'    
    if dataFim is not None: parameters+=f'dataFim={dataFim}&'    
    if ordernar is not None: parameters+=f'ordem={Ordernar}&'    
    if itens is not None: parameters+=f'itens={itens}&'    

    response = requests.get(url+f"/{deputado_id}/discursos?{parameters}")
    print(response)    
    deputado_discursos = response.json()['dados']

    if len(deputado_discursos) == 0 or response.status_code == 404:
        raise HTTPException(
            status_code=404, detail=f"discusso não achado com base no id {deputado_id=}"
        )
    
    print(deputado_discursos)
    campos_para_deletar = ['dataHoraInicio','dataHoraFim','faseEvento','urlTexto','urlAudio','urlVideo','uriEvento']

    for discursos in deputado_discursos:

        for campo in campos_para_deletar:
            del discursos[campo]


    return deputado_discursos
