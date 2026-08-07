from fastapi import FastAPI
from passlib.context import CryptContext #criar uma ferramenta para criptografar senhas
from fastapi.security import OAuth2PasswordBearer #utilizado para a criaçao do refresh token no heater permitindo uma criação de um access token a partir do refresh token
from dotenv import load_dotenv #carrega as variaveis ambientes que estao no arquivo .env
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTS = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTS"))


#criar uma instancia do fastapi
app = FastAPI()

#esquema de criptografia
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/login-form")

#apos a criacao do meu app eu posso criar minhas rotas, isso evita uma requisicao circular
 
from auth_routes import auth_router
from order_routes import order_router

# inclusao dos roteadores no meu app
app.include_router(auth_router)
app.include_router(order_router)





#cria um servidor usando o unicorv e executa o arquivo main
# para rodar nosso codigo executar no terminal: py -m uvicorn main:app --reload


# endpoit -> caminho da minha rota
# /ordens


# Rest APIs
# Get -> leitura/pegar
# Post -> enviar/criar
# Put/Patch -> edicao
# Delete -> deletar