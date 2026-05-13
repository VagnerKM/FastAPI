import os
from sqlalchemy.orm import Session, sessionmaker
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from models import Usuario, db
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "chave_padrao_para_testes")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

# Definindo o schema do OAuth2 aqui evita a importação circular com o main.py
oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/login-form")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db)

def pegar_sessao():
    """ Instancia e fornece uma sessão do banco de dados por requisição. """
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

def verificar_token(token: str = Depends(oauth2_schema), session: Session = Depends(pegar_sessao)):
    """ Verifica a validade do token JWT e retorna o usuário autenticado. """
    try:
        dic_info = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = dic_info.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Token inválido.")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido. Verifique a validade do Token.")

    # Correção: Usando .filter ao invés de .filter_by para expressões lógicas
    usuario = session.query(Usuario).filter(Usuario.id == int(user_id)).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Usuário não encontrado.")
    
    return usuario