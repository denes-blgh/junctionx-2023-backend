from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel

from models import *
from dependencies.auth import require_token, require_staff_token, require_account, Token
from common.cancer_types import get_cancer_type
from common.logger import log

from typing import Annotated, Optional
import datetime


router = APIRouter(tags=["maintenances"])

class MaintenanceBody(BaseModel):
    day: int = 10
    start_hour: int = 8
    start_minute: int = 0
    duration: int = 240
    resource_id: int = 2

@router.post("")
async def create_maintenance(
    body: MaintenanceBody,
):
    # TODO: reschedule appointments

    maintenance = await MaintenanceEvent.create(
        day=body.day,
        start_hour=body.start_hour,
        start_minute=body.start_minute,
        duration=body.duration,
        type = EventType.MAINTENANCE,
        resource_id = body.resource_id,
        display_name = "Maintenance",
        color = "#FF0000"
    )
    return await MaintenanceEventResponse.create(maintenance)