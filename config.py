from decouple import config

API_ID = config('API_ID', cast=int)
API_HASH = config('API_HASH')
BOT_TOKEN = config('BOT_TOKEN')

DB_URL = '{}://{}:{}@{}:{}/{}'.format(
    config('DB_ENGINE', default='postgresql'),
    config('DB_USERNAME', default='postgres'),
    config('DB_PASS', default='password'),
    config('DB_HOST', default='localhost'),
    config('DB_PORT', default='5432'),
    config('DB_NAME', default='mydatabase')
)
