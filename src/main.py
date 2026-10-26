
from src.extract import extrair_dados
from src.transform import transformar_dados
from src.load import carregar_dados
from src.warehouse import carregar_data_warehouse
from src.data_quality import validar_qualidade_dados


def executar_pipeline():
    """Executa o pipeline ETL completo."""

    print("Iniciando pipeline ETL...")

    print("\n[1/4] Extraindo dados dos arquivos CSV...")
    dados = extrair_dados()

    for nome, df in dados.items():
        print(f"  {nome}: {len(df)} registros extraídos")

    print("\n[2/4] Transformando os dados...")
    dados_transformados = transformar_dados(dados)

    for nome, df in dados_transformados.items():
        print(f"  {nome}: {len(df)} registros transformados")

    print("\n[3/4] Carregando dados no staging...")
    carregar_dados(dados_transformados)

    print("\n[4/4] Carregando o Data Warehouse...")
    carregar_data_warehouse()

    print("\nValidando a qualidade dos dados...")
    validar_qualidade_dados()

    print("\nPipeline ETL concluído com sucesso!")


if __name__ == "__main__":
    try:
        executar_pipeline()
    except Exception as erro:
        print(f"\nErro durante a execução do pipeline: {erro}")
        raise
