from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel

from models import *
from dependencies.auth import require_token, require_staff_token, require_account, Token
from common.cancer_types import get_cancer_type
from common.logger import log

from typing import Annotated, Optional
import datetime


router = APIRouter(tags=["rooms"])

@router.get("")
async def get_rooms():
    rooms = await Room.all()

    result = []
    for room in rooms:
        result.append(await RoomResponse.create(room))

    return result

@router.put("/{id}")
async def update_room(
    gender: Gender,
    bed_count: int,
):
    room = await Room.get(gender=gender)

    print(room.gender, bed_count)

    if room is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    room.capacity = bed_count
    await room.save()

    return await RoomResponse.create(room)