from environs import Env

env = Env()
env.read_env()


DATABASE_URL = env.str('DATABASE_URL')
PORT = env.int('PORT')
ROUT = env.str('ROUT')
SECRET_TOKEN = env.str('SECRET_TOKEN')
URL_NEWSLETTERS = env.str('URL_NEWSLETTERS')
