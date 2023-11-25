import time
from fastapi import APIRouter, HTTPException, status, Depends, Response

from models import Account, AccountResponse, Demand

from typing import Annotated, Optional

from dependencies.auth import require_account, require_staff_token, Token
from common.auth import hash_password, check_email

from pydantic import BaseModel

from common.cancer_types import CancerType, cancer_types, get_cancer_type

from routers.auth import _register

import random
import json
import random

with open("common/names.json") as f:
    names = json.load(f)

router = APIRouter(tags=["generate"])

@router.get("/")
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
