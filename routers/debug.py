from fastapi import APIRouter, Response, Request, HTTPException, status

from models import *

from common.calendar import get_calendar


router = APIRouter(tags=["debug"])

# here should go wrappers of common functions that should be tested

@router.get("/calendar")
async def calendar():
    return await get_calendar()
