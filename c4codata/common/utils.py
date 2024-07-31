from datetime import datetime
from settings import auto_config as config

def calc_execution_time(func):
    def wrapper(*args, **kwargs):
        start = datetime.now()
        result = func(*args, **kwargs)
        end = datetime.now()
        if (config.DEBUG):
            print(f"Function {func.__name__} execution time: {end-start}")
        return result
    return wrapper