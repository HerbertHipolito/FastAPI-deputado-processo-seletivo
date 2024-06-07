from fastapi import APIRouter, HTTPException, Query

from schemas.deputado import Deputado
from schemas.deputadoCompleto import DeputadoCompleto
from schemas.discurso import Discurso
from schemas.ordemTipo import ordemTipo
from schemas.despesa import Despesa

from controllers.utils import solicitacao_erro, entidade_nao_encontrada

from typing import List
from utils import filtrar_array, agrupar_despesas
from datetime import datetime

import requests

url = "https://dadosabertos.camara.leg.br/api/v2/deputados"
router = APIRouter()

@router.get("/deputados",
    summary="Dados dos deputados federais",
    description="Retorna dados dos deputados federais com base em um lista de parametros. Se nenhum parametro é passado, será retornado os deptuados em exercicio"
)
def deputados(
    nome: str | None = Query(None, title="Nome do deputado", description="Procura o deputado com base no nome. Não precisa ser nome completo "),
    siglaSexo: str | None = Query(None, description="Sexo do deputado a ser achado. f ou m"),
    itens: int | None = Query(None, description="Numero de itens (deputados no caso) a ser retornado"),
    ordernar: ordemTipo | None = Query(None, description="Ordenação baseado no nomes dos deputados. asc (ascendente) ou desc "),
    idLegislatura: int | None =  Query(None, description="Numero identificador da legislatura de que os parlamentares tenham participados")
    ) -> List[Deputado]:

    new_url = url+'?'

    if nome is not None: new_url+=f'nome={nome}&'    
    if idLegislatura is not None: new_url+=f'idLegislatura={idLegislatura}&'    
    if siglaSexo is not None: new_url+=f'siglaSexo={siglaSexo}&'    
    if itens is not None: new_url+=f'itens={itens}&'    
    if ordernar is not None: new_url+=f"ordem={ordernar.value}&"
    
    response = requests.get(new_url)

    solicitacao_erro(response.status_code)
    deputados_dados = response.json()['dados']
    entidade_nao_encontrada(deputados_dados,'Deputados')
    
    for deputado in deputados_dados:
        del deputado['uri'] 
        del deputado['uriPartido']
        
    return deputados_dados 

@router.get("/deputados/{deputado_id}",
    description="Retorna o deputado que corresponde ao id passado"
)
def deputado(deputado_id:str)-> DeputadoCompleto:

    response = requests.get(url+f"/{deputado_id}")

    solicitacao_erro(response.status_code)
    
    if response.status_code == 404:
        raise HTTPException(
            status_code=404, detail=f"Deputado não achado com base no parametro passado"
        )

    todos_dados = response.json()['dados']
    deputado_dados = todos_dados['ultimoStatus']
    
    deputado_dados['telefone'] = todos_dados['ultimoStatus']['gabinete']['telefone']
    deputado_dados['redeSocial'] = todos_dados['redeSocial']
    deputado_dados['municipioNascimento'] = todos_dados['municipioNascimento']
    deputado_dados['escolaridade'] = todos_dados['escolaridade']
    deputado_dados['dataNascimento'] = todos_dados['dataNascimento']
    deputado_dados['cpf'] = todos_dados['cpf']
    deputado_dados['nomeCivil'] = todos_dados['nomeCivil']

    campos_para_deletar = ['gabinete','condicaoEleitoral','descricaoStatus','data','nomeEleitoral','uri','uriPartido']
    
    for campo in campos_para_deletar:
        del deputado_dados[campo]

    return deputado_dados

