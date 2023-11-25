from fastapi import APIRouter, Response, Request, HTTPException, status

from models import *

from common.calendar import get_calendar

from build.utils import Machine, schedule
from build.utils import Appointment as AppointmentBind
from build.utils import Demand as DemandBind


router = APIRouter(tags=["debug"])

# here should go wrappers of common functions that should be tested

@router.get("/calendar")
async def calendar():
    return await get_calendar()

@router.get("/schedule")
async def make_initial_schedule(
    day_length: int,
    shift_offset: int,
):
    machines = []
    for resource in await Resource.all():
        machines.append(Machine(resource.id, resource.type))

    demands = []
    for demand in await Demand.all():
        cancer = get_cancer_type(demand.cancer_type)
        demands.append(DemandBind(
            demand.id, 
            demand.fractions,
            cancer.avg_duration,
            demand.fractions, 
            cancer.machine_options,
        ))

    print(2)
    result: list[AppointmentBind] = schedule(machines, demands, day_length)
    print(3)

    appointments = []
    now = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    for appointment in result:

        start = now + datetime.timedelta(
            days=appointment.day, 
            minutes=appointment.start + shift_offset,
        )

        end = start + datetime.timedelta(minutes=appointment.duration)

        appointments.append(Appointment(
            demand_id=appointment.demand_id,
            resource_id=appointment.machine_id,
            start=start,
            end=end,
        ))
    
    await Appointment.all().delete()
    await Appointment.bulk_create(appointments)

    return [
        {
            "demand": appointment.demand_id,
            "resource": appointment.resource_id,
            "start": appointment.start,
            "end": appointment.end,
        }
        for appointment in appointments
    ]
