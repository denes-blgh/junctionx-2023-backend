from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel

from models import Account, Appointment, Resource
from dependencies.auth import require_token, require_staff_token, require_account, Token

from typing import Annotated, Optional
import datetime


router = APIRouter(tags=["appointments"])


class AppointmentResponse(BaseModel):
    id: int
    name: str
    start: datetime.datetime
    end: datetime.datetime
    resource_id: int
    patient_id: int

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
        appointments = appointments.filter(patient_id=patient_id)
    return [
        AppointmentResponse(
            id=appointment.id,
            name=appointment.name,
            start=appointment.start,
            end=appointment.end,
            resource_id=appointment.resource_id,
            patient_id=appointment.patient_id,
        ) for appointment in appointments
    ]


class AppointmentBody(BaseModel):
    name: str
    start: datetime.datetime
    end: datetime.datetime
    resource_id: int
    patient_id: int

@router.post("")
async def create_appointment(
    body: AppointmentBody,
    token: Annotated[Token, Depends(require_staff_token)],
):
    if body.start > body.end:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Start must be before end")
    
    if await Account.exists(id=body.patient_id) is False:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Patient does not exist")
    
    if await Resource.exists(id=body.resource_id) is False:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Resource does not exist")

    appointment = await Appointment.create(
        name=body.name,
        start=body.start,
        end=body.end,
        resource_id=body.resource_id,
        patient_id=body.patient_id,
    )

    return AppointmentResponse(
        id=appointment.id,
        name=appointment.name,
        start=appointment.start,
        end=appointment.end,
        resource_id=appointment.resource_id,
        patient_id=appointment.patient_id,
    )
