# O projeto pega a planilha de controle de férias da empresa e transforma em um painel que mostra quem está com férias vencidas ou perto de vencer.

# Recursos da página:

## indicadores (empregados, períodos, vencidas, a vencer)
## gráficos por situação, por gestor e por mês do prazo limite
## lista de atenção imediata, ordenada por quem vence primeiro
## filtros por data de referência, gestor, situação e busca por nome do empregado (filtro vazio = mostra todos)
## download do CSV filtrado

#  Como atualizar os dados

## O dashboard lê o banco, e não o CSV. Depois de mudar a planilha:

## Salve a planilha como CSV e substitua o arquivo data/ferias.csv.
## Rode python etl.py de novo (ele recria a tabela, sem duplicar linhas).
## No navegador, aperte C → Clear cache e depois Rerun (ou reinicie o dashboard).

# Cuidados ao editar a planilha:

 ## Não mude os nomes das colunas. O código depende deles.
 ## Mantenha o formato das datas (mês/dia/ano, como 5/3/2018 = 3 de maio).
 ## Se o Excel em português exportar com ponto e vírgula e datas dia/mês/ano, ajuste no config.py:

# Como rodar (Windows / PowerShell)
 ## Abra o terminal na pasta do projeto (no VS Code: Ctrl + ').
 ## Crie o ambiente virtual (só na primeira vez):
 ## powershell
   ## python -m venv .venv
 ## Ative o ambiente virtual:
 ## powershell
    ## .venv\Scripts\activate

 ##  Deve aparecer (.venv) no começo da linha.

 ## Instale as bibliotecas (só na primeira vez):
 ## powershell
   ##  pip install -r requirements.txt
 ## Rode o ETL (cria e preenche o banco):
 ## powershell
    ## python etl.py
 ## Deve aparecer algo como:

    ## [Extract] 136 linhas e 17 colunas lidas.
    ## [Transform] 136 linhas após a limpeza.
    ## [Load] 136 linhas enviadas; 136 linhas na tabela 'ferias'.
 ## Abra o dashboard:
 ## powershell
    ## -streamlit run dashboard.py

 ## O navegador abre em http://localhost:8501.

 ## Para encerrar: Ctrl + C no terminal. Para sair do ambiente virtual: deactivate.
