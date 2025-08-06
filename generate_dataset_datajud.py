import requests
import pandas as pd
import time
import os
from datetime import datetime

# Parâmetros da query da API

TRIBUNAL_SIGLA = "TJSC"
CIDADE_NOME = "Tubarão"
CIDADE_IBGE_CODIGO = "4218707" # Utilizar código da cidade/comarca segundo o site do IBGE
VARA_NOME = "1ª Vara Cível" # Utilizar nome segundo o site da comarca do Tribunal

NOME_ARQUIVO_SAIDA = f"dataset_{TRIBUNAL_SIGLA}_{CIDADE_NOME}_{VARA_NOME.replace(' ', '_').replace(',', '')}.csv"

# Parâmetros de configuração da chamada na API

API_KEY = os.getenv("DATAJUD_API_KEY")
ENDPOINT_URL = f"https://api-publica.datajud.cnj.jus.br/api_publica_{TRIBUNAL_SIGLA.lower()}/_search"
HEADERS = {
    "Authorization": f"APIKey {API_KEY}",
    "Content-Type": "application/json"
}

# Função de coleta dos dados na API usando lógica de paginação com o parâmetro search_after

def coletar_processos(query):

    print("Iniciando coleta de dados da API com o método search_after...")
    
    query['sort'] = [
            {
                "@timestamp":{
                    "order": "asc"
                }
            }
            ]
    query['size'] = 10000

    todos_os_processos = []
    last_sort_value = None

    while True:

        if last_sort_value:
            query["search_after"] = last_sort_value
        
        try:
            response = requests.post(ENDPOINT_URL, headers=HEADERS, json=query, timeout=120)
            response.raise_for_status()
            response_data = response.json()
        except requests.exceptions.RequestException as e:
            print(f"ERRO: A requisição falhou. Causa: {e}")
            break

        hits = response_data.get("hits", {}).get("hits", [])
        
        if not hits:
            break
            
        for hit in hits:
            todos_os_processos.append(hit['_source'])
        
        last_sort_value = hits[-1].get("sort")

        total_coletados = len(todos_os_processos)
        total_estimado = response_data.get("hits", {}).get("total", {}).get("value", 0)
        print(f"Coletados {total_coletados} de aproximadamente {total_estimado} processos...")
        
        time.sleep(1)

    print(f"Coleta finalizada. Total de {len(todos_os_processos)} processos brutos encontrados.")
    return todos_os_processos

# Função de processamento dos dados coletados e organização em .csv

def processar_e_salvar_csv(dados_brutos, nome_arquivo):

    print("\nIniciando processamento e criação do dataset...")
    if not dados_brutos:
        print("Nenhum dado para processar.")
        return
    dataset_limpo = []
    for processo in dados_brutos:
        classe = processo.get('classe', {})
        orgao = processo.get('orgaoJulgador', {})
        assuntos = processo.get('assuntos', [])
        movimentos = processo.get('movimentos', [])
        nomes_assuntos = "|".join([
            assunto.get('nome', '') 
            for assunto in assuntos 
            if isinstance(assunto, dict)
        ]) if assuntos else ""
        duracao_dias = None
        if movimentos:
            datas_movimentos = [
                datetime.fromisoformat(mov.get('dataHora').replace('Z', '+00:00'))
                for mov in movimentos if mov and mov.get('dataHora')
            ]
            if datas_movimentos:
                data_final = max(datas_movimentos)
                data_inicial = min(datas_movimentos)
                duracao_dias = (data_final - data_inicial).days
        linha = {
            "numero_processo": processo.get('numeroProcesso'),
            "data_ajuizamento": processo.get('dataAjuizamento'),
            "tribunal": processo.get('tribunal'),
            "grau": processo.get('grau'),
            "nivel_sigilo": processo.get('nivelSigilo'),
            "classe_codigo": classe.get('codigo') if classe else None,
            "classe_nome": classe.get('nome') if classe else None,
            "orgao_julgador_codigo": orgao.get('codigo') if orgao else None,
            "orgao_julgador_nome": orgao.get('nome') if orgao else None,
            "municipio_ibge": orgao.get('codigoMunicipioIBGE') if orgao else None,
            "assuntos_nomes": nomes_assuntos,
            "duracao_processo_dias": duracao_dias
        }
        dataset_limpo.append(linha)
    df = pd.DataFrame(dataset_limpo)
    df.to_csv(nome_arquivo, index=False, encoding='utf-8-sig')
    print(f"\nDataset salvo com sucesso como '{nome_arquivo}'.")
    print(f"O dataset contém {len(df)} linhas e {len(df.columns)} colunas.")

# Execução

if __name__ == "__main__":
    if not API_KEY:
        print("ERRO CRÍTICO: A chave da API não foi encontrada.")
    else:
        query_vara_especifica = {
            "query": {
                "bool": {
                    "must": [
                        {"match": {"orgaoJulgador.codigoMunicipioIBGE": CIDADE_IBGE_CODIGO}},
                        {"match_phrase": {"orgaoJulgador.nome": VARA_NOME}}
                    ]
                }
            }
        }
        
        dados_coletados = coletar_processos(query_vara_especifica)
        
        if dados_coletados:
            processar_e_salvar_csv(dados_coletados, NOME_ARQUIVO_SAIDA)