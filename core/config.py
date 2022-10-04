from environs import Env

env = Env()
env.read_env()

TTL = 30000  # time to live token
JWT_secret = env.str('SECRET')
JWT_algorithm = env.str('ALGORITHM')
DATABASE_URL = env.str('DATABASE_URL')
ENCRYPTION_SCHEMAS = env.str('ENCRYPTION_SCHEMAS')
TYPE_TOKEN = env.str('TYPE_TOKEN')
PORT = env.int('PORT')
ROUT = env.str('ROUT')
SECRET_TOKEN = env.str('SECRET_TOKEN')
