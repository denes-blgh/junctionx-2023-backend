from fastapi import APIRouter

from . import auth, accounts, appointments, resources, debug

router = APIRouter()

router.include_router(auth.router, prefix="/auth")
router.include_router(accounts.router, prefix="/accounts")
router.include_router(appointments.router, prefix="/appointments")
router.include_router(resources.router, prefix="/resources")
router.include_router(debug.router, prefix="/debug")
