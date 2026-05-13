import os
from fastapi import FastAPI
from dotenv import load_dotenv

# Carrega as variáveis de ambiente logo na inicialização do app
load_dotenv()

# Importação dos roteadores
from auth_routes import auth_router
from order_routes import order_router

# Inicialização da aplicação com metadados para o Swagger/OpenAPI
app = FastAPI(
    title="API de Gerenciamento de Pedidos",
    description="""
    API RESTful para controle de usuários, autenticação via JWT e gerenciamento de pedidos e itens.
    """,
    version="1.0.0"
)

# Inclusão das rotas definidas nos módulos separados
app.include_router(auth_router)
app.include_router(order_router)

# ==============================================================================
# Para rodar o servidor localmente durante o desenvolvimento, use o comando:
# uvicorn main:app --reload
# ==============================================================================