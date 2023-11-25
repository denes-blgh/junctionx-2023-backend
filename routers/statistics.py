from fastapi import APIRouter, Depends

from models import *
from dependencies.auth import require_staff_token, Token

from typing import Annotated
import datetime

router = APIRouter(tags=["statistics"])

@router.get("")
async def get_statistics(
    # token: Annotated[Token, Depends(require_staff_token)],
):
    appointments = await Appointment.all()
    machine_ids = [x['id'] for x in await Resource.all().values('id')]
    time_per_machine = {id: 0 for id in machine_ids}
    res_cache = {}
    for i, appointment in enumerate(appointments):
        if appointment.start is None or appointment.end is None:
            continue
        res_id = appointment.resource_id
        time_per_machine[res_id] += (appointment.end - appointment.start).total_seconds()

    result = [time_per_machine]
    
    return result
