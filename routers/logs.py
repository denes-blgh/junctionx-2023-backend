from fastapi import APIRouter, Depends, Response

from models import *
from dependencies.auth import require_staff_token, Token

from typing import Annotated
import datetime

router = APIRouter(tags=["logs"])

@router.get("")
async def get_logs(
    token: Annotated[Token, Depends(require_staff_token)],
):
    logs = await Log.all()
    return [
        await LogResponse.create(log)
        for log in logs
    ]

@router.delete("")
async def clear_logs(
    token: Annotated[Token, Depends(require_staff_token)],
):
    await Log.all().delete()
    return Response(status_code=status.HTTP_200_OK)