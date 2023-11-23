from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel

from models import Account, Resource
from dependencies.auth import require_token, require_staff_token, require_account, Token

from typing import Annotated, Optional


router = APIRouter(tags=["resources"])


class ResourceResponse(BaseModel):
    id: int
    name: str

@router.get("")
async def get_resources(
    token: Annotated[Token, Depends(require_account)],
):
    resources = await Resource.all()
    return [
        ResourceResponse(
            id=resource.id,
            name=resource.name,
        ) for resource in resources
    ]


class ResourceBody(BaseModel):
    name: str

@router.post("")
async def create_resource(
    body: ResourceBody,
    token: Annotated[Token, Depends(require_staff_token)],
):
    resource = await Resource.create(
        name=body.name,
    )
    return ResourceResponse(
        id=resource.id,
        name=resource.name,
    )


@router.delete("/{id}")
async def delete_resource(
    id: int,
    token: Annotated[Token, Depends(require_staff_token)],
):
    resource = await Resource.get_or_none(id=id)

    if resource is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    await resource.delete()


class ResourceUpdateBody(BaseModel):
    name: Optional[str]

@router.patch("/{id}")
async def update_resource(
    id: int,
    body: ResourceUpdateBody,
    token: Annotated[Token, Depends(require_staff_token)],
):
    resource = await Resource.get_or_none(id=id)

    if resource is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    if body.name is not None:
        resource.name = body.name

    await resource.save()
    return ResourceResponse(
        id=resource.id,
        name=resource.name,
    )
