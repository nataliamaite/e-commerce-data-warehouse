
import os

import psycopg2
import pytest
from dotenv import load_dotenv

load_dotenv()


@pytest.fixture
def conexao():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "ecommerce_dw"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD"),
    )

    yield conn
    conn.close()


def executar_contagem(conexao, consulta):
    with conexao.cursor() as cursor:
        cursor.execute(consulta)
        return cursor.fetchone()[0]


def test_nao_existem_itens_duplicados(conexao):
    consulta = """
        SELECT COUNT(*)
        FROM (
            SELECT order_id, order_item_id
            FROM dw.fato_vendas
            GROUP BY order_id, order_item_id
            HAVING COUNT(*) > 1
        ) AS duplicados;
    """

    assert executar_contagem(conexao, consulta) == 0


def test_nao_existem_medidas_nulas(conexao):
    consulta = """
        SELECT COUNT(*)
        FROM dw.fato_vendas
        WHERE preco IS NULL
           OR valor_frete IS NULL
           OR valor_total_item IS NULL;
    """

    assert executar_contagem(conexao, consulta) == 0


def test_nao_existem_medidas_negativas(conexao):
    consulta = """
        SELECT COUNT(*)
        FROM dw.fato_vendas
        WHERE preco < 0
           OR valor_frete < 0
           OR valor_total_item < 0;
    """

    assert executar_contagem(conexao, consulta) == 0


def test_valor_total_corresponde_ao_preco_mais_frete(conexao):
    consulta = """
        SELECT COUNT(*)
        FROM dw.fato_vendas
        WHERE valor_total_item <> preco + valor_frete;
    """

    assert executar_contagem(conexao, consulta) == 0


@pytest.mark.parametrize(
    ("tabela_fato", "chave_fato", "tabela_dimensao", "chave_dimensao"),
    [
        ("fato_vendas", "sk_cliente", "dim_cliente", "sk_cliente"),
        ("fato_vendas", "sk_produto", "dim_produto", "sk_produto"),
        ("fato_vendas", "sk_vendedor", "dim_vendedor", "sk_vendedor"),
        ("fato_vendas", "sk_tempo", "dim_tempo", "sk_tempo"),
    ],
)
def test_integridade_referencial(
    conexao,
    tabela_fato,
    chave_fato,
    tabela_dimensao,
    chave_dimensao,
):
    consulta = f"""
        SELECT COUNT(*)
        FROM dw.{tabela_fato} f
        LEFT JOIN dw.{tabela_dimensao} d
            ON f.{chave_fato} = d.{chave_dimensao}
        WHERE d.{chave_dimensao} IS NULL;
    """

    assert executar_contagem(conexao, consulta) == 0
