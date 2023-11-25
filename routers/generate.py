import time
from fastapi import APIRouter, HTTPException, status, Depends, Response

from models import *

from typing import Annotated, Optional

from dependencies.auth import require_account, require_staff_token, Token
from common.auth import hash_password, check_email

from pydantic import BaseModel

from common.cancer_types import CancerType, cancer_types, get_cancer_type
from common.calendar import get_calendar

from routers.auth import _register

from build.utils import Machine, schedule
from build.utils import Appointment as AppointmentBind
from build.utils import Demand as DemandBind

import random
import json
import random

with open("common/names.json") as f:
    names = json.load(f)

router = APIRouter(tags=["generate"])

@router.get("/patients")
async def generate(number: int, impatient_ratio: float = 0.5):
    for i in range(number):
        # gender with non-equal probabilities
        genders = ["male", "female"]
        gender = random.choice(genders)

        first_name = random.choice(names["first"][gender])
        last_name = random.choice(names["last"])

        # cancer type with non-equal probabilities

        # cancer types: 
        """Craniospinal
            Breast
            Breast special
            Head & neck
            Abdomen
            Pelvis
            Crane
            Lung
            Lung special
            Whole Brain"""
        
        probabilities = [0.01, 0.25, 0.05, .1, .1, .18, .04, .12, .05, .1]
        cancer_type_region = random.choices(cancer_types, probabilities)[0]

        #cancer_type = get_cancer_type(cancer_type_region)

        fractions = random.choice(cancer_type_region.fraction_options)

        is_impatient = random.random() < impatient_ratio

        print("new patient: " + first_name + " " + last_name + " " + gender + " " + cancer_type_region.region, " ", fractions)

        # create account
        account = await _register(
            email=None,
            password=None,
            first_name=first_name,
            last_name=last_name
        )

        # create demand
        demand = await Demand.create(
            cancer_type=cancer_type_region.region,
            patient_id=account.id,
            fractions=fractions,
            is_inpatient=is_impatient,
            created_at=int(time.time()),
        )

    # create response
    return "jippiajee"


@router.post("/schedule")
async def initialize_schedule(
    day_length: int,
    shift_offset: int,
    reserve_ratio: float,
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

    result: list[AppointmentBind] = schedule(
        machines, 
        demands, 
        day_length, 
        reserve_ratio
    )

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
