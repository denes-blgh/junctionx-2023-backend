from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "maintenanceevent" ADD "start" TIMESTAMPTZ NOT NULL;
        ALTER TABLE "maintenanceevent" DROP COLUMN "start_hour";
        ALTER TABLE "maintenanceevent" DROP COLUMN "day";
        ALTER TABLE "maintenanceevent" DROP COLUMN "start_minute";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "maintenanceevent" ADD "start_hour" INT NOT NULL;
        ALTER TABLE "maintenanceevent" ADD "day" INT NOT NULL;
        ALTER TABLE "maintenanceevent" ADD "start_minute" INT NOT NULL;
        ALTER TABLE "maintenanceevent" DROP COLUMN "start";"""
