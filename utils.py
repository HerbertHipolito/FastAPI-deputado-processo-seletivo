from schemas.discurso import Discurso
from schemas.despesa import Despesa

from typing import List

def contem_palavras_especial(texto: str, palavras_filtrar: set) -> bool:
    return any(palavra in texto.lower() for palavra in palavras_filtrar)

def filtrar_array(array:List[Discurso],palavras_especial:str) -> List[Discurso]:
    palavras_especial = palavras_especial.split(',')
    return [elemento for elemento in array if contem_palavras_especial(elemento['transcricao'], palavras_especial)]

def agrupar_despesas(despesas:List[Despesa]):

    valor_liquido_acumulado:float = 0
    tipo_despesa = dict()
    nome_fornecedor = dict()
    qtd_fornecedor:int = 0
    url_documentos:List[str] = []
    
    for despesa in despesas:

        valor_liquido_acumulado += despesa['valorLiquido']
        
        if tipo_despesa.get(despesa['tipoDespesa']) is None:
            tipo_despesa[despesa['tipoDespesa']] = despesa['valorLiquido']
        else:
            tipo_despesa[despesa['tipoDespesa']] += despesa['valorLiquido']

        if nome_fornecedor.get(despesa['nomeFornecedor']) is None:
            nome_fornecedor[despesa['nomeFornecedor']] = despesa['valorLiquido']
            qtd_fornecedor += 1
        else:
            nome_fornecedor[despesa['nomeFornecedor']] += despesa['valorLiquido']

        url_documentos.append(despesa['urlDocumento'])
    
    despesas_agrupadas = {
        'valorLiquidoAcumulado':valor_liquido_acumulado,
        'despesasPorTipo':tipo_despesa,
        'despesasFornecedor':nome_fornecedor,
        'mediaDeDespesasPorFornecedor':valor_liquido_acumulado/qtd_fornecedor,
        'quantidadeFornecedores':qtd_fornecedor,
        'url_documentos':url_documentos
    }

    return despesas_agrupadas
    