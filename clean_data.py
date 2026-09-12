"""
Limpeza da base ADCC Historical Dataset (Kaggle)
Fonte: https://www.kaggle.com/datasets/bjagrelli/adcc-historical-dataset

Problema encontrado na base bruta:
- Separador incorreto: arquivo vem delimitado por ';', não por ',' (pandas lia
  tudo como uma única coluna de texto).
- Valores sentinela -1 em winner_points/loser_points representando "não
  aplicável" (lutas decididas por finalização, decisão ou desqualificação não
  têm pontuação), misturados com pontuações reais >= 0.
- Coluna adv_pen com apenas 'PEN' ou vazio, mais natural como booleano.
- Duas lutas do tipo SUBMISSION sem o nome da finalização preenchido.
- Tipos de dado (IDs, ano) não conferidos.

Solução: recarregar com o separador correto, converter sentinelas em NaN,
padronizar colunas booleanas/categóricas, validar tipos e documentar limitação
remanescente (152 lutas por pontos sem placar registrado, concentradas em
torneios de 1998-2013, quando o placar detalhado não era divulgado).
"""

import pandas as pd

RAW_PATH = "data/raw/adcc_historical_data_raw.csv"
OUT_CSV = "data/processed/adcc_historical_data_clean.csv"
OUT_XLSX = "data/processed/adcc_historical_data_clean.xlsx"


def clean():
    df = pd.read_csv(RAW_PATH, sep=";")

    # tipos numéricos
    for col in ["match_id", "winner_id", "loser_id", "year"]:
        df[col] = df[col].astype(int)

    # sentinela -1 -> NaN (pontuação não aplicável ao tipo de vitória)
    df["winner_points"] = df["winner_points"].replace(-1, pd.NA)
    df["loser_points"] = df["loser_points"].replace(-1, pd.NA)

    # adv_pen: 'PEN' / NaN -> booleano
    df["decided_by_penalty"] = df["adv_pen"].eq("PEN")
    df = df.drop(columns=["adv_pen"])

    # submission: mantém NaN quando não é finalização; marca os 2 casos
    # de SUBMISSION sem tipo informado
    mask_unlabeled = (df["win_type"] == "SUBMISSION") & (df["submission"].isna())
    df.loc[mask_unlabeled, "submission"] = "Not specified"

    # texto: remove espaços extras nas colunas de nome/categoria
    text_cols = ["winner_name", "loser_name", "win_type", "submission",
                 "weight_class", "sex", "stage"]
    for col in text_cols:
        df[col] = df[col].str.strip()

    # categorias como category dtype (mais leve, evita erro de digitação)
    for col in ["win_type", "weight_class", "sex", "stage"]:
        df[col] = df[col].astype("category")

    df = df.sort_values(["year", "match_id"]).reset_index(drop=True)

    df.to_csv(OUT_CSV, index=False)
    df.to_excel(OUT_XLSX, index=False, sheet_name="adcc_clean")

    print(f"Linhas: {len(df)} | Colunas: {list(df.columns)}")
    print(f"Salvo em {OUT_CSV} e {OUT_XLSX}")


if __name__ == "__main__":
    clean()
