
from src.extract import extrair_dados


def test_extrair_dados_retorna_seis_conjuntos():
    dados = extrair_dados()

    assert len(dados) == 6

    assert set(dados.keys()) == {
        "orders",
        "order_items",
        "customers",
        "products",
        "sellers",
        "category_translation",
    }
