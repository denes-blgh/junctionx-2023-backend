from fastapi import Request, Depends, HTTPException, status

from common.auth import Token, verify_token
from models import Account

from typing import Annotated


def require_token(request: Request) -> Token:
    plain = request.cookies.get("token")
    payload = verify_token(plain)

    scopes = payload["scopes"].split(" ")

    return Token(
        account_id=payload["sub"],
        scopes=scopes,
    )


def require_staff_token(request: Request) -> Token:
    token = require_token(request)

    if "staff" not in token.scopes:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    return token


async def require_account(
    token: Annotated[Token, Depends(require_token)],
) -> Account:
    
    id = int(token.account_id)
    account = await Account.get_or_none(id=id)

    if account is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    return account


async def require_staff(
    account: Annotated[Account, Depends(require_account)],
):
    if account.type != "staff":
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
