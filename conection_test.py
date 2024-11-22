from pymongo import MongoClient

try:
    client = MongoClient("mongodb://dayana:ohTh#aiT6g@170.245.33.221:27017/")
    print("Conexão com MongoDB bem-sucedida!")
except Exception as e:
    print(f"Erro ao conectar com MongoDB: {e}")