@router.get("/deputados/{deputado_id}/discursos",
    summary="Discursos",
    description="Retorna os discursos do deputado que corresponde ao id passado. Caso o parametro 'dataInicio', será retornado os discursos a partir de 01/01/2022. Use o padrao YYYY-MM-DD"
)
def discursos(
    deputado_id:str,
    dataInicio:str = '2022-01-01',
    dataFim:str| None = None, 
    palavraBusca:str| None = None, 
    itens: int | None = Query(None, description="Numero de itens (discurso no caso) a ser retornado"),
    idLegislatura: int | None = Query(None, description="Numero identificador da legislatura de que o parlamentar tenham participado")
    )->List[Discurso]:

    parameters = ''

    if dataInicio is not None: parameters+=f'dataInicio={dataInicio}&'    
    if dataFim is not None: parameters+=f'dataFim={dataFim}&'    
    if idLegislatura is not None: parameters+=f'idLegislatura={idLegislatura}&'    
    if itens is not None: parameters+=f'itens={itens}&'    
    
    response = requests.get(url+f"/{deputado_id}/discursos?{parameters}")

    solicitacao_erro(response.status_code)

    deputado_discursos = response.json()['dados']

    entidade_nao_encontrada(deputado_discursos,'Discursos')

    if palavraBusca is not None: deputado_discursos = filtrar_array(deputado_discursos,palavraBusca)

    campos_para_deletar = ['dataHoraFim','faseEvento','urlTexto','urlAudio','urlVideo','uriEvento']

    for discursos in deputado_discursos:

        discursos['titulo'] = discursos['faseEvento']['titulo']
        time_formatado = datetime.strptime(discursos['dataHoraInicio'], "%Y-%m-%dT%H:%M")
        discursos['dataHoraInicio'] = time_formatado.strftime("%d/%m/%Y às %H:%M")

        for campo in campos_para_deletar:
            del discursos[campo]

    return deputado_discursos

@router.get("/deputados/{deputado_id}/despesas",
    summary="Despesas deputado",
    description="Retorna as despesas do deputado que corresponde ao id passado. Utilize mes e/ou ano para filtrar despesas"
)
def despesas(
    deputado_id:str,
    cnpjCpfFornecedor:str | None = None,
    ano:int | None = None,
    mes:int | None = None,
    itens:int | None = Query(None, description="Numero de itens a ser retornado"),
    idLegislatura: int | None = Query(None, description="Numero identificador da legislatura de que os parlamentares tenham participados")
    ) -> List[Despesa]:
    
    parameters = ''    

    if cnpjCpfFornecedor is not None: parameters+=f'dataInicio={cnpjCpfFornecedor }&'    
    if idLegislatura is not None: parameters+=f'idLegislatura={idLegislatura}&'    
    if ano is not None: parameters+=f'ano={ano}&'    
    if mes is not None: parameters+=f'mes={mes}&'    
    if itens is not None: parameters+=f'itens={itens}&'    

    response = requests.get(url+f"/{deputado_id}/despesas?{parameters}")
    
    solicitacao_erro(response.status_code)
    
    deputado_despesas = response.json()['dados']

    entidade_nao_encontrada(deputado_despesas,'Despesas')
    
    campos_para_deletar = ['codDocumento','codTipoDocumento','numDocumento','valorGlosa','numRessarcimento']
    despesas = []
    
    for discursos in deputado_despesas:

        tempo_formatado = datetime.strptime(discursos['dataDocumento'], "%Y-%m-%d")
        discursos['dataDocumento'] = tempo_formatado.strftime("%d/%m/%Y")

        for campo in campos_para_deletar:
            del discursos[campo]
        
        despesas.append(discursos)
    
    return despesas

@router.get("/deputados/{deputado_id}/despesasAgrupadas",
    summary="Despesas agrupadas",
    description="Retorna as despesas agrupadas do deputado que corresponde ao id passado. Utilize mes e/ou ano para filtrar despesas. Valores de retorno: Valor liquido acumulado, valor ee documento acumulado, quantidade de fornecedores, quantidade de despesa por tipo e por fornecedore e url dos respectivos documentos",
)
def despesas_agrupadas(
    deputado_id:str,
    ano:int | None = None,
    mes:int | None = None,
    idLegislatura: int | None = Query(None, description="Numero identificador da legislatura de que o parlamentare tenha participado")
    ):
    
    parameters = ''    

    if idLegislatura is not None: parameters+=f'idLegislatura={idLegislatura}&'    
    if ano is not None: parameters+=f'ano={ano}&'    
    if mes is not None: parameters+=f'mes={mes}&'    

    response = requests.get(url+f"/{deputado_id}/despesas?{parameters}")
    
    solicitacao_erro(response.status_code)

    deputado_despesas = response.json()['dados']

    entidade_nao_encontrada(deputado_despesas,'Despesas')

    despesas = agrupar_despesas(deputado_despesas)

    return despesas