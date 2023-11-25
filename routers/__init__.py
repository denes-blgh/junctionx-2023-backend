from fastapi import APIRouter

from routers import auth, accounts, resources, appointments, debug, demands, generate, sss

router = APIRouter()

router.include_router(auth.router, prefix="/auth")
router.include_router(accounts.router, prefix="/accounts")
router.include_router(appointments.router, prefix="/appointments")
router.include_router(resources.router, prefix="/resources")
router.include_router(demands.router, prefix="/demands")
router.include_router(debug.router, prefix="/debug")
router.include_router(generate.router, prefix="/generate")
router.include_router(sss.router, prefix="/sss")