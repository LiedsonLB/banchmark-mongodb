from random import randint
from benchmark_decorator import benchmark
from log import log_action
from utils import random_string

# Testes de inserção de registros simples
@benchmark
def insert_simple_records(quantity, collection):
    records = [{"record_id": i, "value": randint(1, 100)} for i in range(quantity)]
    result = collection.insert_many(records)
    log_action("INSERT", f"{len(result.inserted_ids)} registros simples inseridos com sucesso.")

# Testes de inserção de registros grandes
@benchmark
def insert_large_records(quantity, collection):
    records = [{"record_id": i, "value": randint(1, 100), "extra_data": random_string(100)} for i in range(quantity)]
    result = collection.insert_many(records)
    log_action("INSERT", f"{len(result.inserted_ids)} registros grandes inseridos com sucesso.")

# Testes de leitura filtrada de registros
@benchmark
def read_filtered_records(quantity, collection):
    results = list(collection.find({"value": {"$gt": 50}}).limit(quantity))
    log_action("READ", f"{len(results)} registros filtrados lidos (valor > 50).")
    return results

# Testes de leitura com ordenação de registros
@benchmark
def read_sorted_records(quantity, collection):
    results = list(collection.find().sort("value", 1).limit(quantity))
    log_action("READ", f"{len(results)} registros ordenados por 'value' (ascendente) lidos.")
    return results

# Testes de atualização de registros específicos
@benchmark
def update_specific_records(quantity, collection):
    updated_count = 0
    for record in collection.find({"value": {"$lt": 50}}).limit(quantity):
        result = collection.update_one(
            {"_id": record["_id"]},
            {"$set": {"value": record["value"] + 10}}
        )
        updated_count += result.modified_count
    log_action("UPDATE", f"{updated_count} registros com 'value' < 50 atualizados para novo valor.")

# Testes de exclusão de registros filtrados
@benchmark
def delete_filtered_records(quantity, collection):
    deleted_count = 0
    for record in collection.find({"value": {"$lt": 50}}).limit(quantity):
        result = collection.delete_one({"_id": record["_id"]})
        deleted_count += result.deleted_count
    log_action("DELETE", f"{deleted_count} registros com 'value' < 50 deletados.")

# Testes de inserção em massa
@benchmark
def insert_bulk_records(quantity, collection):
    records = [{"record_id": i, "value": randint(1, 100)} for i in range(quantity)]
    result = collection.insert_many(records)
    log_action("INSERT", f"{len(result.inserted_ids)} registros inseridos em massa.")

# Testes de leitura com projeção
@benchmark
def read_with_projection(quantity, collection):
    results = list(collection.find({"value": {"$gt": 50}}, {"record_id": 1, "value": 1}).limit(quantity))
    log_action("READ", f"{len(results)} registros lidos com projeção (apenas 'record_id' e 'value').")
    return results

# Testes de atualização em massa
@benchmark
def update_bulk_records(quantity, collection):
    updated_count = collection.update_many(
        {"value": {"$lt": 50}},
        {"$set": {"value": 100}}
    ).modified_count
    log_action("UPDATE", f"{updated_count} registros atualizados em massa com 'value' < 50.")

# Testes de exclusão em massa
@benchmark
def delete_bulk_records(quantity, collection):
    deleted_count = collection.delete_many({"value": {"$lt": 50}}).deleted_count
    log_action("DELETE", f"{deleted_count} registros deletados em massa com 'value' < 50.")

# Testes de criação de índice
@benchmark
def create_index(collection):
    index = collection.create_index([("value", 1)])
    log_action("INDEX", f"Índice criado para o campo 'value' com sucesso. Índice: {index}.")

# Testes de consultas complexas (usando operadores lógicos)
@benchmark
def complex_query(quantity, collection):
    results = list(collection.find({"$or": [{"value": {"$gt": 75}}, {"value": {"$lt": 25}}]}).limit(quantity))
    log_action("READ", f"{len(results)} registros lidos com consulta complexa (OR: 'value' > 75 ou 'value' < 25).")
    return results

# Teste de leitura com agregação
@benchmark
def aggregation_query(collection):
    pipeline = [
        {"$group": {"_id": "$value", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 5}
    ]
    results = list(collection.aggregate(pipeline))
    log_action("AGGREGATE", f"5 valores mais frequentes encontrados com agregação: {results}")
    return results