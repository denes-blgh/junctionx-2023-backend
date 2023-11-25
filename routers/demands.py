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


@router.get("/{demand_id}")
async def get_demand(
    demand_id: int,
    token: Annotated[Token, Depends(require_staff_token)],
):
    demand = await Demand.get_or_none(id=demand_id)
    if demand is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Demand does not exist")
    return await DemandResponse.create(demand)


@router.post("")
async def create_demand(
    body: DemandBody,
    token: Annotated[Token, Depends(require_token)],
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


@router.delete("/{demand_id}")
async def delete_demand(
    demand_id: int,
    token: Annotated[Token, Depends(require_staff_token)],
):
    demand = await Demand.get_or_none(id=demand_id)
    if demand is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Demand does not exist")
    await demand.delete()
    return await DemandResponse.create(demand)


class DemandUpdateBody(BaseModel):
    cancer_type: Optional[str]
    patient_id: Optional[int]
    fractions: Optional[int]
    is_inpatient: Optional[bool]


@router.patch("/{demand_id}")
async def update_demand(
    demand_id: int,
    body: DemandUpdateBody,
    token: Annotated[Token, Depends(require_staff_token)],
):
    demand = await Demand.get_or_none(id=demand_id)
    if demand is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Demand does not exist")

    if body.cancer_type is not None:
        demand.cancer_type = body.cancer_type
    if body.patient_id is not None:
        demand.patient_id = body.patient_id
    if body.fractions is not None:
        demand.fractions = body.fractions
    if body.is_inpatient is not None:
        demand.is_inpatient = body.is_inpatient

    await demand.save()
    return await DemandResponse.create(demand)
