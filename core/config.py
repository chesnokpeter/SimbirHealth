import os

postgres_url = os.environ.get('POSTGRES_URL')
secret_key = os.environ.get('SECRET_KEY')
redis_port = int(os.environ.get('REDIS_PORT'))
redis_host = os.environ.get('REDIS_HOST')