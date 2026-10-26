
from pathlib import Path
import pandas as pd


def extrair_dados():
    pasta_dados = Path("data/raw")

    arquivos = {
        "orders": "olist_orders_dataset.csv",
        "order_items": "olist_order_items_dataset.csv",
        "customers": "olist_customers_dataset.csv",
        "products": "olist_products_dataset.csv",
        "sellers": "olist_sellers_dataset.csv",
        "category_translation": "product_category_name_translation.csv",
    }

    dados = {}

    for nome, arquivo in arquivos.items():
        caminho = pasta_dados / arquivo

        if not caminho.exists():
            raise FileNotFoundError(
                f"Arquivo não encontrado: {caminho}"
            )

        dados[nome] = pd.read_csv(caminho)

    return dados
