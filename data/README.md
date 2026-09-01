# Tech Challenge - Crescimento e Receita no E-commerce Olist

Projeto desenvolvido para o **Tech Challenge da Fase 1 da Pós-graduação em Análise de Dados da FIAP**.

O estudo utiliza o conjunto de dados público de e-commerce da Olist para analisar a evolução comercial do marketplace, identificar os principais motores de crescimento e produzir recomendações voltadas a investidores e tomadores de decisão.

## Integrantes

- Cibele Dinorah
- Julio César Gonçalves Conceição
- Isabela Pucci
- Priscila Tatianne Paulino
- Yarla Freires

## Problema de negócio

O marketplace apresentou crescimento ao longo do período analisado, mas o aumento de receita pode ter sido provocado por diferentes fatores: maior volume de pedidos, elevação do ticket médio, expansão regional ou desempenho de determinadas categorias e vendedores.

Este projeto procura responder à seguinte pergunta:

> Como evoluíram os pedidos e a receita da Olist entre 2017 e 2018, e quais categorias, regiões e vendedores mais contribuíram para esse desempenho?

## Objetivos

- analisar a evolução mensal dos pedidos, da receita e do ticket médio;
- identificar tendências, sazonalidades e mudanças no ritmo de crescimento;
- avaliar a participação de categorias, regiões e vendedores;
- verificar se o crescimento depende de poucos segmentos;
- transformar os resultados em recomendações executivas;
- manter uma análise documentada e reproduzível.

## Dataset

O projeto utiliza o **Brazilian E-Commerce Public Dataset by Olist**, formado por aproximadamente 100 mil pedidos realizados entre 2016 e 2018.

Principais arquivos utilizados:

| Arquivo | Utilização |
|---|---|
| `olist_orders_dataset.csv` | Status e data de compra dos pedidos |
| `olist_order_items_dataset.csv` | Produtos, vendedores, preços e fretes |
| `olist_products_dataset.csv` | Características e categorias dos produtos |
| `olist_customers_dataset.csv` | Identificação e localização dos clientes |
| `olist_sellers_dataset.csv` | Identificação e localização dos vendedores |
| `olist_order_payments_dataset.csv` | Formas, parcelas e valores de pagamento |
| `product_category_name_translation.csv` | Tradução dos nomes das categorias |

