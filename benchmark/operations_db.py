from random import randint
from benchmark_decorator import benchmark
from log import log_action
from utils import random_string

@benchmark 
def insert_simple_records(quantity, collection):
    records = [{"record_id": i, "value": randint(1, 100)} for i in range(quantity)]
    result = collection.insert_many(records)
    log_action("INSERT", f"{len(result.inserted_ids)} registros simples inseridos.")
@benchmark 
def insert_large_records(quantity, collection):
    records = [{"record_id": i, "value": randint(1, 100), "extra_data": random_string(100)} for i in range(quantity)]
    result = collection.insert_many(records)
    log_action("INSERT", f"{len(result.inserted_ids)} registros grandes inseridos.")
@benchmark 
def read_filtered_records(quantity, collection):
    results = list(collection.find({"value": {"$gt": 50}}).limit(quantity))
    log_action("READ", f"{len(results)} registros filtrados lidos.")
    return results
@benchmark 
def read_sorted_records(quantity, collection):
    results = list(collection.find().sort("value", 1).limit(quantity))
    log_action("READ", f"{len(results)} registros lidos com ordenação.")
    return results
@benchmark 
def update_specific_records(quantity, collection):
    updated_count = 0
    for record in collection.find({"value": {"$lt": 50}}).limit(quantity):
        result = collection.update_one(
            {"_id": record["_id"]},
            {"$set": {"value": record["value"] + 10}}
        )
        updated_count += result.modified_count
    log_action("UPDATE", f"{updated_count} registros específicos atualizados.")
@benchmark 
def delete_filtered_records(quantity, collection):
    deleted_count = 0
    for record in collection.find({"value": {"$lt": 50}}).limit(quantity):
        result = collection.delete_one({"_id": record["_id"]})
        deleted_count += result.deleted_count
    log_action("DELETE", f"{deleted_count} registros filtrados removidos.")
