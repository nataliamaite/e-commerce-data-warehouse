
import os
from pathlib import Path

import psycopg2
from dotenv import load_dotenv

load_dotenv()


def carregar_data_warehouse():
    """Recria as dimensões e a tabela fato do Data Warehouse."""

    conexao = psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "ecommerce_dw"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD"),
    )

    pasta_projeto = Path(__file__).resolve().parent.parent
    arquivo_dimensoes = pasta_projeto / "sql" / "load_dimensions.sql"
    arquivo_fato = pasta_projeto / "sql" / "load_fact.sql"

    try:
        if not arquivo_dimensoes.exists():
            raise FileNotFoundError(
                f"Arquivo não encontrado: {arquivo_dimensoes}"
            )

        if not arquivo_fato.exists():
            raise FileNotFoundError(
                f"Arquivo não encontrado: {arquivo_fato}"
            )

        sql_dimensoes = arquivo_dimensoes.read_text(encoding="utf-8")
        sql_fato = arquivo_fato.read_text(encoding="utf-8")

        with conexao.cursor() as cursor:
            print("Recriando os dados do Data Warehouse...")

            cursor.execute("""
                TRUNCATE TABLE
                    dw.fato_vendas,
                    dw.dim_cliente,
                    dw.dim_produto,
                    dw.dim_vendedor,
                    dw.dim_tempo
                RESTART IDENTITY;
            """)

            print("Carregando dimensões...")
            cursor.execute(sql_dimensoes)

            print("Carregando tabela fato...")
            cursor.execute(sql_fato)

        conexao.commit()
        print("Data Warehouse carregado com sucesso!")

    except Exception:
        conexao.rollback()
        raise

    finally:
        conexao.close()
