from fastapi import APIRouter
from common.llm import get_response

router = APIRouter()

@router.get("/index")
async def index():
    return {"message": "Hello World!"}

@router.get("/llm")
async def llm(message: str):
    return get_response([
        {"role": "system", "content": "You're an assistant handling cancer patients' emails.\nLook at the initial email and the patient's response. Decide whether the answer was positive or negative, and if there are any follow-up questions from the patient."},
        {"role": "assistant", "content": "Dear Mr. Smith,\n\nWe are writing to inform you about an opportunity to bring your appointment forward to 2:30pm on Tuesday 10th August 2021.\nPlease let us know if you would like to take up this opportunity.\n\nKind regards,\nDr. Jones"},
        {"role": "user", "content": message}
    ])
