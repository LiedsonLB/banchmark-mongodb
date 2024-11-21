from pymongo import MongoClient

try:
    client = MongoClient("mongodb://mongo:27017")
    print("Conexão com MongoDB bem-sucedida!")
except Exception as e:
    print(f"Erro ao conectar com MongoDB: {e}")
