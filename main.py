from enum import Enum

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import date
from typing import List

from models.deputado import Deputado 
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

@app.get("/")
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
    print(response)
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