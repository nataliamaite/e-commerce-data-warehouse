
import pandas as pd

from src.transform import transformar_dados


def criar_dados_teste():
    return {
        "orders": pd.DataFrame({
            "order_id": ["pedido1", "pedido2"],
            "customer_id": ["cliente1", "cliente2"],
            "order_status": ["delivered", "shipped"],
            "order_purchase_timestamp": [
                "2017-10-02 10:00:00",
                "data_invalida",
            ],
            "order_approved_at": [
                "2017-10-02 11:00:00",
                None,
            ],
            "order_delivered_carrier_date": [None, None],
            "order_delivered_customer_date": [None, None],
            "order_estimated_delivery_date": [
                "2017-10-10 00:00:00",
                "2017-10-15 00:00:00",
            ],
        }),
        "order_items": pd.DataFrame({
            "order_id": ["pedido1", "pedido2"],
            "order_item_id": ["1", "2"],
            "product_id": ["produto1", "produto2"],
            "seller_id": ["vendedor1", "vendedor2"],
            "shipping_limit_date": [
                "2017-10-05 00:00:00",
                None,
            ],
            "price": ["100.50", "200.00"],
            "freight_value": ["15.50", "valor_invalido"],
        }),
        "customers": pd.DataFrame({
            "customer_id": ["cliente1"],
            "customer_unique_id": [" unico1 "],
            "customer_zip_code_prefix": ["12345"],
            "customer_city": [" São Paulo "],
            "customer_state": ["sp"],
        }),
        "products": pd.DataFrame({
            "product_id": ["produto1"],
            "product_category_name": [" Beleza "],
            "product_name_lenght": ["10"],
            "product_description_lenght": ["100"],
            "product_photos_qty": ["2"],
            "product_weight_g": ["500.5"],
            "product_length_cm": ["20"],
            "product_height_cm": ["10"],
            "product_width_cm": ["15"],
        }),
        "sellers": pd.DataFrame({
            "seller_id": ["vendedor1"],
            "seller_zip_code_prefix": ["12345"],
            "seller_city": [" João Pessoa "],
            "seller_state": ["pb"],
        }),
        "category_translation": pd.DataFrame({
            "product_category_name": [
                " beleza ",
                "beleza",
            ],
            "product_category_name_english": [
                " beauty ",
                "beauty",
            ],
        }),
    }


def test_transformar_dados_retorna_seis_conjuntos():
    dados = criar_dados_teste()

    resultado = transformar_dados(dados)

    assert len(resultado) == 6
    assert set(resultado.keys()) == set(dados.keys())


def test_orders_converte_colunas_de_data():
    dados = criar_dados_teste()

    resultado = transformar_dados(dados)
    orders = resultado["orders"]

    assert pd.api.types.is_datetime64_any_dtype(
        orders["order_purchase_timestamp"]
    )
    assert pd.isna(orders.loc[1, "order_purchase_timestamp"])


def test_order_items_converte_valores_numericos():
    dados = criar_dados_teste()

    resultado = transformar_dados(dados)
    items = resultado["order_items"]

    assert pd.api.types.is_numeric_dtype(items["price"])
    assert items.loc[0, "price"] == 100.50
    assert pd.isna(items.loc[1, "freight_value"])


def test_customers_padroniza_textos():
    dados = criar_dados_teste()

    resultado = transformar_dados(dados)
    customers = resultado["customers"]

    assert customers.loc[0, "customer_city"] == "são paulo"
    assert customers.loc[0, "customer_state"] == "SP"
    assert customers.loc[0, "customer_unique_id"] == "unico1"


def test_products_converte_medidas_numericas():
    dados = criar_dados_teste()

    resultado = transformar_dados(dados)
    products = resultado["products"]

    assert products.loc[0, "product_weight_g"] == 500.5
    assert pd.api.types.is_numeric_dtype(
        products["product_weight_g"]
    )


def test_sellers_padroniza_textos():
    dados = criar_dados_teste()

    resultado = transformar_dados(dados)
    sellers = resultado["sellers"]

    assert sellers.loc[0, "seller_city"] == "joão pessoa"
    assert sellers.loc[0, "seller_state"] == "PB"


def test_category_translation_remove_duplicidades():
    dados = criar_dados_teste()

    resultado = transformar_dados(dados)
    categorias = resultado["category_translation"]

    assert len(categorias) == 1
    assert categorias.iloc[0]["product_category_name"] == "beleza"
    assert categorias.iloc[0]["product_category_name_english"] == "beauty"


def test_dados_originais_nao_sao_modificados():
    dados = criar_dados_teste()
    orders_originais = dados["orders"].copy(deep=True)

    transformar_dados(dados)

    pd.testing.assert_frame_equal(
        dados["orders"],
        orders_originais
    )
