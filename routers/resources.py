from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel

from models import *
from dependencies.auth import require_token, require_staff_token, require_account, Token
from common.logger import log

from typing import Annotated, Optional


router = APIRouter(tags=["resources"])


@router.get("")
async def get_resources(
    token: Annotated[Token, Depends(require_staff_token)],
):
    resources = await Resource.all()
    return [
        await ResourceResponse.create(resource)
        for resource in resources
    ]


@router.get("/{id}")
async def get_resource(
    id: int,
    token: Annotated[Token, Depends(require_staff_token)],
):
    resource = await Resource.get_or_none(id=id)

    if resource is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    return await ResourceResponse.create(resource)


class ResourceBody(BaseModel):
    type: str

@router.post("")
async def create_resource(
    body: ResourceBody,
    token: Annotated[Token, Depends(require_staff_token)],
):
    resource = await Resource.create(
        type=body.type,
    )
    await log(f"Added resource: {resource.type} with id {resource.id}")
    return await ResourceResponse.create(resource)


@router.delete("/{id}")
async def delete_resource(
    id: int,
    token: Annotated[Token, Depends(require_staff_token)],
):
    resource = await Resource.get_or_none(id=id)

    if resource is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    await resource.delete()
    await log(f"Deleted resource: {resource.type} with id {resource.id}")


class ResourceUpdateBody(BaseModel):
    type: Optional[str]
    status: Optional[ResourceStatus]

@router.patch("/{id}")
async def update_resource(
    id: int,
    body: ResourceUpdateBody,
    token: Annotated[Token, Depends(require_staff_token)],
):
    resource = await Resource.get_or_none(id=id)

    if resource is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    if body.type is not None:
        resource.type = body.type

    await resource.save()
    await log(f"Updated resource: {resource.type} with id {resource.id}")
    return await ResourceResponse.create(resource)
