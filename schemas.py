#classes que cria no python usando a estrutura pydantic -> forca a tipagem dos dados
from pydantic import BaseModel #definir modelos de dados
from typing import Optional, List #da para classes parametros opcionais 

class UsurarioSchema(BaseModel):
    nome: str
    email: str
    senha: str
    ativo: Optional[bool]
    admin: Optional[bool] 

    class Config:
        from_atributes = True #faz com que os dados passados acima nao sejam interpretados como um dicionario python mas sim orm (objective relative model) - > classe

class PedidoSchema(BaseModel):
    id_usuario: int

    class Config:
        from_atributes = True 

class LoginSchema(BaseModel):
    email: str
    senha: str

    class Config:
        from_atributes = True 


class ItemPedidoSchema (BaseModel):
    quantidade : int
    sabor : str
    tamanho : str
    preco_unitario : float

    class Config:
        from_atributes = True 


class ResponsePedidoSchema(BaseModel): #forma padrao de resposta
    id: int
    status: str
    preco: float
    itens: List[ItemPedidoSchema]
    
    class Config:
        from_atributes = True 