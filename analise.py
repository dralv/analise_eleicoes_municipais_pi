#%%
import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd

# %%
#carregando dados das eleições piaui
resultados_2024 = pd.read_csv('dados/resultados/resultados_2024.csv',sep=';',encoding='ISO-8859-1')
resultados_2020 = pd.read_csv('dados/resultados/resultados_2020.csv',sep=';',encoding='ISO-8859-1')
resultados_2016= pd.read_csv('dados/resultados/resultados_2016.csv',sep=';',encoding='ISO-8859-1')
#carregando dados do mapa piaui
municipios_pi = gpd.read_file('dados/PI_Municipios_2022/PI_Municipios_2022.shp')
#carregando informações sobre partidos
partidos = pd.read_csv('dados/partidos2024.csv',sep=';')

# %%
resultados_2024.head(10)
# %%
resultados_2020.head(10)
# %%
resultados_2016.head(10)

# %%
partidos.head(10)

# %%
municipios_pi.head(10)

# %%
#filtrando apenas os cargos de prefeito em primeiro turno
resultados_2024 = resultados_2024[(resultados_2024['DS_CARGO']=='Prefeito') & (resultados_2024['NR_TURNO']==1)]
resultados_2020 = resultados_2020[(resultados_2020['DS_CARGO']=='Prefeito') & (resultados_2020['NR_TURNO']==1)]
resultados_2016 = resultados_2016[(resultados_2016['DS_CARGO']=='Prefeito') & (resultados_2016['NR_TURNO']==1)]

# %%
#selecionando apenas colunas essenciais
resultados_2024 = resultados_2024[['CD_MUNICIPIO', 'NM_MUNICIPIO', 'NM_CANDIDATO','NR_PARTIDO','SG_PARTIDO', 'QT_VOTOS_NOMINAIS_VALIDOS', 'DS_SIT_TOT_TURNO']]
resultados_2020 = resultados_2020[['CD_MUNICIPIO', 'NM_MUNICIPIO', 'NM_CANDIDATO','NR_PARTIDO','SG_PARTIDO', 'QT_VOTOS_NOMINAIS_VALIDOS', 'DS_SIT_TOT_TURNO']]
resultados_2016 = resultados_2016[['CD_MUNICIPIO', 'NM_MUNICIPIO', 'NM_CANDIDATO','NR_PARTIDO','SG_PARTIDO', 'QT_VOTOS_NOMINAIS', 'DS_SIT_TOT_TURNO']]
# %%
# group by da soma de votos por partido
votos_por_partidos_2016 = resultados_2016.groupby('SG_PARTIDO')['QT_VOTOS_NOMINAIS'].sum().reset_index().sort_values(by='QT_VOTOS_NOMINAIS', ascending=False)
votos_por_partidos_2020 = resultados_2020.groupby('SG_PARTIDO')['QT_VOTOS_NOMINAIS_VALIDOS'].sum().reset_index().sort_values(by='QT_VOTOS_NOMINAIS_VALIDOS', ascending=False)
votos_por_partidos_2024 = resultados_2024.groupby('SG_PARTIDO')['QT_VOTOS_NOMINAIS_VALIDOS'].sum().reset_index().sort_values(by='QT_VOTOS_NOMINAIS_VALIDOS', ascending=False)

# %%

# Função para configurar cada subplot
def configurar_subplot(ax, titulo, dados, cor, largura_barra):
    barra = ax.bar(dados['SG_PARTIDO'], dados['QT_VOTOS'], width=largura_barra, color=cor)
    ax.set_title(titulo, color='black', size=32, pad=20)
    ax.set_xticks(range(len(dados)))  # Define os ticks no eixo x
    ax.set_xticklabels(dados['SG_PARTIDO'], rotation=45, ha='right', fontsize=25)
    ax.set_yticklabels([])  # Remove rótulos do eixo Y
    ax.set_ylim(0, ax.get_ylim()[1] * 1.1)  # Adiciona espaço ao eixo Y
    adicionar_rotulos_barras(barra, ax)  # Adiciona rótulos acima das barras

# Função para adicionar rótulos nas barras
def adicionar_rotulos_barras(barras, ax):
    for barra in barras:
        yval = barra.get_height()
        ax.text(barra.get_x() + barra.get_width() / 2, yval, int(yval), 
                va='bottom', ha='center', fontsize=25, rotation=45)

# Dados de exemplo
dados_2016 = votos_por_partidos_2016.rename(columns={'QT_VOTOS_NOMINAIS': 'QT_VOTOS'})
dados_2020 = votos_por_partidos_2020.rename(columns={'QT_VOTOS_NOMINAIS_VALIDOS': 'QT_VOTOS'})
dados_2024 = votos_por_partidos_2024.rename(columns={'QT_VOTOS_NOMINAIS_VALIDOS': 'QT_VOTOS'})

# Configuração dos subplots
fig, ax = plt.subplots(3, 1, figsize=(50, 35))
largura_barra = 0.3  # Largura das barras

# Configura cada subplot com a função reutilizável
configurar_subplot(ax[0], 'Votos por partido 2016', dados_2016, 'blue', largura_barra)
configurar_subplot(ax[1], 'Votos por partido 2020', dados_2020, 'green', largura_barra)
configurar_subplot(ax[2], 'Votos por partido 2024', dados_2024, 'orange', largura_barra)

