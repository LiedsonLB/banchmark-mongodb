from datetime import datetime
from random import randint
import csv
import time
from pymongo import MongoClient

LOG_FILE = "benchmark_log.txt"
CSV_FILE = "data.csv"

def log_action(action, message):
    print(f"Logging action: {action} - {message}")  # Imprime no console para depuração
    try:
        with open(LOG_FILE, "a") as log:
            log.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {action}: {message}\n")
            log.flush()  # Garante que os dados sejam gravados imediatamente
    except Exception as e:
        print(f"Erro ao gravar no log: {e}")

def read_csv(file_path):
    """ Lê o arquivo CSV e retorna uma lista de registros """
    records = []
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Ajuste para usar 'user_id' em vez de 'record_id'
            records.append({
                "record_id": int(row["user_id"]),  # Usando 'user_id' como 'record_id'
                "full_name": row["full_name"],
                "email": row["email"],
                "birth_date": row["birth_date"],
                "street_address": row["street_address"],
                "city": row["city"],
                "state": row["state"],
                "postal_code": row["postal_code"],
                "last_order_date": row["last_order_date"],
                "total_spent": float(row["total_spent"]),  # Convertendo para float se for necessário
                "num_orders": int(row["num_orders"])  # Convertendo para inteiro se for necessário
            })
    return records

def insert_records_from_csv(collection, records):
    """ Insere registros lidos do CSV no MongoDB """
    result = collection.insert_many(records)
    log_action("INSERT", f"{len(result.inserted_ids)} registros inseridos do CSV.")

# Função para processar e preparar os registros do CSV para inserção
def prepare_record(row):
    # Convertendo os campos de data para datetime
    birth_date = datetime.strptime(row["birth_date"], "%Y-%m-%d")
    last_order_date = datetime.strptime(row["last_order_date"], "%Y-%m-%d")
    
    # Convertendo valores numéricos de forma segura
    total_spent = float(row["total_spent"]) if row["total_spent"].replace('.', '', 1).isdigit() else 0.0
    num_orders = int(row["num_orders"]) if row["num_orders"].isdigit() else 0
    
    # Criando o registro para inserir
    record = {
        "record_id": int(row["user_id"]),
        "full_name": row["full_name"],
        "email": row["email"],
        "birth_date": birth_date,
        "street_address": row["street_address"],
        "city": row["city"],
        "state": row["state"],
        "postal_code": row["postal_code"],
        "last_order_date": last_order_date,
        "total_spent": total_spent,
        "num_orders": num_orders
    }
    return record

def process_data(num_records, collection):
    """ Limita o número de registros a serem processados. """
    # Ler registros do CSV
    print(f"Lendo {num_records} registros do CSV...")
    records_from_csv = read_csv(CSV_FILE)
    records_from_csv = records_from_csv[:num_records]  # Limita a quantidade de registros lidos
    print(f"{len(records_from_csv)} registros lidos do CSV.")

    # Preparando os registros antes de inserir
    prepared_records = [prepare_record(row) for row in records_from_csv]
    
    # Inserir registros no banco de dados
    print(f"Inserindo {num_records} registros no banco de dados...")
    insert_records_from_csv(collection, prepared_records)

    return records_from_csv