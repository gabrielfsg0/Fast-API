#criar as classes dos bancos de dados
from sqlalchemy import create_engine, Column, String, Integer, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship #conectar dois campos distintos sem criar dependencia
from sqlalchemy_utils.types import ChoiceType #permite passar nos status os valores que pode ser utilizado (PENDENTE, CANCELADO, FINALIZADO)


#dentro do create_engine eu posso passar o link do banco de dados quando fizer o deploy do projeto
db = create_engine("sqlite:///banco.db")

#criacao da minha base do banco de dados usando a declarative_base
Base = declarative_base()

#criar as classes/tabelas do banco:
#usuario -> quem faz o pedidos
class Usuario(Base):
    #define a tabela com as informacoes dos usuarios 
    __tablename__ = "usuarios"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String)
    email = Column("email", String, nullable=False)
    senha = Column("senha", String)
    ativo = Column("ativo", Boolean)
    admin = Column ("admin", Boolean, default=False)

    #define o que vai acontecer quando for realizada a criacao de um usuario, utilizando o init para a criacao do objeto usuario
    def __init__(self, nome, email, senha, ativo=True, admin=False):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin
         
#pedidos -> pedido realizado pelo usuario
class Pedido(Base):
    __tablename__ = "pedidos"

    # STATUS_PEDIDOS = (
    #     ("PENDENTE", "PENDENTE"),
    #     ("CANCELADO", "CANCELADO"),
    #     ("FINALIZADO", "FINALIZADO")
    # )

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    status = Column("status", String) #pendente, cancelado, finalizado
    #como meu usuario nesse caso pertence a uma outra tabela, é necessario informar que é uma "chave estrangeira", utilizando o ForeingKey. 
    usuario = Column("usuario", ForeignKey("usuarios.id")) # Assim, chama da tabela usuario a primary_key
    preco = Column("preco", Float)
    itens = relationship("ItemPedido", cascade="all, delete")#criacao da relacao entre as classes, quando deletar um item pedido ele ira cascadear a delecao para a outra classe tb

    def __init__(self, usuario, status="PENDENTE", preco=0):
        self.usuario = usuario
        self.status = status
        self.preco = preco

    def calcular_preco(self):

        #percorrer todos os itens do pedido
        #somar todos os precos de todos os itens do pedido
        #editar no campo preco o valor final do preco do pedido

        self.preco = sum(item.preco_unitario * item.quantidade for item in self.itens)

#itens dos pedidos -> o que vem no pedido, escolhido pelo usuario
class ItemPedido(Base):
    __tablename__ = "itens_pedidos"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    quantidade = Column("quantidade", Integer)
    sabor = Column("sabor", String)
    tamanho = Column("tamanho", String)
    preco_unitario = Column("preco_unitario", Float)
    pedido = Column("pedido", ForeignKey("pedidos.id"))

    def __init__(self, quantidade, sabor, tamanho, preco_unitario, pedido):
        self.quantidade = quantidade
        self.sabor = sabor
        self.tamanho = tamanho
        self.preco_unitario = preco_unitario
        self.pedido = pedido

#executa a criacao dos metadados do seu banco (cria efetivamente o banco de dados)
#------------------------------------------------------------------------------------
# criacao do banco de dados
# 1. instalar o alembic (py -m pip install alembic)
# 2. iniciar o alembic (py -m alembic init alembic)
# 3. geraçao do arquivo .py (py -m alembic revision --autogenerate -m "Initial Migration")
# 4. aplicacao dos dados no banco (py -m alembic upgrade head)
