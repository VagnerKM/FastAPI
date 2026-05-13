from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
#from sqlalchemy_utils.types import ChoiceType

db = create_engine("sqlite:///banco.db")

Base = declarative_base()

class Usuario(Base):
    """ Modelo representando a tabela de usuários no banco de dados. """
    __tablename__ = "usuarios"
    
    id = Column(Integer, autoincrement=True, primary_key=True)
    nome = Column(String)
    email = Column(String, nullable=False, unique=True)
    senha = Column(String)
    ativo = Column(Boolean, default=True)
    admin = Column(Boolean, default=False)

    def __init__(self, nome: str, email: str, senha: str, ativo: bool = True, admin: bool = False):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin

class Pedido(Base):
    """ Modelo representando a tabela de pedidos. """
    __tablename__ = "pedidos"

    # StatusPedido = [
    #     ("PENDENTE", "PENDENTE"),
    #     ("FINALIZADO", "FINALIZADO"),
    #     ("CANCELADO", "CANCELADO")
    # ]

    id = Column(Integer, autoincrement=True, primary_key=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    status = Column(String, default="PENDENTE")
    # status = Column("status", ChoiceType(StatusPedido), default="PENDENTE")
    valor = Column(Float, nullable=False, default=0.0)
    
    # Relacionamento: um pedido tem vários itens
    itens = relationship("ItensPedido", back_populates="pedido", cascade="all, delete")
    usuario = relationship("Usuario")

    def __init__(self, usuario_id: int, valor: float = 0.0, status: str = "PENDENTE"):
        self.usuario_id = usuario_id
        self.status = status
        self.valor = valor

    def calcular_valor_total(self):
        """ Calcula e atualiza o valor total do pedido com base nos itens atrelados a ele. """
        self.valor = sum(item.quantidade * item.preco_unitario for item in self.itens)

class ItensPedido(Base):
    """ Modelo representando os itens individuais dentro de um pedido. """
    __tablename__ = "itens_pedido"
    
    id = Column(Integer, autoincrement=True, primary_key=True)
    produto_id = Column(Integer, ForeignKey("produtos.id"))
    quantidade = Column(Integer)
    preco_unitario = Column(Float, nullable=False)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"))

    # Relacionamento de volta para o pedido
    pedido = relationship("Pedido", back_populates="itens")

    def __init__(self, pedido_id: int, produto_id: int, quantidade: int, preco_unitario: float):
        self.pedido_id = pedido_id
        self.produto_id = produto_id
        self.quantidade = quantidade
        self.preco_unitario = preco_unitario

class Produto(Base):
    """ Modelo representando a tabela de produtos. """
    __tablename__ = "produtos"
    
    id = Column(Integer, autoincrement=True, primary_key=True)
    nome = Column(String)
    descricao = Column(String)
    preco = Column(Float, nullable=False)

    def __init__(self, nome: str, descricao: str, preco: float):
        self.nome = nome
        self.descricao = descricao
        self.preco = preco


# Criar uma migração: alembic revision --autogenerate -m "Mensagem da migração"
# Aplicar a migração: alembic upgrade head