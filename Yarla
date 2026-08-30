# manipulação dos dados
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import seaborn as sns
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
df_customers = pd.read_csv(BASE_DIR / 'olist_customers_dataset.csv')
df_orders = pd.read_csv(BASE_DIR / 'olist_orders_dataset.csv')
df_items = pd.read_csv(BASE_DIR / 'olist_order_items_dataset.csv')
df_products = pd.read_csv(BASE_DIR / 'olist_products_dataset.csv')

CORES_GRAFICOS = ['#E67E22', '#2E8B57', '#1F4E78']
CORES_REGIOES = {
    'Sudeste': '#1B5E20',
    'Sul': '#43A047',
    'Centro-Oeste': '#81C784',
    'Nordeste': '#E65100',
    'Norte': '#FF9800',
}

# Mapeamento de Regiões
mapa_regioes = {
    'SP': 'Sudeste',
    'RJ': 'Sudeste',
    'MG': 'Sudeste',
    'ES': 'Sudeste',
    'PR': 'Sul',
    'RS': 'Sul',
    'SC': 'Sul',
    'DF': 'Centro-Oeste',
    'GO': 'Centro-Oeste',
    'MT': 'Centro-Oeste',
    'MS': 'Centro-Oeste',
    'BA': 'Nordeste',
    'PE': 'Nordeste',
    'CE': 'Nordeste',
    'MA': 'Nordeste',
    'PB': 'Nordeste',
    'RN': 'Nordeste',
    'AL': 'Nordeste',
    'SE': 'Nordeste',
    'PI': 'Nordeste',
    'AM': 'Norte',
    'PA': 'Norte',
    'RO': 'Norte',
    'TO': 'Norte',
    'AC': 'Norte',
    'AP': 'Norte',
    'RR': 'Norte',
}
df_customers['regiao'] = df_customers['customer_state'].map(mapa_regioes)

# 2. Merge das bases
df_merged = (
    df_customers.merge(df_orders, on='customer_id')
    .merge(df_items, on='order_id')
    .merge(df_products, on='product_id')
)
df_merged = df_merged.dropna(subset=['product_category_name'])

# Formatação dos nomes das categorias
df_merged['product_category_name'] = (
    df_merged['product_category_name'].str.replace('_', ' ').str.title()
)


# GRÁFICO 1: PARTICIPAÇÃO POR REGIÃO (% em Valor Vendido R$)

df_regiao_valor = (
    df_merged.groupby('regiao')['price'].sum().reset_index()
)
df_regiao_valor.columns = ['Região', 'Valor_Total']
fig_regiao = px.pie(
    df_regiao_valor,
    values='Valor_Total',
    names='Região',
    title='<b>1. Participação por Região (% Valor vendido)</b>',
    hole=0.4,
    color_discrete_sequence=CORES_GRAFICOS,
)
fig_regiao.update_traces(textinfo='percent')
fig_regiao.show()


# GRÁFICO 2: PARTICIPAÇÃO POR CATEGORIA - TOP 10 (% em Valor Vendido R$)

df_cat_valor = (
    df_merged.groupby('product_category_name')['price']
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)
df_cat_valor.columns = ['Categoria', 'Valor_Total']
fig_categoria = px.pie(
    df_cat_valor,
    values='Valor_Total',
    names='Categoria',
    title='<b>2. Participação do Valor Vendido - Top 10 Categorias (%)</b>',
    hole=0.4,
    color_discrete_sequence=CORES_GRAFICOS,
)
fig_categoria.update_traces(textinfo='percent')
fig_categoria.show()


# GRÁFICO 3: CATEGORIA QUE MAIS VENDE POR REGIÃO

df_regiao_categoria = (
    df_merged.groupby(['regiao', 'product_category_name'])['price']
    .sum()
    .reset_index()
)
df_regiao_categoria.columns = ['Região', 'Categoria', 'Valor_Total']

df_top_cat_por_regiao = df_regiao_categoria.loc[
    df_regiao_categoria.groupby('Região')['Valor_Total'].idxmax()
]
df_top_cat_por_regiao = df_top_cat_por_regiao.sort_values(
    'Valor_Total', ascending=True
)

