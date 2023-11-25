from tortoise import fields, models
from fastapi import HTTPException, status

from enum import Enum, StrEnum
import time
import datetime
from typing import Optional

from pydantic import BaseModel

from common.cancer_types import CancerType, get_cancer_type


class AccountType(StrEnum):
    PATIENT = "patient"
    STAFF = "staff"


class Account(models.Model):
    id = fields.IntField(pk=True)
    email = fields.CharField(max_length=254, unique=True, null=True)
    email_verified = fields.BooleanField(default=False)

    password = fields.TextField(null=True)
    google_id = fields.TextField(null=True)

    first_name = fields.TextField(null=True)
    last_name = fields.TextField(null=True)

    created_at = fields.IntField() # unix timestamp
    updated_at = fields.IntField() # unix timestamp

    type = fields.CharEnumField(AccountType, default=AccountType.PATIENT)

    class Meta:
        table = "accounts"

    async def update(self):
        self.updated_at = int(time.time())
        return await self.save()


class AccountResponse(BaseModel):
    id: int
    email: Optional[str]
    google_id: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    created_at: int
    updated_at: int
    type: str

    @classmethod
    async def create(cls, account: Account):
        return cls(
            id=account.id,
            email=account.email,
            google_id=account.google_id,
            first_name=account.first_name,
            last_name=account.last_name,
            created_at=account.created_at,
            updated_at=account.updated_at,
            type=account.type,
        )

class ResourceStatus(StrEnum):
    MAINTENANCE = "maintenance"
    OPERATING = "operating"

class Resource(models.Model):
    id = fields.IntField(pk=True)
    type = fields.TextField() # machine name
    status = fields.CharEnumField(ResourceStatus, default=ResourceStatus.OPERATING) # machine status

    class Meta:
        table = "resources"


class ResourceResponse(BaseModel):
    id: int
    type: str
    status: ResourceStatus
    next_treatement: Optional[datetime.datetime]

    @classmethod
    async def create(cls, resource: Resource):
        now = datetime.datetime.now()
        appointments = await Appointment.all().filter(resource_id=resource.id).filter(start__gte=now).order_by("start")
        next_treatement = appointments[0].start if appointments else None
        return cls(
            id=resource.id,
            type=resource.type,
            status=resource.status,
            next_treatement=next_treatement
        )


class Demand(models.Model):
    id = fields.IntField(pk=True)
    cancer_type = fields.TextField()
    patient = fields.ForeignKeyField("models.Account", related_name="demands")
    created_at = fields.DatetimeField(auto_now_add=True)
    fractions = fields.IntField()
    is_inpatient = fields.BooleanField()

    class Meta:
        table = "demands"


class DemandResponse(BaseModel):
    id: int
    cancer_type: CancerType
    patient: AccountResponse
    created_at: datetime.datetime
    fractions: int
    is_inpatient: bool

    @classmethod
    async def create(cls, demand: Demand):
        return cls(
            id=demand.id,
            cancer_type=get_cancer_type(demand.cancer_type),
            patient=await AccountResponse.create(await demand.patient),
            created_at=demand.created_at,
            fractions=demand.fractions,
            is_inpatient=demand.is_inpatient,
        )


class Appointment(models.Model):
    id = fields.IntField(pk=True)
    demand = fields.ForeignKeyField("models.Demand", related_name="appointment")
    resource = fields.ForeignKeyField("models.Resource", related_name="appointments")
    start = fields.DatetimeField()
    end = fields.DatetimeField()

    async def validate(self):
        # check for overlapping intervals for a single resource
        overlapping_records = await Appointment.filter(
            resource_id=self.resource_id,
            start__lte=self.end,
            end__gte=self.start,
        ).exists()

        if overlapping_records:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                "Resource is already booked for this period"
            )

    class Meta:
        table = "appointments"
        # cannot overlap
        unique_together = (("resource", "start"), ("resource", "end"))


class AppointmentResponse(BaseModel):
    id: Optional[int]
    start: datetime.datetime
    end: datetime.datetime
    demand: DemandResponse
    resource: ResourceResponse

    @classmethod
    async def create(cls, appointment: Appointment):
        return cls(
            id=appointment.id,
            start=appointment.start,
            end=appointment.end,
            demand=await DemandResponse.create(await appointment.demand),
            resource=await ResourceResponse.create(await appointment.resource),
        )
