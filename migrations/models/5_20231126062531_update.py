from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "maintenanceevent" ADD "start_minute" INT NOT NULL;
        ALTER TABLE "maintenanceevent" ADD "display_name" TEXT;
        ALTER TABLE "maintenanceevent" ADD "day" INT NOT NULL;
        ALTER TABLE "maintenanceevent" ADD "duration" INT NOT NULL;
        ALTER TABLE "maintenanceevent" ADD "start_hour" INT NOT NULL;
        ALTER TABLE "maintenanceevent" ADD "color" TEXT;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "maintenanceevent" DROP COLUMN "start_minute";
        ALTER TABLE "maintenanceevent" DROP COLUMN "display_name";
        ALTER TABLE "maintenanceevent" DROP COLUMN "day";
        ALTER TABLE "maintenanceevent" DROP COLUMN "duration";
        ALTER TABLE "maintenanceevent" DROP COLUMN "start_hour";
        ALTER TABLE "maintenanceevent" DROP COLUMN "color";"""
