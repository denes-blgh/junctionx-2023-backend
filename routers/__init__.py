from fastapi import APIRouter

from . import auth, accounts

router = APIRouter()

router.include_router(auth.router, prefix="/auth")
router.include_router(accounts.router, prefix="/accounts")

@router.get("/index")
async def index():
    return {"message": "Hello World!"}
