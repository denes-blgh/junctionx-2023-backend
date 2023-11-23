from fastapi import APIRouter, HTTPException, status, Depends

from models import Account

from typing import Annotated, Optional

from dependencies.auth import require_account
from common.auth import hash_password, check_email

from pydantic import BaseModel

router = APIRouter(tags=["accounts"])


class AccountResponse(BaseModel):
    email: Optional[str]
    google_id: Optional[str]
    created_at: int
    updated_at: int
    type: str


@router.get("/me")
async def get_me(
    account: Annotated[Account, Depends(require_account)],
):
    return AccountResponse(
        email=account.email,
        google_id=account.google_id,
        created_at=account.created_at,
        updated_at=account.updated_at,
        type=account.type,
    )


@router.post("/change-password")
async def change_password(
    account: Annotated[Account, Depends(require_account)],
    password: str,
):
    account.password = hash_password(password)
    await account.update()


@router.post("/change-email")
async def change_email(
    account: Annotated[Account, Depends(require_account)],
    email: str,
):
    check_email(email)

    if await Account.get_or_none(email=email.lower()) is not None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Email already used.")

    account.email = email
    await account.update()
