# Dashboard de Controle de Férias

## Sobre o projeto

O projeto transforma a planilha de controle de férias da empresa em um dashboard interativo, permitindo acompanhar a situação dos períodos de férias dos funcionários e identificar aqueles que estão com férias vencidas ou próximas do vencimento.

O objetivo é facilitar o acompanhamento dos prazos, auxiliar os gestores na organização das férias e evitar períodos vencidos.

## Funcionalidades

- **Indicadores:** total de empregados, períodos de férias, períodos vencidos e períodos a vencer.
- **Gráficos:** visualização dos períodos por situação, gestor e mês do prazo limite.
- **Lista de atenção imediata:** apresenta os funcionários que precisam de atenção, ordenados pelo prazo de vencimento mais próximo.
- **Filtros:** por data de referência, gestor, situação e nome do empregado.
- **Visualização completa:** quando os filtros estão vazios, todos os registros são exibidos.
- **Exportação:** download dos dados filtrados em formato CSV.

## Tecnologias utilizadas

- Python
- Streamlit
- Pandas
- SQLite
- CSV

## Como executar o projeto (Windows / PowerShell)

### 1. Abra a pasta do projeto

Abra o projeto no VS Code e acesse o terminal com `Ctrl + '`.

### 2. Crie o ambiente virtual

Execute o comando abaixo (somente na primeira execução):

```powershell
python -m venv .venv
```

### 3. Ative o ambiente virtual

```powershell
.venv\Scripts\Activate.ps1
```

Após a ativação, deverá aparecer `(.venv)` no início da linha do terminal.

### 4. Instale as dependências

Execute o comando abaixo para instalar as bibliotecas necessárias:

```powershell
pip install -r requirements.txt
```

### 5. Execute o ETL

O ETL realiza a extração, transformação e carregamento dos dados da planilha para o banco de dados.

```powershell
python etl.py
```

**Exemplo de saída esperada:**

```text
[Extract] 136 linhas e 17 colunas lidas.
[Transform] 136 linhas após a limpeza.
[Load] 136 linhas enviadas; 136 linhas na tabela 'ferias'.
```

### 6. Inicie o dashboard

```powershell
streamlit run dashboard.py
```

O navegador abrirá o dashboard no endereço:

http://localhost:8501

Para encerrar a aplicação, pressione `Ctrl + C` no terminal.

Para sair do ambiente virtual, execute:

```powershell
deactivate
```

## Como atualizar os dados

O dashboard consulta diretamente o banco de dados, e não a planilha CSV. Portanto, sempre que houver alterações na planilha original, é necessário atualizar o banco de dados.

Siga os passos:

1. Atualize a planilha de controle de férias.
2. Salve ou exporte a planilha no formato CSV.
3. Substitua o arquivo `data/ferias.csv` pelo arquivo atualizado.
4. Execute novamente o ETL:

```powershell
python etl.py
```

5. No navegador, pressione `C` para limpar o cache e depois `R` para executar novamente. Se necessário, reinicie o dashboard.

O processo de ETL recria e preenche a tabela, evitando a duplicação de registros.

## Cuidados ao editar a planilha

- **Não altere os nomes das colunas:** o código depende dos nomes definidos na planilha.
- **Mantenha o formato das datas:** o padrão esperado é mês/dia/ano (MM/DD/YYYY). Por exemplo, `5/3/2018` representa 3 de maio de 2018.
- **Formato CSV:** se o Excel estiver configurado em português, a exportação poderá utilizar ponto e vírgula (`;`) como separador e datas no formato dia/mês/ano (`DD/MM/YYYY`).

Caso isso aconteça, ajuste as configurações correspondentes no arquivo `config.py` para que o ETL consiga interpretar corretamente os dados.# Dashboard de Controle de Férias

## Sobre o projeto

O projeto transforma a planilha de controle de férias da empresa em um dashboard interativo, permitindo acompanhar a situação dos períodos de férias dos funcionários e identificar aqueles que estão com férias vencidas ou próximas do vencimento.

O objetivo é facilitar o acompanhamento dos prazos, auxiliar os gestores na organização das férias e evitar períodos vencidos.

## Funcionalidades

- **Indicadores:** total de empregados, períodos de férias, períodos vencidos e períodos a vencer.
- **Gráficos:** visualização dos períodos por situação, gestor e mês do prazo limite.
- **Lista de atenção imediata:** apresenta os funcionários que precisam de atenção, ordenados pelo prazo de vencimento mais próximo.
- **Filtros:** por data de referência, gestor, situação e nome do empregado.
- **Visualização completa:** quando os filtros estão vazios, todos os registros são exibidos.
- **Exportação:** download dos dados filtrados em formato CSV.

## Tecnologias utilizadas

- Python
- Streamlit
- Pandas
- SQLite
- CSV

## Como executar o projeto (Windows / PowerShell)

### 1. Abra a pasta do projeto

Abra o projeto no VS Code e acesse o terminal com `Ctrl + '`.

### 2. Crie o ambiente virtual

Execute o comando abaixo (somente na primeira execução):

```powershell
python -m venv .venv
```

### 3. Ative o ambiente virtual

```powershell
.venv\Scripts\Activate.ps1
```

Após a ativação, deverá aparecer `(.venv)` no início da linha do terminal.

### 4. Instale as dependências

Execute o comando abaixo para instalar as bibliotecas necessárias:

```powershell
pip install -r requirements.txt
```

### 5. Execute o ETL

O ETL realiza a extração, transformação e carregamento dos dados da planilha para o banco de dados.

```powershell
python etl.py
```

