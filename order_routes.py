from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from dependencies import pegar_sessao, verificar_token
from schemas import ItemPedidoSchema, RespostaPedidoSchema
from models import Pedido, Usuario, ItensPedido

order_router = APIRouter(prefix="/pedidos", tags=["orders"], dependencies=[Depends(verificar_token)])

@order_router.get("/")
async def get_orders(session: Session = Depends(pegar_sessao)):
    """ Retorna a quantidade total de ordens registradas no sistema. """
    quantidade = session.query(Pedido).count()
    return {"Quantidade de Ordens": quantidade}

@order_router.post("/pedido")
async def criar_pedido(session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    """ Cria um novo pedido em branco associado ao usuário logado. """
    novo_pedido = Pedido(usuario_id=usuario.id)
    session.add(novo_pedido)
    session.commit()
    session.refresh(novo_pedido)
    
    return {
        "mensagem": "Pedido criado com sucesso", 
        "ID do pedido": novo_pedido.id
    }

@order_router.post("/pedido/cancelar/{pedido_id}")
async def cancelar_pedido(pedido_id: int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    """ Cancela um pedido existente. Apenas o dono do pedido ou um admin podem executar. """
    pedido = session.query(Pedido).filter(Pedido.id == pedido_id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    
    if not usuario.admin and pedido.usuario_id != usuario.id:
        raise HTTPException(status_code=401, detail="Você não tem permissão para cancelar este pedido.")
    
    pedido.status = "CANCELADO"
    session.commit()
    
    return {
        "mensagem": f"Pedido n° {pedido.id} cancelado com sucesso",
        "Pedido": pedido
    }

@order_router.get("/pedido/listar")
async def listar_pedidos_admin(session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    """ Retorna todos os pedidos do sistema. (Uso exclusivo de Admin) """
    if not usuario.admin:
        raise HTTPException(status_code=403, detail="Você não tem autorização para fazer essa solicitação.")
    
    pedidos = session.query(Pedido).all()
    return {"Pedidos": pedidos}

@order_router.post("/pedido/adicionar-item/{pedido_id}")
async def adicionar_item(pedido_id: int, item_pedido_schema: ItemPedidoSchema, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    """ Adiciona um item a um pedido existente e recalcula seu valor total. """
    pedido = session.query(Pedido).filter(Pedido.id == pedido_id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    
    if not usuario.admin and pedido.usuario_id != usuario.id:
        raise HTTPException(status_code=401, detail="Você não tem permissão para adicionar itens a este pedido.")
    
    item_pedido = ItensPedido(
        pedido_id=pedido_id, 
        produto_id=item_pedido_schema.produto_id, 
        quantidade=item_pedido_schema.quantidade, 
        preco_unitario=item_pedido_schema.preco_unitario
    )
    
    session.add(item_pedido)
    # Flush garante que o item foi inserido no contexto da transação antes de recalcular o total
    session.flush() 
    
    pedido.calcular_valor_total() 
    session.commit()
    session.refresh(pedido)
    
    return {
        "mensagem": f"Item adicionado ao Pedido n° {pedido.id} com sucesso",
        "Pedido": pedido
    }

@order_router.post("/pedido/remover-item/{id_item_pedido}")
async def remover_item(id_item_pedido: int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    """ Remove um item de um pedido existente e recalcula seu valor total. """
    item_pedido = session.query(ItensPedido).filter(ItensPedido.id == id_item_pedido).first()
    if not item_pedido:
        raise HTTPException(status_code=404, detail="Item do pedido não encontrado")

    pedido = session.query(Pedido).filter(Pedido.id == item_pedido.pedido_id).first()

    if not usuario.admin and usuario.id != pedido.usuario_id:
        raise HTTPException(status_code=401, detail="Você não tem permissão para remover itens a este pedido.")
    
    session.delete(item_pedido)
    session.flush() 
    
    pedido.calcular_valor_total()
    session.commit()
    session.refresh(pedido)
    
    return {
        "mensagem": f"Item removido do Pedido n° {pedido.id} com sucesso",
        "Quantidade de itens restantes": len(pedido.itens),
        "Pedido": pedido
    }

@order_router.post("/pedido/finalizar/{pedido_id}")
async def finalizar_pedido(pedido_id: int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    """ Finaliza um pedido existente. """
    pedido = session.query(Pedido).filter(Pedido.id == pedido_id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    
    if not usuario.admin and pedido.usuario_id != usuario.id:
        raise HTTPException(status_code=401, detail="Você não tem permissão para finalizar este pedido.")
    
    pedido.status = "FINALIZADO"
    session.commit()
    
    return {
        "mensagem": f"Pedido n° {pedido.id} finalizado com sucesso",
        "Pedido": pedido
    }

@order_router.get("/pedido/{pedido_id}")
async def obter_pedido(pedido_id: int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    """ Busca os detalhes de um pedido específico. """
    pedido = session.query(Pedido).filter(Pedido.id == pedido_id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    
    if not usuario.admin and pedido.usuario_id != usuario.id:
        raise HTTPException(status_code=401, detail="Você não tem permissão para acessar este pedido.")
    
    return {
        "mensagem": f"Pedido n° {pedido.id} obtido com sucesso",
        "Pedido": pedido
    }

@order_router.get("/pedido/listar/pedidos-usuario", response_model=list[RespostaPedidoSchema])
async def listar_pedidos_usuario(session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    """ Lista todos os pedidos pertencentes ao usuário autenticado atual. """
    pedidos = session.query(Pedido).filter(Pedido.usuario_id == usuario.id).all()
    return pedidos