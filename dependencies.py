from fastapi import Depends, HTTPException
from model import db
from sqlalchemy.orm import Session, sessionmaker #permite criacao de uma sessao no banco de dados para que seja realizada alguma alteracao
from model import Usuario
from jose import jwt, JWTError
from main import SECRET_KEY, ALGORITHM, oauth2_schema


def pegar_sessao():
    
    try:
        Session = sessionmaker(bind=db) 
        session = Session() 
        yield session 

    finally: 
        session.close() 



def verificar_token(token: str = Depends(oauth2_schema), session: Session = Depends(pegar_sessao)):
    try:
        dic_info = jwt.decode(token, SECRET_KEY, ALGORITHM) 
        id_usuario = dic_info.get("sub")
    except JWTError:
        raise HTTPException (status_code=401, detail="Acesso negado, verifique a validade do token")

    usuario = session.query(Usuario).filter(Usuario.id == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Acesso invalido")
    return usuario
