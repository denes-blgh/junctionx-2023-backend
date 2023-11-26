from fastapi import APIRouter, HTTPException, status, Depends, Response

from models import Account, AccountResponse

from typing import Annotated, Optional

from dependencies.auth import require_account, require_staff_token, Token
from common.auth import hash_password, check_email
from common.logger import log

from pydantic import BaseModel

router = APIRouter(tags=["accounts"])


@router.get("")
async def get_accounts(
    staff: Annotated[Token, Depends(require_staff_token)],
):
    accounts = await Account.all()
    return [
        await AccountResponse.create(account)
        for account in accounts
    ]


@router.get("/me")
async def get_me(
    account: Annotated[Account, Depends(require_account)],
):
    return await AccountResponse.create(account)


@router.get("/{id}")
async def get_account(
    id: int,
    staff: Annotated[Token, Depends(require_staff_token)],
):
    account = await Account.get_or_none(id=id)

    if account is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    return await AccountResponse.create(account)


@router.post("/me/change-password")
async def change_password(
    account: Annotated[Account, Depends(require_account)],
    password: str,
):
    account.password = hash_password(password)
    await account.update()
    await log(f"Password changed for account {str(account.id)} ({account.first_name} {account.last_name}).")


@router.post("/me/change-email")
async def change_email(
    account: Annotated[Account, Depends(require_account)],
    email: str,
):
    check_email(email)

    if await Account.get_or_none(email=email.lower()) is not None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Email already used.")

    account.email = email
    await account.update()
    await log(f"Email changed for account {str(account.id)} ({account.first_name} {account.last_name}).")


@router.delete("/me")
async def delete_me(
    account: Annotated[Account, Depends(require_account)]
):
    response = Response()
    response.delete_cookie("token")
    await log(f"Account deleted: {account.id} ({account.first_name} {account.last_name})")
    await account.delete()
    return response


@router.delete("/{id}")
async def delete_account(
    id: int,
    staff: Annotated[Token, Depends(require_staff_token)],
):
    account = await Account.get_or_none(id=id)

    if account is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    await log(f"Account deleted: {account.id} ({account.first_name} {account.last_name})")
    await account.delete()
