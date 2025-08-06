# Análise de Dados de Varas Judiciais com a API Datajud

Este projeto contém um script Python para coletar, processar e salvar dados de processos judiciais de uma vara específica utilizando a API pública Datajud do CNJ.

## Sobre o Projeto

O objetivo deste script é criar um dataset estruturado em formato CSV a partir de dados brutos de processos judiciais. O dataset inclui informações como classe processual, assuntos, órgão julgador e a duração do processo em dias (calculada a partir dos movimentos).

## Como Utilizar

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/gvilherme7/datajud_datasets](https://github.com/gvilherme7/datajud_datasets)
    ```

2.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure a Chave da API:**
    Este script requer uma chave da API do Datajud. Configure-a como uma variável de ambiente para maior segurança e praticidade:
    ```powershell
    $env:DATAJUD_API_KEY='SUA_CHAVE_AQUI'
    ```

4.  **Ajuste os Parâmetros:**
    Abra o script `generate_dataset_datajud.py` e edite as variáveis na seção de configuração para definir o tribunal, comarca e vara de sua escolha.
    A sigla do Tribunal e nome da vara/órgão julgador podem ser obtidos a partir do site do tribunal em questão. O nome da vara é case sensitive e deve incluir acentuações e caracteres espeiciais quando presentes.
    O código da cidade/comarca pode ser obtido no site do IBGE.

5.  **Execute o script:**
    ```bash
    python generate_dataset_datajud.py
    ```

## Datasets de Exemplo

Neste repositório, você encontrará os seguintes datasets gerados como exemplo:

* `dataset_TJSC_Tubarão_1ª_Vara_Cível.csv`: Processos judiciais (que não em segredo de justiça) em andamento na 1ª Vara Cível da Comarca de Tubarão/SC.
* `dataset_TJSC_Tubarão_Vara_da_Família_... .csv`: Processos judiciais (que não em segredo de justiça) em andamento na Vara da Família, Órfãos, Infância e Juventude da Comarca de Tubarão/SC.