from pydantic import BaseModel, ConfigDict
from typing import Optional, List

class UsuarioSchema(BaseModel):
    """ Schema para criação e validação de dados de um novo usuário. """
    nome: str
    email: str
    senha: str
    ativo: Optional[bool] = True
    admin: Optional[bool] = False

    model_config = ConfigDict(from_attributes=True)

class ItemPedidoSchema(BaseModel):
    """ Schema para representar a adição, leitura ou formatação de um item dentro de um pedido. """
    produto_id: int
    quantidade: int
    preco_unitario: float

    model_config = ConfigDict(from_attributes=True)

class LoginSchema(BaseModel):
    """ Schema para validação das credenciais de login via corpo da requisição (JSON). """
    email: str
    senha: str

    model_config = ConfigDict(from_attributes=True)

class RespostaPedidoSchema(BaseModel):
    """ Schema para formatar a resposta ao buscar os detalhes completos de um pedido. """
    id: int
    valor: float
    status: str
    itens: List[ItemPedidoSchema]
    
    model_config = ConfigDict(from_attributes=True)