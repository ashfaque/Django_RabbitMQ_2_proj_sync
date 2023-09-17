
import os

if __name__ == '__main__':
    conda_env_name = 'rmqenv'
    os.system(f'C:\\Users\\%USERNAME%\\.conda\\envs\\{conda_env_name}\\python.exe -m uvicorn drf_RabbitMQ_2_proj_sync.asgi:application --reload --host 0.0.0.0 --port 8001 --workers 1 --use-colors --log-level info')
