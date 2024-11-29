import time
from operations_db import (
    insert_simple_records,
    insert_large_records,
    insert_bulk_records,
    read_filtered_records, 
    read_sorted_records, 
    update_specific_records, 
    delete_filtered_records, 
    create_index, 
    complex_query, 
    aggregation_query
)
from utils import random_string
from log import CSV_FILE, read_csv, insert_records_from_csv
from pymongo import MongoClient

def process_data(num_records, collection):
    """ Limita o número de registros a serem processados. """
    # Ler registros do CSV
    print(f"Lendo {num_records} registros do CSV...")
    records_from_csv = read_csv(CSV_FILE)
    records_from_csv = records_from_csv[:num_records]  # Limita a quantidade de registros lidos
    print(f"{len(records_from_csv)} registros lidos do CSV.")

    # Inserir registros no banco de dados
    print(f"Inserindo {num_records} registros no banco de dados...")
    insert_records_from_csv(collection, records_from_csv)

    return records_from_csv

def main():
    # Configuração do MongoDB
    MONGO_URI = "mongodb://root:mylittlepassword@mongo:27017"
    DATABASE_NAME = "benchmark_db"
    COLLECTION_NAME = "benchmark_collection"
    
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]
    
    # Inicializa os testes com registros (aumentando os números)
    insert_simple_records(10000, collection)  # Aumentando para 10.000 registros simples
    insert_large_records(50000, collection)  # Aumentando para 50.000 registros grandes
    insert_bulk_records(20000, collection)   # Aumentando para 20.000 registros em massa
    read_filtered_records(1000, collection)  # Lendo 1000 registros filtrados
    create_index(collection)

    # Processar e inserir registros do CSV (aumentando para 500 registros)
    records = process_data(500, collection)  # Processando 500 registros

    # Realizar outras operações de leitura e atualização
    read_sorted_records(1000, collection)   # Lendo 1000 registros ordenados
    update_specific_records(1000, collection)  # Atualizando 1000 registros
    delete_filtered_records(1000, collection)  # Deletando 1000 registros
    complex_query(1000, collection)         # Consulta complexa com 1000 registros
    aggregation_query(collection)           # Realizando a agregação

if __name__ == "__main__":
    main()
