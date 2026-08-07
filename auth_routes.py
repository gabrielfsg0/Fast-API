#criacao de um roteador
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from model import Usuario
from dependencies import pegar_sessao, verificar_token
from main import bcrypt_context, ACCESS_TOKEN_EXPIRE_MINUTS, ALGORITHM, SECRET_KEY
from schemas import UsurarioSchema
from schemas import LoginSchema
from jose import jwt, JWTError #utilizado para geracao de token e verificacao de erro de token
from datetime import datetime, timedelta, timezone #essa biblioteca é utilizada para atribuir horario no codigo ja que temos a criacao de token que dura 30 minutos
from fastapi.security import OAuth2PasswordRequestForm #criacao do formulario oauth2 


#passar duas variaveis: o caminho e tags
# a criacao de prefixo auxilia em dividir as rotas para nao ter conflito com outras rotas
auth_router = APIRouter(prefix = "/auth", tags = ["auth"])

#criacao do token de usuario 
def criar_token(id_usuario, duracao_token=timedelta(minutes= ACCESS_TOKEN_EXPIRE_MINUTS)): #aqui estou colocando como padrao um delta de 30 minutos 
    # JWT -> Json Web Token
    data_expiracao = datetime.now(timezone.utc) + duracao_token #timezone.utc passa o horario sem fuso - hora zero (regiao de greenwitch)
    dic_info = {"sub": str(id_usuario), "exp": data_expiracao}
    jwt_codificado = jwt.encode(dic_info, SECRET_KEY, ALGORITHM) #encode -> codificacao
    return jwt_codificado


def autenticar_usuario(email, senha, session):
    usuario = session.query(Usuario).filter(Usuario.email == email).first() #faz uma busca para ver se o email passado existe no banco de dados
    if not usuario:
        return False
    elif not bcrypt_context.verify(senha, usuario.senha): #compara se a senha nao é igual ao hash da senha (senha criptografada)
        return False
    return usuario


@auth_router.get("/")
async def home():
    """
    Essa é a rota padrao de autenticacao do nosso sistema. 
    """
    return {"mensagem": "voce acessou a rota padrao de autenticacao", "autenticado": False}


@auth_router.post("/criar_conta")
async def criar_conta(usuario_schema: UsurarioSchema, session: Session = Depends(pegar_sessao)): #o Depends informa que o session sera a resposta da funcao pegar_sessao, que entra como parametro
    usuario = session.query(Usuario).filter(Usuario.email == usuario_schema.email).first() #faco uma busca para identificar usuarios com o email passado durante a criacao do novo usuario

    if usuario: #nesse caso ele verifica que o usuario existe
        raise HTTPException(status_code=400, detail="Email do usuario ja cadastrado") #padroniza meu erro como code 400 e envia a msg requirida 
    else:
        senha_criptografada = bcrypt_context.hash(usuario_schema.senha) #hash é o codigo criptografado 
        novo_usuario = Usuario(usuario_schema.nome, usuario_schema.email, senha_criptografada, usuario_schema.ativo, usuario_schema.admin)
        session.add(novo_usuario) #adiciona no meu banco de dados o meu novo usuario
        session.commit() #salva todas alteracoes feitas no banco de dados durante a sessao
        return {"mensagem": f"usuario cadastrado com sucesso {usuario_schema.email}"}


# login -> email e senha -> token JWT(json web token)
@auth_router.post("/login")
async def login(login_schema: LoginSchema, session: Session = Depends(pegar_sessao)):
    usuario = autenticar_usuario(login_schema.email, login_schema.senha, session)#aplicacao da funcao verificando os dados do usuario definidos no LoginSchema
    if not usuario:
        raise HTTPException(status_code= 400, detail="Usuario nao encontrado ou credenciais invalidas")
    else: #como temos usuario, vamos criar um token para ele
        access_token = criar_token(usuario.id)
        refresh_token = criar_token(usuario.id, duracao_token=timedelta(days=7)) #nesse caso, meu token nao expira em 30 minutos e sim em 7 dias
        return {
            "access_token": access_token,
            "refrash_token": refresh_token,
            "token_type": "bearer"
            }

#segundo esquema de login para receber como paramentro o formulario de login OAuth2, para tratar autenticacao de barrer tokens
@auth_router.post("/login-form")
async def login_form(dados_formulario: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(pegar_sessao)):
    usuario = autenticar_usuario(dados_formulario.username, dados_formulario.password, session)
    if not usuario:
        raise HTTPException(status_code= 400, detail="Usuario nao encontrado ou credenciais invalidas")
    else:
        access_token = criar_token(usuario.id)
        return {
            "access_token": access_token,
            "token_type": "bearer"
            }

    
# o access token tem duracao de 30 min, o refresh tem duracao de 7 dias. Quando vence meu access token ele me da um refresh token, gerando a partir dele um novo access token
@auth_router.get("/refresh")
async def use_refresh_token(usuario: Usuario = Depends(verificar_token)):
    access_token = criar_token(usuario.id)
    return {
            "access_token": access_token,
            "token_type": "bearer"
            }

