import time
from log import log_action

# Função de benchmark para medir o tempo de execução
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