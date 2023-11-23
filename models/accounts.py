from tortoise import fields, models

from enum import StrEnum
import time


class AccountType(StrEnum):
    PATIENT = "patient"
    STAFF = "staff"


class Account(models.Model):
    id = fields.IntField(pk=True)
    email = fields.CharField(max_length=254, unique=True, null=True)
    email_verified = fields.BooleanField(default=False)

    password = fields.TextField(null=True)
    google_id = fields.TextField(null=True)

    created_at = fields.IntField() # unix timestamp
    updated_at = fields.IntField() # unix timestamp

    type = fields.CharEnumField(AccountType, default=AccountType.PATIENT)

    class Meta:
        table = "accounts"

    async def update(self):
        self.updated_at = int(time.time())
        return await self.save()