# Ajuste das margens e espaçamento entre gráficos
plt.subplots_adjust(left=0.1, right=0.9, top=0.85, bottom=0.1, hspace=0.7)

# Exibir o gráfico
plt.show()

# %%
#identificando o espectro dos partidos
#transformando o espectro em variãvel categórica 
espec_type = pd.CategoricalDtype(categories=['Direita', 'Centro', 'Esquerda'], ordered=True)
partidos['Espectro'] = partidos['Espectro'].str.title()
partidos['Espectro'] = partidos['Espectro'].astype(espec_type)
partidos.info()

# %%
#merge para identificar o espectro do partido
resultados_2016 = resultados_2016.merge(partidos[['NR_PARTIDO','Espectro']], left_on='NR_PARTIDO', right_on='NR_PARTIDO')
resultados_2020 = resultados_2020.merge(partidos[['NR_PARTIDO','Espectro']], left_on='NR_PARTIDO', right_on='NR_PARTIDO')
resultados_2024 = resultados_2024.merge(partidos[['NR_PARTIDO','Espectro']], left_on='NR_PARTIDO', right_on='NR_PARTIDO')

# %%
#group by por Espectro e Munícipio
votos_espectro_2016 = resultados_2016.groupby(
    ['CD_MUNICIPIO', 'Espectro'], observed=False
).agg({'NM_MUNICIPIO': 'first', 'QT_VOTOS_NOMINAIS': 'sum'}).reset_index()

votos_espectro_2020 = resultados_2020.groupby(
    ['CD_MUNICIPIO', 'Espectro'], observed=False
).agg({'NM_MUNICIPIO': 'first', 'QT_VOTOS_NOMINAIS_VALIDOS': 'sum'}).reset_index()

votos_espectro_2024 = resultados_2024.groupby(
    ['CD_MUNICIPIO', 'Espectro'], observed=False
).agg({'NM_MUNICIPIO': 'first', 'QT_VOTOS_NOMINAIS_VALIDOS': 'sum'}).reset_index()

# %%
# Selecionar o espectro mais votado para cada município
espectro_mais_votado_2016 = votos_espectro_2016.loc[
    votos_espectro_2016.groupby('CD_MUNICIPIO')['QT_VOTOS_NOMINAIS'].idxmax()
].reset_index(drop=True)

espectro_mais_votado_2020 = votos_espectro_2020.loc[
    votos_espectro_2020.groupby('CD_MUNICIPIO')['QT_VOTOS_NOMINAIS_VALIDOS'].idxmax()
].reset_index(drop=True)

espectro_mais_votado_2024 = votos_espectro_2024.loc[
    votos_espectro_2024.groupby('CD_MUNICIPIO')['QT_VOTOS_NOMINAIS_VALIDOS'].idxmax()
].reset_index(drop=True)
# %%
#merge dados municipios com eleicoes
municipios_pi['NM_MUN'] = municipios_pi['NM_MUN'].str.upper()
municipios_pi_espectro_mais_votado_2016 = municipios_pi.merge(espectro_mais_votado_2016,how='left',left_on='NM_MUN',right_on='NM_MUNICIPIO')

municipios_pi_espectro_mais_votado_2020 = municipios_pi.merge(espectro_mais_votado_2020,how='left',left_on='NM_MUN',right_on='NM_MUNICIPIO')

municipios_pi_espectro_mais_votado_2024 = municipios_pi.merge(espectro_mais_votado_2024,how='left',left_on='NM_MUN',right_on='NM_MUNICIPIO')

# %%
fig, ax = plt.subplots(1, 3, figsize=(28, 10))

# Dados para cada ano
anos = [2016, 2020, 2024]
datasets = [
    municipios_pi_espectro_mais_votado_2016,
    municipios_pi_espectro_mais_votado_2020,
    municipios_pi_espectro_mais_votado_2024
]

# Função para configurar o gráfico
def configurar_grafico(ax, ano, dataset):
    ax.set_title(f'Espectro Mais Votado {ano}', color='black', size=16)
    ax.axis('off')

    # Plotar o mapa
    dataset.plot(
        column='Espectro',
        linewidth=0.2,
        edgecolor='black',
        legend=True,
        cmap='Accent',
        ax=ax,
        missing_kwds={'color': 'lightgrey', 'label': 'Espectro Desconhecido'},
        legend_kwds={
            'loc': 'upper left',
            'bbox_to_anchor': (0, 1),
            'title': 'Espectro',
            'fontsize': 12
        }
    )

    # Adicionar contagens de espectros no gráfico
    espectro_counts = dataset['Espectro'].value_counts(dropna=False)
    for idx, (espectro, count) in enumerate(espectro_counts.items()):
        espectro_label = 'Desconhecido' if pd.isna(espectro) else espectro
        ax.text(
            0.1, 0.7 - idx * 0.05, f'{espectro_label}: {count} cidades',
            transform=ax.transAxes, fontsize=12, color='black'
        )

# Loop para configurar cada gráfico
for i, (ano, dataset) in enumerate(zip(anos, datasets)):
    configurar_grafico(ax[i], ano, dataset)

plt.show()