from fastapi import APIRouter
from common.sms import send_text_message

router = APIRouter()

@router.get("/sms")
async def sms(number, message):
    return send_text_message(number, message)