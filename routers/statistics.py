from fastapi import APIRouter, Depends

from models import *
from dependencies.auth import require_staff_token, Token

from typing import Annotated
import datetime

router = APIRouter(tags=["statistics"])

@router.get("")
async def get_statistics(
    token: Annotated[Token, Depends(require_staff_token)],
):
    appointments = await Appointment.all()
    machine_ids = [x['id'] for x in await Resource.all().values('id')]
    empty_per_machine = { id: 0 for id in machine_ids }

    time_per_machine = empty_per_machine.copy()
    for appointment in appointments:
        if appointment.start is None or appointment.end is None:
            continue
        res_id = appointment.resource_id
        time_per_machine[res_id] += (appointment.end - appointment.start).total_seconds()

    appointments_per_machine = {}
    for appointment in appointments:
        if appointment.start is None or appointment.end is None:
            continue
        res_id = appointment.resource_id
        if res_id not in appointments_per_machine:
            appointments_per_machine[res_id] = []
        appointments_per_machine[res_id].append(appointment)

    average_patients_per_machine_per_day = empty_per_machine.copy()
    average_break_time_per_machine = empty_per_machine.copy() # In minutes
    patients_counter = empty_per_machine.copy()
    break_time_counter = empty_per_machine.copy()

    for key, value in appointments_per_machine.items():
        prev_appointment = value[0]
        for appointment in value:
            if appointment.start is None or appointment.end is None:
                continue
            average_patients_per_machine_per_day[key] += 1
            if appointment.start.date() != prev_appointment.start.date():
                print("Next day: ", appointment.start.date())
                prev_appointment = appointment
                patients_counter[key] += 1
                continue
            average_break_time_per_machine[key] += (appointment.end - appointment.start).total_seconds()
            break_time_counter[key] += 1
        average_patients_per_machine_per_day[key] /= patients_counter[key]
        average_break_time_per_machine[key] /= break_time_counter[key]
        average_break_time_per_machine[key] /= 60
    
    return [time_per_machine, average_patients_per_machine_per_day, average_break_time_per_machine]
