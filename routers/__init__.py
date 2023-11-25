from fastapi import APIRouter

from routers import auth, accounts, resources, appointments, debug, demands, generate, upcoming, logs, sss, statistics, rooms
router = APIRouter()

router.include_router(auth.router, prefix="/auth")
router.include_router(accounts.router, prefix="/accounts")
router.include_router(appointments.router, prefix="/appointments")
router.include_router(resources.router, prefix="/resources")
router.include_router(demands.router, prefix="/demands")
router.include_router(debug.router, prefix="/debug")
router.include_router(generate.router, prefix="/generate")
router.include_router(sss.router, prefix="/sss")
router.include_router(upcoming.router, prefix="/upcoming")
router.include_router(logs.router, prefix="/logs")
router.include_router(statistics.router, prefix="/statistics")
router.include_router(rooms.router, prefix="/rooms")
