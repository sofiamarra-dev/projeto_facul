from datetime import date
import numpy as np
import pandas as pd 
import plotly.express as px
import streamlit as st 
from sqlalchemy import create_engine

from config import DB_URL , TABELA 

st.set_page_config(page_title="Controle de Férias",layout= "wide")

COLUNAS_DATA = [
    "data_de_admissao",
    "inicio_periodo_aquisitivo",
    "fim_periodo_aquisitivo",
    "limite_para_gozo",
    "inicio_das_ferias",
    "fim_das_ferias",
    "proximo_pa_inicio",
    "proximo_pa_fim",
    "proximo_limite_de_gozo",
]
                   
ORDEM = [
    "Vencida",
    "Vence em até 30 dias",
    "Vence em 31–90 dias",
    "No prazo",
    "Em aquisição",
    "Quitada",
]        

CORES = {
    "Vencida": "#d62728",
    "Vence em até 30 dias": "#ff7f0e",
    "Vence em 31–90 dias": "#e8c41c",
    "No prazo": "#2ca02c",
    "Em aquisição": "#4c78a8",
    "Quitada": "#9aa0a6",
}

@st.cache_data
def carregar() -> pd.DataFrame:
    engine = create_engine(DB_URL)
    df = pd.read_sql(f"SELECT * FROM {TABELA}",engine)
    #no SQLite as datas votam como texto:converte de novo
    for col in COLUNAS_DATA:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col],errors="coerce")
    return df        
        
        
def classificar(df: pd.DataFrame, ref: pd.Timestamp) -> pd.DataFrame:
    """Define a situação de cada período aquisitivo em relação à data de referência."""
    df = df.copy()
    gozado = df["dias_gozados"].fillna(0) + df["abono_dias"].fillna(0)
    condicoes = [
        gozado >= 30,
        df["fim_periodo_aquisitivo"] > ref,
        df["limite_para_gozo"] < ref,
        df["limite_para_gozo"] <= ref + pd.Timedelta(days=30),
        df["limite_para_gozo"] <= ref + pd.Timedelta(days=90),
    ]
    opcoes = [
        "Quitada",
        "Em aquisição",
        "Vencida",
        "Vence em até 30 dias",
        "Vence em 31–90 dias",
    ]
    df["situacao"] = np.select(condicoes, opcoes, default="No prazo")

    limite = pd.to_datetime(df["limite_para_gozo"], errors="coerce")
    df["dias_para_vencer"] = (
        limite.to_numpy().astype("datetime64[D]") - np.datetime64(ref.date(), "D")
    ).astype("int64")
    return df
    

df = carregar()
 
st.title("Controle de Férias")
st.caption(
    "Cada linha é um período aquisitivo. A situação é calculada pela data de "
    "referência e pelo prazo limite para gozo."
)
 
# --- filtros ---
st.sidebar.header("Filtros")
ref = pd.Timestamp(st.sidebar.date_input("Data de referência", value=date.today()))
df = classificar(df, ref)

gestores = sorted(df["gestor"].dropna().unique())
sel_gestores = st.sidebar.multiselect("Gestor", gestores)
sel_situacoes = st.sidebar.multiselect("Situação", ORDEM)
busca = st.sidebar.text_input("Buscar empregado")

# filtro vazio = não filtrar (mostra tudo)
if sel_gestores:
    df = df[df["gestor"].isin(sel_gestores)]
if sel_situacoes:
    df = df[df["situacao"].isin(sel_situacoes)]
if busca.strip():
    df = df[
        df["empregado"].str.contains(busca.strip(), case=False, regex=False, na=False)
    ]
    
# --- indicadores ---
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Empregados", df["codigo"].nunique())
c2.metric("Períodos", len(df))
c3.metric("Vencidas", int((df["situacao"] == "Vencida").sum()))
c4.metric("Vencem em até 30 dias", int((df["situacao"] == "Vence em até 30 dias").sum()))
c5.metric("Vencem em 31–90 dias", int((df["situacao"] == "Vence em 31–90 dias").sum()))
 
# --- gráficos ---
g1, g2 = st.columns(2)
 
por_situacao = (
    df.groupby("situacao").size().reindex(ORDEM, fill_value=0).reset_index(name="periodos")
)
por_situacao = por_situacao[por_situacao["periodos"] > 0]
g1.plotly_chart(
    px.bar(
        por_situacao,
        x="situacao",
        y="periodos",
        color="situacao",
        color_discrete_map=CORES,
        title="Períodos por situação",
        labels={"situacao": "", "periodos": "Períodos"},
    ).update_layout(showlegend=False)
)
 
por_gestor = df.groupby(["gestor", "situacao"]).size().reset_index(name="periodos")
g2.plotly_chart(
    px.bar(
        por_gestor,
        x="gestor",
        y="periodos",
        color="situacao",
        color_discrete_map=CORES,
        category_orders={"situacao": ORDEM},
        title="Situação por gestor",
        labels={"gestor": "Gestor", "periodos": "Períodos"},
    )
)
 
pendentes = df[df["situacao"] != "Quitada"].copy()
pendentes["mes_limite"] = pendentes["limite_para_gozo"].dt.to_period("M").dt.to_timestamp()
por_mes = pendentes.groupby(["mes_limite", "gestor"]).size().reset_index(name="periodos")
st.plotly_chart(
    px.bar(
        por_mes,
        x="mes_limite",
        y="periodos",
        color="gestor",
        title="Prazos limite para gozo por mês",
        labels={"mes_limite": "Mês do prazo limite", "periodos": "Períodos"},
    )
)
 
# --- atenção imediata ---
st.subheader("Atenção imediata")
urgentes = df[df["situacao"].isin(["Vencida", "Vence em até 30 dias", "Vence em 31–90 dias"])]
urgentes = urgentes.sort_values("dias_para_vencer")[
    ["gestor", "codigo", "empregado", "limite_para_gozo", "dias_para_vencer", "situacao"]
].copy()
urgentes["limite_para_gozo"] = urgentes["limite_para_gozo"].dt.strftime("%d/%m/%Y")
urgentes.columns = ["Gestor", "Código", "Empregado", "Limite para gozo", "Dias p/ vencer", "Situação"]
if urgentes.empty:
    st.success("Nenhum período vencido ou perto de vencer.")
else:
    st.caption("Dias negativos = prazo já vencido.")
    st.dataframe(urgentes, hide_index=True)
 
# --- dados completos ---
with st.expander("Ver todos os dados"):
    st.dataframe(df, hide_index=True)
    st.download_button(
        "Baixar CSV filtrado",
        df.to_csv(index=False).encode("utf-8"),
        file_name="ferias_filtrado.csv",
        mime="text/csv",
    )
    
    