# ADCC Historical Dataset — Limpeza e Preparação de Dados

## Contexto
Base histórica de lutas do ADCC (Abu Dhabi Combat Club), um dos principais
campeonatos de jiu-jitsu/grappling submission do mundo, cobrindo edições de
1998 a 2022.

**Fonte original:** [ADCC Historical Dataset — Kaggle](https://www.kaggle.com/datasets/bjagrelli/adcc-historical-dataset)

## Problema
O arquivo bruto (`data/raw/adcc_historical_data_raw.csv`) tinha várias
características que impediam o uso direto em análise:

1. **Separador incorreto** — o CSV usa `;` como delimitador, então uma leitura
   padrão (`,`) juntava todas as colunas em uma só.
2. **Valores sentinela** — `winner_points` e `loser_points` usam `-1` para
   representar "não aplicável" (lutas decididas por finalização, decisão ou
   desqualificação não têm placar), misturado com pontuações reais.
3. **Coluna binária mal tipada** — `adv_pen` só assume `PEN` ou vazio,
   funcionando na prática como um booleano.
4. **Inconsistência pontual** — 2 lutas do tipo `SUBMISSION` sem o nome da
   finalização preenchido.
5. **Tipos de dado não validados** — IDs e ano lidos sem garantia de tipo
   inteiro.

## Solução
Script `scripts/clean_data.py` (Python/pandas) que:
- lê o CSV com o separador correto (`;`);
- converte os valores `-1` de pontuação em `NaN` (ausência real de dado);
- transforma `adv_pen` na coluna booleana `decided_by_penalty`;
- rotula as 2 finalizações sem tipo como `"Not specified"`;
- limpa espaços em texto e converte colunas categóricas (`win_type`,
  `weight_class`, `sex`, `stage`) para `category`;
- ordena por ano/match_id e exporta os resultados tratados em CSV e Excel.

**Limitação documentada (não corrigida artificialmente):** 152 lutas
decididas por pontos não têm placar registrado na fonte original,
concentradas em torneios de 1998 a 2013 — nesse período o ADCC não divulgava
o placar detalhado.

## Estrutura do repositório
```
adcc-project/
├── data/
│   ├── raw/                 # dado original, sem alterações
│   └── processed/           # dado limpo (CSV e XLSX)
├── scripts/
│   └── clean_data.py        # script de limpeza
└── README.md
```

## Como rodar
```bash
pip install pandas openpyxl
python scripts/clean_data.py
```

## Resultado
1.028 lutas tratadas, 14 colunas, prontas para análise (ex.: taxa de vitória
por tipo de finalização, evolução de peso-categorias ao longo dos anos,
comparação de desempenho por atleta).
