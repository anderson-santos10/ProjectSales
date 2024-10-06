import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(layout="wide")

# Carregando os dados
df = pd.read_csv('supermarket_sales.csv', sep=";", decimal=",")

# Convertendo a coluna "Date" para datetime
df["Date"] = pd.to_datetime(df["Date"])

# Ordenando os dados pela data
df = df.sort_values("Date")

# Criando a coluna "Month" (Ano-Mês) para filtrar os meses
df["Month"] = df["Date"].apply(lambda x: str(x.year) + "-" + str(x.month))

# Criando a seleção de mês na barra lateral
month = st.sidebar.selectbox("Mês", df["Month"].unique())

# Filtrando o dataframe de acordo com o mês selecionado
df_filtered = df[df["Month"] == month]
df_filtered

# Dividindo a tela em colunas para exibir gráficos
col1, col2 = st.columns(2)
col3, col4, col5 = st.columns(3)

# Gráfico de barras para o faturamento por dia, com cores para as cidades
fig_date = px.bar(df_filtered, x="Date", y="Total",
                  color="City", title="Faturamento por dia")
col1.plotly_chart(fig_date, use_container_width=True)

# Agrupando e somando o total de vendas por linha de produto
product_total = df_filtered.groupby(
    "Product line")[["Total"]].sum().reset_index()

# Gráfico de barras horizontal para faturamento por linha de produto
fig_prod = px.bar(product_total, x="Total", y="Product line", color="Product line",
                  title="Faturamento por tipo de produto", orientation="h")
col2.plotly_chart(fig_prod, use_container_width=True)

# Agrupando e somando o total de vendas por cidade
city_total = df_filtered.groupby("City")[["Total"]].sum().reset_index()

# Gráfico de barras para o faturamento por filial
fig_city = px.bar(city_total, x="City", y="Total",
                  title="Faturamento por filial")
col3.plotly_chart(fig_city, use_container_width=True)

# Gráfico de pizza para faturamento por tipo de pagamento
fig_kind = px.pie(df_filtered, values="Total", names="Payment",
                  title="Faturamento por tipo de pagamento")
col4.plotly_chart(fig_kind, use_container_width=True)

# Agrupando e calculando a média de avaliação (Rating) por cidade
city_rating = df_filtered.groupby("City")[["Rating"]].mean().reset_index()

# Gráfico de barras para a média de avaliação por cidade
fig_rating = px.bar(city_rating, y="Rating", x="City",
                    title="Média de Avaliação por Cidade")
col5.plotly_chart(fig_rating, use_container_width=True)
