from datetime import UTC, datetime, timedelta

import jwt
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

SECRET_KEY = "actividad-9-secret-key-2026-super-segura"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


def crear_token(username: str) -> str:
    ahora = datetime.now(UTC)
    expiracion = ahora + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    payload = {
        "sub": username,
        "iat": ahora,
        "exp": expiracion,
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/login", response_model=TokenResponse)
def login(datos: LoginRequest) -> TokenResponse:
    if datos.username != "admin" or datos.password != "123456":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
        )

    token = crear_token(datos.username)

    return TokenResponse(
        access_token=token,
        token_type="bearer",
    )
