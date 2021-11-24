import datetime
from pydantic import BaseSettings



class ServerSettings(BaseSettings):
    SECRET_KEY: str = "576E5A7234753778214125442A472D4B6150645367556B58703273357638792F"
    HOST: str = '0.0.0.0'
    PORT: int = 8000
    DEBUG: bool = True
    RELOAD: bool = True
    

class DatabaseSettings(BaseSettings):
    DB_HOST: str = "localhost"
    DB_PORT: int = "5432"
    DB_NAME: str = "authserver"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"

class JwtTokenSettings(BaseSettings):
    EXPIRATION_TIME = datetime.timedelta(days=1,hours=0,minutes=0,seconds=0)

class CombineSettings(ServerSettings,DatabaseSettings,JwtTokenSettings):...

settings = CombineSettings()