fig_top_categoria_regiao = px.bar(
    df_top_cat_por_regiao,
    x='Valor_Total',
    y='Região',
    color='Categoria',
    orientation='h',
    title='<b>3. Categoria que Mais Vende em Cada Região</b>',
    labels={'Valor_Total': 'Valor Vendido (R$)', 'Região': 'Região'},
    color_discrete_sequence=CORES_GRAFICOS,
)
fig_top_categoria_regiao.update_layout(height=400, showlegend=True)
fig_top_categoria_regiao.show()

# GRÁFICO 4: EVOLUÇÃO ANUAL DOS PEDIDOS POR REGIÃO

# Preparar datas e extrair o ano da compra
df_orders_regiao = df_orders.merge(
    df_customers[['customer_id', 'regiao']], on='customer_id', how='inner'
)
df_orders_regiao['order_purchase_timestamp'] = pd.to_datetime(
    df_orders_regiao['order_purchase_timestamp'], errors='coerce'
)
df_orders_regiao = df_orders_regiao.dropna(
    subset=['order_purchase_timestamp', 'regiao']
)
df_orders_regiao['Ano'] = df_orders_regiao['order_purchase_timestamp'].dt.year
df_orders_regiao['Trimestre'] = (
    df_orders_regiao['order_purchase_timestamp'].dt.to_period('Q').astype(str)
    .str.replace('Q', ' T', regex=False)
)

# Agrupar por Ano e Região para contar pedidos únicos
df_evolucao_regiao = (
    df_orders_regiao.groupby(['Ano', 'regiao'])['order_id']
    .nunique()
    .reset_index()
)
df_evolucao_regiao.columns = ['Ano', 'Região', 'Pedidos']
df_evolucao_regiao['Ano'] = df_evolucao_regiao['Ano'].astype(int)

# Gráfico de linhas comparando a evolução das regiões ao longo dos anos
fig_evolucao_regiao = px.line(
    df_evolucao_regiao,
    x='Ano',
    y='Pedidos',
    color='Região',
    markers=True,
    title='<b>4. Evolução do Número de Pedidos por Região (Anual)</b>',
    labels={'Ano': 'Ano da Compra', 'Pedidos': 'Quantidade de Pedidos'},
    color_discrete_map=CORES_REGIOES,
)

fig_evolucao_regiao.update_xaxes(dtick=1)  # Exibir anos como inteiros na escala
fig_evolucao_regiao.update_layout(hovermode='x unified')
fig_evolucao_regiao.show()


# GRÁFICO 5: EVOLUÇÃO TRIMESTRAL DOS PEDIDOS POR REGIÃO

df_evolucao_trimestre = (
    df_orders_regiao.groupby(['Trimestre', 'regiao'])['order_id']
    .nunique()
    .reset_index()
    .sort_values('Trimestre')
)
df_evolucao_trimestre.columns = ['Trimestre', 'Região', 'Pedidos']
ultimo_trimestre = pd.to_datetime(
    df_orders_regiao['order_purchase_timestamp']
).max().to_period('Q')
ordem_trimestres = [
    f'{trimestre.year} T{trimestre.quarter}'
    for trimestre in pd.period_range('2016Q1', ultimo_trimestre, freq='Q')
]
regioes = df_evolucao_trimestre['Região'].unique()
indice_completo = pd.MultiIndex.from_product(
    [ordem_trimestres, regioes], names=['Trimestre', 'Região']
)
df_evolucao_trimestre = (
    df_evolucao_trimestre.set_index(['Trimestre', 'Região'])
    .reindex(indice_completo, fill_value=0)
    .reset_index()
)

fig_evolucao_trimestre = px.line(
    df_evolucao_trimestre,
    x='Trimestre',
    y='Pedidos',
    color='Região',
    markers=True,
    title='<b>5. Evolução do Número de Pedidos por Região (Trimestral)</b>',
    labels={'Trimestre': 'Trimestre da Compra', 'Pedidos': 'Quantidade de Pedidos'},
    color_discrete_map=CORES_REGIOES,
    category_orders={'Trimestre': ordem_trimestres},
)

fig_evolucao_trimestre.update_layout(hovermode='x unified')
fig_evolucao_trimestre.show()
