from fastapi import Depends, HTTPException
from model import db
from sqlalchemy.orm import Session, sessionmaker #permite criacao de uma sessao no banco de dados para que seja realizada alguma alteracao
from model import Usuario
from jose import jwt, JWTError
from main import SECRET_KEY, ALGORITHM, oauth2_schema


def pegar_sessao():
    
#-----------------------------------------------------------------------------------------------------------------------
#Se durante a execucao da funcao na qual o pegar_funcao esta relacionado (neste caso seria a funcao criar_conta) 
# der algum erro, ele trava na linha de codigo yield sem realizar o close. Para arrumar isso, é necessario colocar dentro da estrutura try
#-----------------------------------------------------------------------------------------------------------------------

    try:
        Session = sessionmaker(bind=db) #ligacao da minha sessao com meu banco de dados criado no model.py
        session = Session() #inicializo minha sessao com o banco de dados
        yield session #pega o valor da sessao sem encerrar o funcionamento da funcao. 

    finally: #independente se deu certo ou errado o try, vamos realizar o session.close()
        session.close() #fecha minha sessao apos retornar pro usuario


#dependencia para verificar token
def verificar_token(token: str = Depends(oauth2_schema), session: Session = Depends(pegar_sessao)):
    try:
        dic_info = jwt.decode(token, SECRET_KEY, ALGORITHM) #decode -> decodificacao do token
        id_usuario = dic_info.get("sub")
    except JWTError:
        raise HTTPException (status_code=401, detail="Acesso negado, verifique a validade do token")
    #verificar se o token é valor
    #extrair o ID do usuario do token
    usuario = session.query(Usuario).filter(Usuario.id == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Acesso invalido")
    return usuario