Os arquivos originais não precisam ser versionados no repositório. Consulte a seção [Como executar](#como-executar) para preparar o ambiente local.

## Definições dos indicadores

Para garantir consistência, foram adotadas as seguintes regras:

- **Pedidos:** contagem distinta de `order_id` com status `delivered`;
- **Receita de produtos:** soma da coluna `price` da tabela de itens;
- **Ticket médio:** receita de produtos dividida pelo total de pedidos entregues;
- **Mês da venda:** mês de `order_purchase_timestamp`;
- **Valor movimentado:** soma de `payment_value`, apresentado separadamente da receita de produtos;
- **Frete:** soma de `freight_value`, não incluída na definição principal de receita.

Antes das junções, os itens e pagamentos devem ser agregados no nível de `order_id`. Essa etapa evita a multiplicação indevida de valores em pedidos com vários itens ou registros de pagamento.

## Resultados iniciais

A análise exploratória identificou:

- **99.441** pedidos registrados;
- **96.478** pedidos entregues;
- **R$ 13,22 milhões** em receita de produtos entregues;
- **R$ 137,04** de ticket médio geral.

Para evitar distorções causadas por meses incompletos de 2016, a principal comparação utiliza janeiro a agosto de 2017 e o mesmo período de 2018.

| Indicador | Jan-ago/2017 | Jan-ago/2018 | Variação |
|---|---:|---:|---:|
| Pedidos | 21.998 | 52.783 | +139,9% |
| Receita | R$ 2,99 milhões | R$ 7,22 milhões | +141,1% |
| Ticket médio | R$ 136,08 | R$ 136,75 | +0,5% |

### Interpretação inicial

O crescimento da receita foi sustentado principalmente pelo aumento do volume de pedidos. Embora pedidos e receita tenham crescido aproximadamente 140%, o ticket médio avançou apenas 0,5% no período comparável.

Novembro de 2017 apresentou o maior volume mensal, com 7.289 pedidos e receita de R$ 987,8 mil. O resultado sugere um efeito sazonal associado ao período da Black Friday, hipótese que será validada durante o desenvolvimento do projeto.

Maio de 2018 apresentou uma combinação comercial relevante: receita de R$ 977,5 mil, 6.749 pedidos e ticket médio de R$ 144,84. Esse resultado será investigado por categoria, região e vendedor.

## Hipótese de trabalho

> O crescimento da Olist foi impulsionado principalmente pelo aumento do volume de pedidos, mas pode estar concentrado em determinadas categorias, regiões e vendedores.

Essa hipótese será avaliada e poderá ser confirmada, reformulada ou rejeitada de acordo com as evidências encontradas.

## Metodologia

O desenvolvimento segue as etapas do CRISP-DM:

1. **Entendimento do negócio:** definição das perguntas e dos critérios de sucesso;
2. **Entendimento dos dados:** análise das tabelas, chaves, períodos e qualidade;
3. **Preparação:** tratamento, agregação e integração dos dados;
4. **Análise e modelagem:** cálculo dos indicadores e investigação dos segmentos;
5. **Avaliação:** validação dos resultados e das hipóteses;
6. **Comunicação:** apresentação executiva, recomendações e vídeo final.

## Estrutura planejada do repositório

```text
olist-tech-challenge/
├── README.md
├── requirements.txt
├── .gitignore
├── data/
│   ├── raw/                  # CSVs originais, não versionados
│   └── processed/            # Bases tratadas, não versionadas
├── notebooks/
│   ├── 01_entendimento_dos_dados.ipynb
│   ├── 02_preparacao_dos_dados.ipynb
│   └── 03_crescimento_e_receita.ipynb
├── src/
│   ├── data_processing.py
│   ├── metrics.py
│   └── visualizations.py
├── outputs/
│   ├── figures/
│   └── tables/
└── presentation/
```

Essa estrutura representa a organização planejada e deve ser ajustada aos arquivos efetivamente desenvolvidos pelo grupo.

## Tecnologias

- Python 3;
- Pandas e NumPy;
- Matplotlib, Seaborn ou Plotly;
- Jupyter Notebook;
- Git e GitHub;
- ferramenta de apresentação definida pelo grupo.

## Como executar

### 1. Clone o repositório

```bash
git clone URL_DO_REPOSITORIO
cd olist-tech-challenge
```

### 2. Crie e ative um ambiente virtual

```bash
python -m venv .venv
```

No Windows:

```bash
.venv\Scripts\activate
```

No Linux ou macOS:

```bash
source .venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Adicione os dados

Baixe o dataset público da Olist e coloque os arquivos CSV em:

```text
data/raw/
```

### 5. Execute os notebooks

Execute-os na ordem indicada:

1. `01_entendimento_dos_dados.ipynb`;
2. `02_preparacao_dos_dados.ipynb`;
3. `03_crescimento_e_receita.ipynb`.

> Os comandos e nomes dos arquivos deverão ser atualizados caso a implementação final utilize outra estrutura.

## Cuidados de qualidade

- pedidos podem conter vários itens e pagamentos;
- `customer_id` e `customer_unique_id` possuem significados diferentes;
- receita de produtos e valor pago não são indicadores equivalentes;
- os registros de 2016 e o final de agosto de 2018 possuem cobertura incompleta;
- correlação não deve ser apresentada como causalidade;
- hipóteses de sazonalidade precisam ser explicitamente identificadas;
- todas as regras de inclusão, exclusão e tratamento devem ser documentadas.

## Próximas etapas

- [x] Definir o tema Crescimento e Receita;
- [x] Calcular a evolução mensal dos indicadores principais;
- [ ] Analisar categorias e produtos;
- [ ] Avaliar regiões e perfil geográfico do crescimento;
- [ ] Identificar vendedores de maior desempenho;
- [ ] Medir concentração e diversificação da receita;
- [ ] Consolidar recomendações executivas;
- [ ] Preparar a apresentação e o vídeo final.

## Entregáveis do Tech Challenge

- repositório GitHub com os códigos utilizados;
- apresentação executiva com storytelling;
- vídeo executivo de até cinco minutos;
- conclusões e recomendações em linguagem orientada ao negócio.

## Licença e uso dos dados

Este repositório possui finalidade acadêmica. O uso e a redistribuição do dataset devem respeitar os termos definidos por sua fonte original. Os dados da Olist são anonimizados.

