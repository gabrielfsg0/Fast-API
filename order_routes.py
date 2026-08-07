#criacao de um roteador
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import pegar_sessao, verificar_token
from schemas import PedidoSchema, ItemPedidoSchema, ResponsePedidoSchema
from model import Pedido, Usuario, ItemPedido
from typing import List


#passar duas variaveis: o caminho e tags
# a criacao de prefixo auxilia em dividir as rotas para nao ter conflito com outras rotas
order_router = APIRouter(prefix = "/pedidos", tags = ["pedidos"], dependencies=[Depends(verificar_token)]) #passando o dependecies no order_router faz com que ela seja aplicada para todas as rotas ao mesmo tempo

#criacao da rota definindo o tipo de requisicao e o caminho a ser seguido
#decorator: linha de codigo que vem antes de uma funcao com @ que atribui uma funcionalidade nova para a funcao que esta sendo criada
#json: formato de resposta
@order_router.get("/")
async def pedidos():
    """
    Essa é a rota padrao de pedidos do nosso sistema. todas as rotas dos pedidos precisam de autenticacao
    """
    return {"mensagem": "voce acessou a rota de pedidos"}

#criando um pedido
@order_router.post("/pedido")
async def criar_pedido(pedido_schema: PedidoSchema, session: Session = Depends(pegar_sessao)): #o Depends informa que o session sera a resposta da funcao pegar_sessao, que entra como parametro
    novo_pedido = Pedido(usuario=pedido_schema.id_usuario)
    session.add(novo_pedido)
    session.commit()
    return {"mensagem": f"Pedido criado com sucesso. ID do pedido: {novo_pedido.id_usuario}"}

#tanto para pedidos quanto para criar pedidos nao precisamos passar a dependencia de criar token pois a unica exigencia é q eles sejam usuários

#nessa proxima rota é necessario ter um nivel de acesso para fazer alteracoes no pedido
@order_router.post("/pedido/cancelar/{id_pedido}") #podemos passar uma coisa na rota que vira como argumento da minha funcao
async def cancelar_pedido(id_pedido: int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)): #depends(vefirificar_token) me passa quem é o usuario
    #usuario.admin = True
    #usuario.id = pedido.usuario

    pedido = session.query(Pedido).filter(pedido.id == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail='Pedido nao encontrado')
    
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail='voce nao tem autorização para fazer essa modificação')
    
    pedido.status = "CANCELADO"
    session.commit()
    return {
        "Mensagem": f"Pedido numero {pedido.id} cancelado com sucesso", #o {pedido.id} foca o programa carregadar as informacoes do pedido
        "pedido": pedido #ao forcar carregar as informacoes do pedido, podemos mostar o dicionario do pedido chamando o pedido como mensagem
        }

@order_router.get("/listar")
async def listar_pedidos(session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    if usuario.admin == False:
        raise HTTPException(status_code=401, detail='Voce nao pode realizar esta operacao')
    else:
        pedidos = session.query(Pedido).all()
        return {
            "pedidos": pedidos
        }

@order_router.post("pedido/adicionar-item/{id_pedido}")
async def adicionar_item_pedido (id_pedido: int, 
                                 item_pedido_schema: ItemPedidoSchema,  
                                 session: Session = Depends(pegar_sessao), 
                                 usuario: Usuario = Depends(verificar_token)):
    
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido)
    if not pedido:
        raise HTTPException(status_code=400, detail='Pedido nao existente')

    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail='Voce nao tem autorizacao para essa operacao')

    #criando um item pedido no meu banco de dados
    item_pedido = ItemPedido(item_pedido_schema.quantidade, 
                             item_pedido_schema.sabor,
                             item_pedido_schema.tamanho, 
                             item_pedido_schema.preco_unitario, 
                             id_pedido)
    session.add(item_pedido)
    pedido.calcular_preco()
    session.commit()
    return {
        "Mensagem": "Item criado com sucesso",
        "Item_id": item_pedido.id,
        "preco_pedido": pedido.preco
    }

@order_router.post("pedido/remover-item/{id_item_pedido}")
async def remover_item_pedido (id_item_pedido: int,
                                 session: Session = Depends(pegar_sessao), 
                                 usuario: Usuario = Depends(verificar_token)):
    
    item_pedido = session.query(Pedido).filter(ItemPedido.id == id_item_pedido)
    pedido = session.query(Pedido).filter(Pedido.id == item_pedido.pedido).first()
    if not item_pedido:
        raise HTTPException(status_code=400, detail='Item nao existente')

    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail='Voce nao tem autorizacao para essa operacao')

    session.delete(item_pedido)
    pedido.calcular_preco()
    session.commit()
    return {
        "Mensagem": "Item removido com sucesso",
        "quantidade_itens_pedido": len(pedido.itens),
        "pedido": pedido
    }

@order_router.post("/pedido/finalizar/{id_pedido}") #podemos passar uma coisa na rota que vira como argumento da minha funcao
async def finalizar_pedido(id_pedido: int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)): #depends(vefirificar_token) me passa quem é o usuario
    #usuario.admin = True
    #usuario.id = pedido.usuario

    pedido = session.query(Pedido).filter(pedido.id == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail='Pedido nao encontrado')
    
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail='voce nao tem autorização para fazer essa modificação')
    
    pedido.status = "FINALIZADO"
    session.commit()
    return {
        "Mensagem": f"Pedido numero {pedido.id} finalizado com sucesso", #o {pedido.id} foca o programa carregadar as informacoes do pedido
        "pedido": pedido #ao forcar carregar as informacoes do pedido, podemos mostar o dicionario do pedido chamando o pedido como mensagem
        }

@order_router.get("/pedido/{id_pedido}")
async def visualizar_pedido(id_pedido: int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(pedido.id == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail='Pedido nao encontrado')
        
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail='voce nao tem autorização para fazer essa modificação')
    return {
        "quantidade_de_itens_do_pedido": len(pedido.itens),
        "pedido": pedido
    }

@order_router.get("/listar/pedidos-usuario", response_model=List[ResponsePedidoSchema])
async def listar_pedidos(session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
  
    pedidos = session.query(Pedido).filter(Pedido.usuario == usuario.id).all()
    return pedidos
