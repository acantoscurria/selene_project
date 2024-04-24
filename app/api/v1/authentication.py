import os
from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlmodel import Session, select
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/users/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class TokenResponseSchema(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
    scopes: list[str] = []


def verify_password(plain_password, hashed_password):
    '''Verifica que el password almacenado sea el mismo que el ingresado en login'''
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    '''hashea el password'''
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: float = ACCESS_TOKEN_EXPIRE_MINUTES):
    '''Debe generar el token si se cumple la logica del endpoint "token" '''
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def token_decode(
        token: Annotated[str, Depends(oauth2_scheme)],
        security_scopes: SecurityScopes
):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload is {}:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    token_data = TokenData(scopes=payload.get(
        "scopes", []), username=payload.get("sub"))

    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No tienes suficientes permisos",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return payload
