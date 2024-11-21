import time
from pymongo import MongoClient
from random import randint, choice
import string

# Configuração do MongoDB
MONGO_URI = "mongodb://root:mylittlepassword@mongo:27017"
DATABASE_NAME = "benchmark_db"
COLLECTION_NAME = "benchmark_collection"

# Nome do arquivo de log
LOG_FILE = "benchmark_log.txt"

# Conexão com o MongoDB
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

# Função para registrar logs
def log_action(action, message):
    with open(LOG_FILE, "a") as log:
        log.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {action}: {message}\n")

# Função para medir o tempo de execução
def benchmark(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        elapsed_time = end - start
        log_action("BENCHMARK", f"{func.__name__} executado em {elapsed_time:.6f} segundos")
        print(f"{func.__name__}: {elapsed_time:.6f} segundos")
        return result
    return wrapper

# Função auxiliar para gerar strings aleatórias
def random_string(length=10):
    return ''.join(choice(string.ascii_letters + string.digits) for _ in range(length))

# Operações no MongoDB
@benchmark
def insert_simple_records(quantity):
    records = [{"record_id": i, "value": randint(1, 100)} for i in range(quantity)]
    result = collection.insert_many(records)
    log_action("INSERT", f"{len(result.inserted_ids)} registros simples inseridos.")

@benchmark
def insert_large_records(quantity):
    records = [{"record_id": i, "value": randint(1, 100), "extra_data": random_string(100)} for i in range(quantity)]
    result = collection.insert_many(records)
    log_action("INSERT", f"{len(result.inserted_ids)} registros grandes inseridos.")

@benchmark
def read_filtered_records(quantity):
    results = list(collection.find({"value": {"$gt": 50}}).limit(quantity))
    log_action("READ", f"{len(results)} registros filtrados lidos.")
    return results

@benchmark
def read_sorted_records(quantity):
    results = list(collection.find().sort("value", 1).limit(quantity))
    log_action("READ", f"{len(results)} registros lidos com ordenação.")
    return results

@benchmark
def update_specific_records(quantity):
    updated_count = 0
    for record in collection.find({"value": {"$lt": 50}}).limit(quantity):
        result = collection.update_one(
            {"_id": record["_id"]},
            {"$set": {"value": record["value"] + 10}}
        )
        updated_count += result.modified_count
    log_action("UPDATE", f"{updated_count} registros específicos atualizados.")

@benchmark
def delete_filtered_records(quantity):
    deleted_count = 0
    for record in collection.find({"value": {"$lt": 50}}).limit(quantity):
        result = collection.delete_one({"_id": record["_id"]})
        deleted_count += result.deleted_count
    log_action("DELETE", f"{deleted_count} registros filtrados removidos.")

# Testando o benchmark
if __name__ == "__main__":
    # Limpar a coleção antes de iniciar o teste
    collection.delete_many({})
    print("Coleção limpa.")

    # Inserir registros simples
    print("Inserindo registros simples...")
    insert_simple_records(100)

    # Inserir registros grandes
    print("Inserindo registros grandes...")
    insert_large_records(100)

    # Ler registros filtrados
    print("Lendo registros filtrados...")
    filtered_records = read_filtered_records(10)
    print(f"Registros filtrados: {filtered_records}")

    # Ler registros com ordenação
    print("Lendo registros com ordenação...")
    sorted_records = read_sorted_records(10)
    print(f"Registros ordenados: {sorted_records}")

    # Atualizar registros específicos
    print("Atualizando registros específicos...")
    update_specific_records(10)

    # Deletar registros filtrados
    print("Deletando registros filtrados...")
    delete_filtered_records(5)

    # Leitura final
    print("Lendo registros finais...")
    final_records = read_filtered_records(10)
    print(f"Registros finais: {final_records}")