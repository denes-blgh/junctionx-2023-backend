from fastapi import APIRouter

router = APIRouter()

@router.get("/index")
async def index():
    return {"message": "Hello World!"}
