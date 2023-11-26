from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel

from models import *
from dependencies.auth import require_token, require_staff_token, require_account, Token
from common.cancer_types import get_cancer_type
from common.logger import log

from typing import Annotated, Optional
import datetime


router = APIRouter(tags=["appointments"])


@router.get("")
async def get_appointments(
    token: Annotated[Token, Depends(require_staff_token)],
    resource_id: Optional[int] = None,
    patient_id: Optional[int] = None,
):
    appointments = await Appointment.all()
    if resource_id is not None:
        appointments = appointments.filter(resource_id=resource_id)
    if patient_id is not None:
        appointments = appointments.filter(demand__patient_id=patient_id)

    result = []
    for appointment in appointments:
        result.append(await AppointmentResponse.create(appointment))

    return result


@router.get("/{id}")
async def get_appointment(
    id: int,
    token: Annotated[Token, Depends(require_staff_token)],
):
    appointment = await Appointment.get_or_none(id=id)

    if appointment is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    return await AppointmentResponse.create(appointment)


class AppointmentBody(BaseModel):
    start: datetime.datetime
    end: datetime.datetime
    resource_id: int
    demand_id: int
    room: Optional[int]

@router.post("")
async def create_appointment(
    body: AppointmentBody,
    token: Annotated[Token, Depends(require_staff_token)],
):
    if body.start > body.end:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Start must be before end")
    
    if await Demand.exists(id=body.demand_id) is False:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Demand does not exist")
    
    if await Resource.exists(id=body.resource_id) is False:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Resource does not exist")

    appointment = Appointment(
        start=body.start,
        end=body.end,
        resource_id=body.resource_id,
        demand_id=body.demand_id,
        room_id=body.room,
    )

    await appointment.validate()
    await appointment.save()
    await log(f"Appointment created: {appointment.id}")

    return await AppointmentResponse.create(appointment)


@router.delete("/{id}")
async def delete_appointment(
    id: int,
    token: Annotated[Token, Depends(require_staff_token)],
):
    appointment = await Appointment.get_or_none(id=id)

    if appointment is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    await appointment.delete()
    await log(f"Appointment deleted: {appointment.id}")


class AppointmentUpdateBody(BaseModel):
    start: Optional[datetime.datetime]
    end: Optional[datetime.datetime]
    resource_id: Optional[int]
    demand_id: Optional[int]
    room_id: Optional[int]


@router.patch("/{id}")
async def update_appointment(
    id: int,
    body: AppointmentUpdateBody,
    token: Annotated[Token, Depends(require_staff_token)],
):
    appointment = await Appointment.get_or_none(id=id)

    if appointment is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    
    if body.start is not None:
        appointment.start = body.start
    if body.end is not None:
        appointment.end = body.end
    if body.resource_id is not None:
        appointment.resource_id = body.resource_id
    if body.demand_id is not None:
        appointment.demand_id = body.demand_id
    if body.room_id is not None:
        appointment.room_id = body.room_id

    #await appointment.validate()
    await appointment.save()
    await log(f"Appointment updated: {appointment.id}")

    return await AppointmentResponse.create(appointment)
