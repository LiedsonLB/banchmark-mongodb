import time
from operations_db import insert_simple_records, insert_large_records, read_filtered_records, read_sorted_records, update_specific_records, delete_filtered_records
from utils import random_string

if __name__ == "__main__":
    # Limpar a coleção antes de iniciar o teste
    from pymongo import MongoClient

    MONGO_URI = "mongodb://root:mylittlepassword@mongo:27017"
    DATABASE_NAME = "benchmark_db"
    COLLECTION_NAME = "benchmark_collection"
    
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]

    collection.delete_many({})
    print("Coleção limpa.")

    # Inserir registros simples
    print("Inserindo registros simples...")
    insert_simple_records(1000, collection)

    # Inserir registros grandes
    print("Inserindo registros grandes...")
    insert_large_records(10000, collection)

    # Ler registros filtrados
    print("Lendo registros filtrados...")
    filtered_records = read_filtered_records(10, collection)
    print(f"Registros filtrados: {filtered_records}")

    # Ler registros com ordenação
    print("Lendo registros com ordenação...")
    sorted_records = read_sorted_records(10, collection)
    print(f"Registros ordenados: {sorted_records}")

    # Atualizar registros específicos
    print("Atualizando registros específicos...")
    update_specific_records(10000, collection)

    # Deletar registros filtrados
    print("Deletando registros filtrados...")
    delete_filtered_records(50, collection)

    # Leitura final
    print("Lendo registros finais...")
    final_records = read_filtered_records(10, collection)
    print(f"Registros finais: {final_records}")
