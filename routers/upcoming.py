from fastapi import APIRouter, Depends

from models import *
from dependencies.auth import require_staff_token, Token

from typing import Annotated
import datetime

router = APIRouter(tags=["upcoming"])

@router.get("")
async def get_upcoming(
    token: Annotated[Token, Depends(require_staff_token)],
):
    now = datetime.datetime.now() + datetime.timedelta(hours=2)
    appointments = await Appointment.all().filter(start__gte=now).order_by("start").limit(10)
    result = []
    for appointment in appointments:
        result.append(await AppointmentResponse.create(appointment))
    
    return result
