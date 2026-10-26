
import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()


def validar_qualidade_dados():
    """Valida regras básicas de qualidade da tabela fato."""

    consultas = {
        "Itens duplicados": """
            SELECT COUNT(*)
            FROM (
                SELECT order_id, order_item_id
                FROM dw.fato_vendas
                GROUP BY order_id, order_item_id
                HAVING COUNT(*) > 1
            ) AS duplicados;
        """,
        "Medidas nulas": """
            SELECT COUNT(*)
            FROM dw.fato_vendas
            WHERE preco IS NULL
               OR valor_frete IS NULL
               OR valor_total_item IS NULL;
        """,
        "Medidas negativas": """
            SELECT COUNT(*)
            FROM dw.fato_vendas
            WHERE preco < 0
               OR valor_frete < 0
               OR valor_total_item < 0;
        """,
        "Total diferente de preço + frete": """
            SELECT COUNT(*)
            FROM dw.fato_vendas
            WHERE valor_total_item <> preco + valor_frete;
        """,
        "Clientes sem dimensão correspondente": """
            SELECT COUNT(*)
            FROM dw.fato_vendas f
            LEFT JOIN dw.dim_cliente d
                ON f.sk_cliente = d.sk_cliente
            WHERE d.sk_cliente IS NULL;
        """,
        "Produtos sem dimensão correspondente": """
            SELECT COUNT(*)
            FROM dw.fato_vendas f
            LEFT JOIN dw.dim_produto d
                ON f.sk_produto = d.sk_produto
            WHERE d.sk_produto IS NULL;
        """,
        "Vendedores sem dimensão correspondente": """
            SELECT COUNT(*)
            FROM dw.fato_vendas f
            LEFT JOIN dw.dim_vendedor d
                ON f.sk_vendedor = d.sk_vendedor
            WHERE d.sk_vendedor IS NULL;
        """,
        "Datas sem dimensão correspondente": """
            SELECT COUNT(*)
            FROM dw.fato_vendas f
            LEFT JOIN dw.dim_tempo d
                ON f.sk_tempo = d.sk_tempo
            WHERE d.sk_tempo IS NULL;
        """,
    }

    conexao = psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "ecommerce_dw"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD"),
    )

    try:
        falhas = []

        with conexao.cursor() as cursor:
            for nome, consulta in consultas.items():
                cursor.execute(consulta)
                quantidade = cursor.fetchone()[0]

                if quantidade != 0:
                    falhas.append(f"{nome}: {quantidade} ocorrência(s)")
                    print(f"  FALHA — {nome}: {quantidade}")
                else:
                    print(f"  OK — {nome}")

        if falhas:
            raise RuntimeError(
                "Foram encontradas falhas de qualidade:\n"
                + "\n".join(falhas)
            )

        print("Todas as validações de qualidade passaram.")

    finally:
        conexao.close()
