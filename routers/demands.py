from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel

from models import *
from dependencies.auth import require_token, require_staff_token, require_account, Token

from typing import Annotated, Optional
import datetime


router = APIRouter(tags=["demands"])


@router.get("")
async def get_demands(
    token: Annotated[Token, Depends(require_staff_token)],
):
    demands = await Demand.all()
    return [
        await DemandResponse.create(demand)
        for demand in demands
    ]


class DemandBody(BaseModel):
    cancer_type: str
    patient_id: int
    fractions: int
    is_inpatient: bool
    created_at: datetime.datetime = None


@router.post("")
async def create_demand(
    body: DemandBody,
    token: Annotated[Token, Depends(require_account)],
):
    if await Account.exists(id=body.patient_id) is False:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Patient does not exist")

    demand = await Demand.create(
        cancer_type=body.cancer_type,
        patient_id=body.patient_id,
        fractions=body.fractions,
        is_inpatient=body.is_inpatient,
        created_at=body.created_at,
    )
    return await DemandResponse.create(demand)
