from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta, timezone
from jose import jwt
from models import Usuario
from dependencies import pegar_sessao, verificar_token, SECRET_KEY, ALGORITHM
from schemas import UsuarioSchema, LoginSchema
from passlib.context import CryptContext
import os

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ACESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACESS_TOKEN_EXPIRE_MINUTES", 30))

auth_router = APIRouter(prefix="/auth", tags=["auth"])

def criar_token(user_id: int, duracao_token: timedelta = None):
    """ Gera um token JWT para autenticação. """
    if duracao_token is None:
        duracao_token = timedelta(minutes=ACESS_TOKEN_EXPIRE_MINUTES)
        
    data_expiracao = datetime.now(timezone.utc) + duracao_token
    dic_info = {"sub": str(user_id), "exp": data_expiracao}
    token = jwt.encode(dic_info, SECRET_KEY, algorithm=ALGORITHM)
    return token

def autenticar_usuario(email: str, senha: str, session: Session):
    """ Verifica se as credenciais fornecidas batem com o banco de dados. """
    usuario = session.query(Usuario).filter(Usuario.email == email).first()
    if not usuario:
        return False
    # Valida a senha usando o hash
    if not bcrypt_context.verify(senha, usuario.senha):
        return False
    return usuario

@auth_router.post("/criar_conta")
async def criar_conta(usuario_schema: UsuarioSchema, session: Session = Depends(pegar_sessao)):
    """ Registra um novo usuário no sistema. """
    usuario = session.query(Usuario).filter(Usuario.email == usuario_schema.email).first()
    
    if usuario:
        raise HTTPException(status_code=400, detail=f"Email {usuario_schema.email} já está em uso.")
    
    senha_criptografada = bcrypt_context.hash(usuario_schema.senha)
    novo_usuario = Usuario(
        nome=usuario_schema.nome, 
        email=usuario_schema.email, 
        senha=senha_criptografada, 
        ativo=usuario_schema.ativo, 
        admin=usuario_schema.admin
    )
    
    session.add(novo_usuario)
    session.commit()

    return {f"{usuario_schema.nome.capitalize()}": "Registrado com sucesso!"}


@auth_router.post("/login")
async def login(login_schema: LoginSchema, session: Session = Depends(pegar_sessao)):
    """ Autentica o usuário via JSON e retorna os tokens de acesso e refresh. """
    usuario = autenticar_usuario(login_schema.email, login_schema.senha, session)
    
    if not usuario:
        raise HTTPException(status_code=400, detail="Email ou senha incorretos.")
    
    acess_token = criar_token(usuario.id)
    refresh_token = criar_token(usuario.id, duracao_token=timedelta(days=7))
    
    return {
        "acess_token": acess_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@auth_router.post("/login-form")
async def login_form(dados_formulario: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(pegar_sessao)):
    """ Autentica o usuário via Form Data (padrão do Swagger/OAuth2) e retorna os tokens. """
    usuario = autenticar_usuario(dados_formulario.username, dados_formulario.password, session)
    
    if not usuario:
        raise HTTPException(status_code=400, detail="Email ou senha incorretos.")
    
    acess_token = criar_token(usuario.id)
    refresh_token = criar_token(usuario.id, duracao_token=timedelta(days=7))
    
    return {
        "acess_token": acess_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@auth_router.get("/refresh")
async def use_refresh_token(usuario: Usuario = Depends(verificar_token)):
    """ Gera e retorna um novo access token a partir de uma sessão já autenticada. """
    acess_token = criar_token(usuario.id)
    
    return {
        "acess_token": acess_token,
        "token_type": "bearer"
    }