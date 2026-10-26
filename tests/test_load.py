
import pandas as pd
import pytest
from unittest.mock import MagicMock

from src import load


def criar_dados_teste():
    return {
        "orders": pd.DataFrame({
            "order_id": ["pedido1"],
            "customer_id": ["cliente1"],
            "order_status": ["delivered"],
            "order_purchase_timestamp": [
                pd.Timestamp("2017-10-02 10:00:00")
            ],
            "order_approved_at": [None],
            "order_delivered_carrier_date": [None],
            "order_delivered_customer_date": [None],
            "order_estimated_delivery_date": [
                pd.Timestamp("2017-10-10 00:00:00")
            ],
        }),
        "order_items": pd.DataFrame({
            "order_id": ["pedido1"],
            "order_item_id": [1],
            "product_id": ["produto1"],
            "seller_id": ["vendedor1"],
            "shipping_limit_date": [
                pd.Timestamp("2017-10-05 00:00:00")
            ],
            "price": [100.50],
            "freight_value": [15.50],
        }),
        "customers": pd.DataFrame({
            "customer_id": ["cliente1"],
            "customer_unique_id": ["unico1"],
            "customer_zip_code_prefix": ["12345"],
            "customer_city": ["joão pessoa"],
            "customer_state": ["PB"],
        }),
        "products": pd.DataFrame({
            "product_id": ["produto1"],
            "product_category_name": ["beleza"],
            "product_name_lenght": [10],
            "product_description_lenght": [100],
            "product_photos_qty": [2],
            "product_weight_g": [500.5],
            "product_length_cm": [20],
            "product_height_cm": [10],
            "product_width_cm": [15],
        }),
        "sellers": pd.DataFrame({
            "seller_id": ["vendedor1"],
            "seller_zip_code_prefix": ["12345"],
            "seller_city": ["joão pessoa"],
            "seller_state": ["PB"],
        }),
        "category_translation": pd.DataFrame({
            "product_category_name": ["beleza"],
            "product_category_name_english": ["beauty"],
        }),
    }


def configurar_conexao_falsa(monkeypatch):
    conexao = MagicMock()
    cursor = MagicMock()

    conexao.cursor.return_value.__enter__.return_value = cursor

    monkeypatch.setattr(
        load.psycopg2,
        "connect",
        MagicMock(return_value=conexao)
    )

    monkeypatch.setattr(
        load,
        "execute_values",
        MagicMock()
    )

    # Evita que psycopg2 tente formatar identificadores
    # SQL com uma conexão simulada.
    comando_sql = MagicMock()
    comando_sql.format.return_value = comando_sql
    comando_sql.join.return_value = comando_sql
    comando_sql.as_string.return_value = (
        "INSERT INTO staging.tabela VALUES %s"
    )

    monkeypatch.setattr(
        load.sql,
        "SQL",
        MagicMock(return_value=comando_sql)
    )

    monkeypatch.setattr(
        load.sql,
        "Identifier",
        MagicMock(return_value=MagicMock())
    )

    return conexao


def test_carregar_dados_insere_seis_conjuntos(monkeypatch):
    configurar_conexao_falsa(monkeypatch)
    dados = criar_dados_teste()

    load.carregar_dados(dados)

    assert load.execute_values.call_count == 6


def test_carregar_dados_converte_nulos_para_none(monkeypatch):
    configurar_conexao_falsa(monkeypatch)
    dados = criar_dados_teste()

    load.carregar_dados(dados)

    chamadas = load.execute_values.call_args_list
    valores_orders = chamadas[0].args[2]

    assert valores_orders[0][4] is None


def test_carregar_dados_rejeita_conjunto_ausente(monkeypatch):
    conexao = configurar_conexao_falsa(monkeypatch)
    dados = criar_dados_teste()
    del dados["orders"]

    with pytest.raises(ValueError, match="Conjunto de dados ausente"):
        load.carregar_dados(dados)

    conexao.rollback.assert_called_once()
    conexao.close.assert_called_once()


def test_carregar_dados_rejeita_valor_que_nao_e_dataframe(monkeypatch):
    conexao = configurar_conexao_falsa(monkeypatch)
    dados = criar_dados_teste()
    dados["orders"] = ["não é um DataFrame"]

    with pytest.raises(TypeError, match="precisa ser um DataFrame"):
        load.carregar_dados(dados)

    conexao.rollback.assert_called_once()
    conexao.close.assert_called_once()
