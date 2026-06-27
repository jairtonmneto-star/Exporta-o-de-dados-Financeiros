import yfinance as yf
import pandas as pd
import streamlit as st
import plotly.express as px
#Definicao de titulo e subtitulo e sidebar
st.set_page_config(page_title = "Analise de Ações de Criptomoedas", page_icon = "💰", layout = "wide")
st.title("Dashboard de Análise de Ações de Criptomoedas")
st.sidebar.header("Filtros")
#Definição do que sera filtrado
cryptos = st.sidebar.multiselect("Selecione as criptomoedas", ["BTC-USD", "ETH-USD", "LTC-USD", "XRP-USD"])
periodo = st.sidebar.selectbox("Selecione o período", ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y"])
if not cryptos:
    st.warning("Selecione ao menos uma criptomoeda.")
    st.stop()

todos_historicos = []
for crypto in cryptos:
    dados = yf.Ticker(crypto)
    hist = dados.history(period=periodo)
    hist["Crypto"] = crypto
    todos_historicos.append(hist)

dados_hist = pd.concat(todos_historicos)
info = yf.Ticker(cryptos[0]).info
#KPI no topo
col1, col2, col3, col4 = st.columns(4)
col1.metric("Preço Atual", f"${info.get('regularMarketPrice', 0):.2f}")
col2.metric("Maximo em 52 semanas", f"${info.get('fiftyTwoWeekHigh', 0):.2f}")
col3.metric("Mínimo em 52 semanas", f"${info.get('fiftyTwoWeekLow', 0):.2f}")
col4.metric("Variação (1d)", f"{info.get('regularMarketChangePercent', 0):.2f}%")
st.divider()
#Grafico de Preco
fig = px.line(dados_hist, x=dados_hist.index, y="Close", title=f"Preço de Fechamento das Criptomoedas: {', '.join(cryptos)}")
st.plotly_chart(fig, use_container_width=True)
#Tabela com Dados
st.subheader("Tabela de Dados")
st.dataframe(dados_hist[["Open", "High", "Low", "Close", "Volume","Crypto"]].tail(30))