**Exemplo de saída esperada:**

```text
[Extract] 136 linhas e 17 colunas lidas.
[Transform] 136 linhas após a limpeza.
[Load] 136 linhas enviadas; 136 linhas na tabela 'ferias'.
```

### 6. Inicie o dashboard

```powershell
streamlit run dashboard.py
```

O navegador abrirá o dashboard no endereço:

http://localhost:8501

Para encerrar a aplicação, pressione `Ctrl + C` no terminal.

Para sair do ambiente virtual, execute:

```powershell
deactivate
```

## Como atualizar os dados

O dashboard consulta diretamente o banco de dados, e não a planilha CSV. Portanto, sempre que houver alterações na planilha original, é necessário atualizar o banco de dados.

Siga os passos:

1. Atualize a planilha de controle de férias.
2. Salve ou exporte a planilha no formato CSV.
3. Substitua o arquivo `data/ferias.csv` pelo arquivo atualizado.
4. Execute novamente o ETL:

```powershell
python etl.py
```

5. No navegador, pressione `C` para limpar o cache e depois `R` para executar novamente. Se necessário, reinicie o dashboard.

O processo de ETL recria e preenche a tabela, evitando a duplicação de registros.

## Cuidados ao editar a planilha

- **Não altere os nomes das colunas:** o código depende dos nomes definidos na planilha.
- **Mantenha o formato das datas:** o padrão esperado é mês/dia/ano (MM/DD/YYYY). Por exemplo, `5/3/2018` representa 3 de maio de 2018.
- **Formato CSV:** se o Excel estiver configurado em português, a exportação poderá utilizar ponto e vírgula (`;`) como separador e datas no formato dia/mês/ano (`DD/MM/YYYY`).

Caso isso aconteça, ajuste as configurações correspondentes no arquivo `config.py` para que o ETL consiga interpretar corretamente os dados.# Dashboard de Controle de Férias

## Sobre o projeto

O projeto transforma a planilha de controle de férias da empresa em um dashboard interativo, permitindo acompanhar a situação dos períodos de férias dos funcionários e identificar aqueles que estão com férias vencidas ou próximas do vencimento.

O objetivo é facilitar o acompanhamento dos prazos, auxiliar os gestores na organização das férias e evitar períodos vencidos.

## Funcionalidades

- **Indicadores:** total de empregados, períodos de férias, períodos vencidos e períodos a vencer.
- **Gráficos:** visualização dos períodos por situação, gestor e mês do prazo limite.
- **Lista de atenção imediata:** apresenta os funcionários que precisam de atenção, ordenados pelo prazo de vencimento mais próximo.
- **Filtros:** por data de referência, gestor, situação e nome do empregado.
- **Visualização completa:** quando os filtros estão vazios, todos os registros são exibidos.
- **Exportação:** download dos dados filtrados em formato CSV.

## Tecnologias utilizadas

- Python
- Streamlit
- Pandas
- SQLite
- CSV

## Como executar o projeto (Windows / PowerShell)

### 1. Abra a pasta do projeto

Abra o projeto no VS Code e acesse o terminal com `Ctrl + '`.

### 2. Crie o ambiente virtual

Execute o comando abaixo (somente na primeira execução):

```powershell
python -m venv .venv
```

### 3. Ative o ambiente virtual

```powershell
.venv\Scripts\Activate.ps1
```

Após a ativação, deverá aparecer `(.venv)` no início da linha do terminal.

### 4. Instale as dependências

Execute o comando abaixo para instalar as bibliotecas necessárias:

```powershell
pip install -r requirements.txt
```

### 5. Execute o ETL

O ETL realiza a extração, transformação e carregamento dos dados da planilha para o banco de dados.

```powershell
python etl.py
```

**Exemplo de saída esperada:**

```text
[Extract] 136 linhas e 17 colunas lidas.
[Transform] 136 linhas após a limpeza.
[Load] 136 linhas enviadas; 136 linhas na tabela 'ferias'.
```

### 6. Inicie o dashboard

```powershell
streamlit run dashboard.py
```

O navegador abrirá o dashboard no endereço:

http://localhost:8501

Para encerrar a aplicação, pressione `Ctrl + C` no terminal.

Para sair do ambiente virtual, execute:

```powershell
deactivate
```

## Como atualizar os dados

O dashboard consulta diretamente o banco de dados, e não a planilha CSV. Portanto, sempre que houver alterações na planilha original, é necessário atualizar o banco de dados.

Siga os passos:

1. Atualize a planilha de controle de férias.
2. Salve ou exporte a planilha no formato CSV.
3. Substitua o arquivo `data/ferias.csv` pelo arquivo atualizado.
4. Execute novamente o ETL:

```powershell
python etl.py
```

5. No navegador, pressione `C` para limpar o cache e depois `R` para executar novamente. Se necessário, reinicie o dashboard.

O processo de ETL recria e preenche a tabela, evitando a duplicação de registros.

## Cuidados ao editar a planilha

- **Não altere os nomes das colunas:** o código depende dos nomes definidos na planilha.
- **Mantenha o formato das datas:** o padrão esperado é mês/dia/ano (MM/DD/YYYY). Por exemplo, `5/3/2018` representa 3 de maio de 2018.
- **Formato CSV:** se o Excel estiver configurado em português, a exportação poderá utilizar ponto e vírgula (`;`) como separador e datas no formato dia/mês/ano (`DD/MM/YYYY`).

Caso isso aconteça, ajuste as configurações correspondentes no arquivo `config.py` para que o ETL consiga interpretar corretamente os dados.