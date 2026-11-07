import re 
import unicodedata

import pandas as pd 
from sqlalchemy import create_engine , text

from config import CSV_PATH , DATE_FORMAT , DB_URL , DECIMAL , ENCODING , SEP , TABELA

COLUNAS_DATA = [
    "data_de_admissao",
    "inicio_periodo_aquisitivo",
    "fim_periodo_aquisitivo",
    "limite_para_gozo",
    "inicio_das_ferias",
    "fim_das_ferias",
    "proximo_pa_Inicio",
    "proximo_pa_fim",
    "proximo_limite_de_gozo",
]

FORMATOS_DATA = ["%m/%d/%Y", "%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y", "%Y-%m-%d %H:%M:%S"]


def converter_data(serie: pd.Series) -> pd.Series:
    """Testa vários formatos e fica com o que converte mais datas."""
    melhor, melhor_ok = None, -1
    for fmt in FORMATOS_DATA:
        conv = pd.to_datetime(serie, format=fmt, errors="coerce")
        ok = int(conv.notna().sum())
        if ok > melhor_ok:
            melhor, melhor_ok = conv, ok
    return melhor

COLUNAS_NUM = ["dias_gozados","abono_dias","saldo_de_ferias"]

def normalizar_nome(nome: str) -> str:
    """'Abono (dias)' -> 'abono_dias' | 'Início Período Aquisitivo' -> 'inicio_periodo_aquisitivo'"""
    nome = unicodedata.normalize("NFKD", str(nome))
    nome = "".join(c for c in nome if not unicodedata.combining(c))
    nome = re.sub(r"[^a-zA-Z0-9]+", "_", nome.strip().lower())
    return nome.strip("_")
 
 
def extract() -> pd.DataFrame:
    """E: lê o CSV (tenta utf-8 e, se falhar, latin-1)."""
    try:
        df = pd.read_csv(CSV_PATH, sep=SEP, decimal=DECIMAL, encoding=ENCODING)
    except UnicodeDecodeError:
        df = pd.read_csv(CSV_PATH, sep=SEP, decimal=DECIMAL, encoding="latin-1")
    print(f"[Extract] {len(df)} linhas e {len(df.columns)} colunas lidas.")
    return df
 
 
def transform(df: pd.DataFrame) -> pd.DataFrame:
    """T: limpa e padroniza os dados."""
    df.columns = [normalizar_nome(c) for c in df.columns]
 
    # remove linhas totalmente vazias e duplicadas
    df = df.dropna(how="all").drop_duplicates().copy()
 
    # texto: tira espaços sobrando (ex.: "ROGERIO OLLERMANN  MOSCARDINE" com 2 espaços)
    for col in COLUNAS_DATA:
        if col not in df.columns:
            continue
        original = df[col].astype("string").str.strip()
        df[col] = converter_data(original)
        invalidas = int((original.notna() & df[col].isna()).sum())
        if invalidas:
            print(f"[Aviso] {invalidas} data(s) inválida(s) em '{col}' viraram vazio.")
    if "status" in df.columns:
        df["status"] = df["status"].str.upper()
 
    # datas (formato mês/dia/ano) e números
    for col in COLUNAS_DATA:
        if col not in df.columns:
            continue
        original = df[col]
        df[col] = pd.to_datetime(original, format=DATE_FORMAT, errors="coerce")
        invalidas = int((original.notna() & df[col].isna()).sum())
        if invalidas:
            print(f"[Aviso] {invalidas} data(s) inválida(s) em '{col}' viraram vazio.")
 
    for col in COLUNAS_NUM:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
 
    # verificações de qualidade
    if "abono_dias" in df.columns and (df["abono_dias"] > 10).any():
        qtd = int((df["abono_dias"] > 10).sum())
        print(f"[Aviso] {qtd} linha(s) com abono acima de 10 dias (limite legal). Confira.")
    if {"fim_periodo_aquisitivo", "limite_para_gozo"} <= set(df.columns):
        incoerentes = int((df["limite_para_gozo"] < df["fim_periodo_aquisitivo"]).sum())
        if incoerentes:
            print(f"[Aviso] {incoerentes} linha(s) com limite antes do fim do período.")
 
    print(f"[Transform] {len(df)} linhas após a limpeza.")
    return df.reset_index(drop=True)
 
 
def load(df: pd.DataFrame) -> None:
    """L: grava no banco (substitui a tabela se ela já existir) e confere a contagem."""
    engine = create_engine(DB_URL)
    df.to_sql(TABELA, engine, if_exists="replace", index=False)
    with engine.connect() as conn:
        total = conn.execute(text(f"SELECT COUNT(*) FROM {TABELA}")).scalar()
    print(f"[Load] {len(df)} linhas enviadas; {total} linhas na tabela '{TABELA}'.")
 
 
if __name__ == "__main__":
    load(transform(extract()))