# Documentação do Projeto de Análise Eleitoral do Piauí

## Sumário
- [Descrição](#descrição)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Instalação e Dependências](#instalação-e-dependências)
- [Descrição dos Dados](#descrição-dos-dados)
- [Fluxo do Projeto](#fluxo-do-projeto)
- [Visualizações](#visualizações)
- [Execução](#execução)
- [Conclusões](#conclusões)
- [Licença](#licença)

---

## Descrição
Este projeto realiza uma análise exploratória dos resultados das eleições municipais no estado do Piauí para os anos de **2016**, **2020** e **2024**. O objetivo principal é analisar a distribuição dos votos por partido e espectro ideológico (Esquerda, Centro, Direita) nos municípios do estado, além de visualizar esses resultados em mapas geográficos.

---

## Estrutura do Projeto
```
📂 dados/
 ┣ 📂 resultados/
 ┃ ┣ 📄 resultados_2016.csv
 ┃ ┣ 📄 resultados_2020.csv
 ┃ ┗ 📄 resultados_2024.csv
 ┣ 📄 partidos2024.csv
 ┗ 📂 PI_Municipios_2022/
   ┗ 📄 PI_Municipios_2022.cpg
   ┣ 📄 PI_Municipios_2022.dbf
   ┣ 📄 PI_Municipios_2022.prj
   ┣ 📄 PI_Municipios_2022.shp
   ┗ 📄 PI_Municipios_2022.shx

📄 main.py (Script principal)
📄 README.md (Documentação)
📄 requirements.txt (Pacotes)
```
---

## Instalação e Dependências
1. **Python 3.x** instalado.
2. Instale as dependências necessárias com:
   ```bash
   pip install -rrequirements.txt
   ```


---

## Descrição dos Dados
- **resultados_2016.csv, resultados_2020.csv, resultados_2024.csv**: Resultados das eleições municipais para prefeito (1º turno) por município.
  - **Fonte**: [Site TSE](https://dadosabertos.tse.jus.br/organization/tse-agel)
  - **Colunas principais**: 
    - `NM_CANDIDATO`: Nome do candidato.
    - `SG_PARTIDO`: Sigla do partido.
    - `QT_VOTOS`: Quantidade de votos válidos.
    - `DS_CARGO`: Cargo disputado (Prefeito).
  
- **partidos2024.csv**: Informações sobre o espectro ideológico dos partidos.
    - **Fonte**: [GitHub](https://github.com/programacaodinamica/analise-dados/blob/master/dados/partidos2024.csv)

- **PI_Municipios_2022.shp**: Shapefile contendo o mapa dos municípios do Piauí.
    - **Fonte**: [IBGE](https://www.ibge.gov.br/geociencias/organizacao-do-territorio/malhas-territoriais/15774-malhas.html)
---

## Fluxo do Projeto
### 1. **Carregamento dos Dados**
Os dados de eleições, partidos e o mapa são carregados para `DataFrames` utilizando `pandas` e `geopandas`.

### 2. **Filtragem e Limpeza dos Dados**
- Filtra apenas os resultados de eleições para prefeito no 1º turno.
- Mantém apenas colunas relevantes, como nome do candidato, partido e número de votos.

### 3. **Análise de Votos por Partido**
- Realiza um `groupby` por partido para somar os votos em cada eleição.
- Renomeia colunas para padronizar a estrutura.

### 4. **Visualização de Gráficos**
- Cria gráficos de barras comparando os votos por partido em 2016, 2020 e 2024.
- Utiliza **matplotlib** para a visualização dos dados.

### 5. **Identificação do Espectro Ideológico**
- Adiciona a coluna `Espectro` a partir da tabela de partidos.
- Realiza um `merge` dos dados de eleições com o espectro ideológico dos partidos.

### 6. **Visualização Geográfica dos Resultados**
- Utiliza **geopandas** para plotar mapas do Piauí.
- Mostra o espectro ideológico mais votado em cada município para os anos analisados.

---

## Visualizações
1. **Gráficos de barras**:
   - Votos por partido em 2016, 2020 e 2024.
   - Adição de rótulos com a contagem de votos nas barras.

2. **Mapas geográficos**:
   - Espectro mais votado em cada município.
   - Cores diferentes para Esquerda, Centro e Direita.
   - Municípios com espectro desconhecido são destacados em cinza.

---

## Execução
1. **Baixe o repositório**:
   ```bash
   git clone https://github.com/seu-usuario/projeto-eleicoes-piaui.git
   cd projeto-eleicoes-piaui
   ```

2. **Execute o script principal**:
   ```bash
   python main.py
   ```

3. **Visualização dos gráficos e mapas**:
   O script irá gerar gráficos e mapas exibindo a distribuição de votos por partido e por espectro ideológico.

---

## Conclusões
Este projeto fornece insights sobre o comportamento eleitoral no estado do Piauí e permite visualizar como o espectro ideológico evoluiu ao longo das eleições. A análise também pode ser usada como base para estudos de marketing político e comportamento do eleitorado.


