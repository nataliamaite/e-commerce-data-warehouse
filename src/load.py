
import os

import numpy as np
import pandas as pd
import psycopg2
from dotenv import load_dotenv
from psycopg2 import sql
from psycopg2.extras import execute_values


load_dotenv()

TABELAS = {
    "orders": "orders",
    "order_items": "order_items",
    "customers": "customers",
    "products": "products",
    "sellers": "sellers",
    "category_translation": "category_translation",
}



def carregar_dados(dados):
    """
    Substitui os dados do staging dentro de uma transação.
    Se ocorrer um erro, desfaz a carga.
    """
    conexao = psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "ecommerce_dw"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD"),
    )

    try:
        with conexao.cursor() as cursor:
            # Limpa as tabelas de staging dentro da transação.
            cursor.execute("""
                TRUNCATE TABLE
                    staging.orders,
                    staging.order_items,
                    staging.customers,
                    staging.products,
                    staging.sellers,
                    staging.category_translation;
            """)

            for nome_dados, nome_tabela in TABELAS.items():
                if nome_dados not in dados:
                    raise ValueError(
                        f"Conjunto de dados ausente: {nome_dados}"
                    )

                df = dados[nome_dados]

                if not isinstance(df, pd.DataFrame):
                    raise TypeError(
                        f"{nome_dados} precisa ser um DataFrame do Pandas"
                    )

                if df.empty:
                    continue

                colunas = list(df.columns)

                comando = sql.SQL(
                    "INSERT INTO {}.{} ({}) VALUES %s"
                ).format(
                    sql.Identifier("staging"),
                    sql.Identifier(nome_tabela),
                    sql.SQL(", ").join(
                        sql.Identifier(coluna) for coluna in colunas
                    ),
                )

                valores = [
                    tuple(
                        None
                        if pd.isna(valor)
                        else valor.item()
                        if isinstance(valor, np.generic)
                        else valor
                        for valor in linha
                    )
                    for linha in df.itertuples(index=False, name=None)
                ]

                execute_values(
                    cursor,
                    comando.as_string(conexao),
                    valores,
                    page_size=1000,
                )

        conexao.commit()

    except Exception:
        conexao.rollback()
        raise

    finally:
        conexao.close()
