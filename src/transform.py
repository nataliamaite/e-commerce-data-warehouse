import pandas as pd


def transformar_dados(dados):
    """
    Transforma e padroniza os seis conjuntos de dados do Olist.
    Retorna um novo dicionário com os DataFrames transformados.
    """
    dados_transformados = {}

    # 1. Pedidos
    orders = dados["orders"].copy()

    colunas_data_orders = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ]

    for coluna in colunas_data_orders:
        orders[coluna] = pd.to_datetime(
            orders[coluna],
            errors="coerce"
        )

    dados_transformados["orders"] = orders

    # 2. Itens dos pedidos
    order_items = dados["order_items"].copy()

    order_items["shipping_limit_date"] = pd.to_datetime(
        order_items["shipping_limit_date"],
        errors="coerce"
    )

    colunas_inteiras = ["order_item_id"]

    for coluna in colunas_inteiras:
        order_items[coluna] = pd.to_numeric(
            order_items[coluna],
            errors="coerce"
        ).astype("Int64")

    colunas_numericas = ["price", "freight_value"]

    for coluna in colunas_numericas:
        order_items[coluna] = pd.to_numeric(
            order_items[coluna],
            errors="coerce"
        )

    dados_transformados["order_items"] = order_items

    # 3. Clientes
    customers = dados["customers"].copy()

    colunas_texto_customers = [
        "customer_id",
        "customer_unique_id",
        "customer_zip_code_prefix",
        "customer_city",
        "customer_state",
    ]

    for coluna in colunas_texto_customers:
        customers[coluna] = customers[coluna].astype("string").str.strip()

    customers["customer_city"] = customers["customer_city"].str.lower()
    customers["customer_state"] = customers["customer_state"].str.upper()

    dados_transformados["customers"] = customers

    # 4. Produtos
    products = dados["products"].copy()

    colunas_inteiras_products = [
        "product_name_lenght",
        "product_description_lenght",
        "product_photos_qty",
    ]

    for coluna in colunas_inteiras_products:
        products[coluna] = pd.to_numeric(
            products[coluna],
            errors="coerce"
        ).astype("Int64")

    colunas_numericas_products = [
        "product_weight_g",
        "product_length_cm",
        "product_height_cm",
        "product_width_cm",
    ]

    for coluna in colunas_numericas_products:
        products[coluna] = pd.to_numeric(
            products[coluna],
            errors="coerce"
        )

    products["product_category_name"] = (
        products["product_category_name"]
        .astype("string")
        .str.strip()
        .str.lower()
    )

    dados_transformados["products"] = products

    # 5. Vendedores
    sellers = dados["sellers"].copy()

    colunas_texto_sellers = [
        "seller_id",
        "seller_zip_code_prefix",
        "seller_city",
        "seller_state",
    ]

    for coluna in colunas_texto_sellers:
        sellers[coluna] = sellers[coluna].astype("string").str.strip()

    sellers["seller_city"] = sellers["seller_city"].str.lower()
    sellers["seller_state"] = sellers["seller_state"].str.upper()

    dados_transformados["sellers"] = sellers

    # 6. Tradução das categorias
    category_translation = dados["category_translation"].copy()

    for coluna in [
        "product_category_name",
        "product_category_name_english",
    ]:
        category_translation[coluna] = (
            category_translation[coluna]
            .astype("string")
            .str.strip()
            .str.lower()
        )

    category_translation = category_translation.drop_duplicates(
        subset=["product_category_name"],
        keep="first"
    )

    dados_transformados["category_translation"] = category_translation

    return dados_transformados