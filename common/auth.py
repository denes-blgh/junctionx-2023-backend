from models import Account

from fastapi import HTTPException, status
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta
from pydantic import BaseModel

from typing import Optional, Any
import os
import re


def check_email(email: str):
    if re.match(r"[^@]+@[^@]+\.[^@]+", email) is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid email.")


_pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def verify_password(
    plain: str,
    hashed: str,
) -> str:
    return _pwd_context.verify(plain, hashed)


def hash_password(
    plain: str,
) -> str:
    return _pwd_context.hash(plain)


async def authenticate(
    email: str,
    password: str,
) -> Optional[Account]:
    
    account: Optional[Account] = await Account.get_or_none(email = email)

    if account is None:
        return None

    if not verify_password(password, account.password):
        return None

    return account


def encode_token(
    data: dict[str, Any],
    expire_minutes: int = 60,
) -> str:

    expire = datetime.utcnow() + timedelta(minutes=expire_minutes)

    to_encode: dict = data.copy()
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        claims=to_encode,
        key=os.environ["JWT_SECRET"],
        algorithm="HS256"
    )

    return encoded_jwt


def verify_token(token: str) -> dict[str, Any]:
    try:
        payload = jwt.decode(
            token=token,
            key=os.environ["JWT_SECRET"],
            algorithms="HS256"
        )
        return payload
    except JWTError as e:
        print(e)
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    except KeyError:
        return HTTPException(status.HTTP_400_BAD_REQUEST)


class Token(BaseModel):
    account_id: int
    scopes: list[str]


def create_token(account: Account) -> str:
    scopes = []

    if account.type == "staff":
        scopes.append("staff")

    return encode_token({
        "sub": str(account.id),
        "scopes": " ".join(scopes),
    })
