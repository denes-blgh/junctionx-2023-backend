from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "appointments" ADD "end" TIMESTAMPTZ NOT NULL;
        ALTER TABLE "appointments" ADD "patient_id" INT NOT NULL;
        ALTER TABLE "appointments" ADD "resource_id" INT NOT NULL;
        ALTER TABLE "appointments" ADD "name" TEXT NOT NULL;
        ALTER TABLE "appointments" ADD "start" TIMESTAMPTZ NOT NULL;
        CREATE TABLE IF NOT EXISTS "resources" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" TEXT NOT NULL
);
        DROP TABLE IF EXISTS "machines";
        ALTER TABLE "appointments" ADD CONSTRAINT "fk_appointm_accounts_f0b3de2b" FOREIGN KEY ("patient_id") REFERENCES "accounts" ("id") ON DELETE CASCADE;
        ALTER TABLE "appointments" ADD CONSTRAINT "fk_appointm_resource_ba439e39" FOREIGN KEY ("resource_id") REFERENCES "resources" ("id") ON DELETE CASCADE;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "appointments" DROP CONSTRAINT "fk_appointm_resource_ba439e39";
        ALTER TABLE "appointments" DROP CONSTRAINT "fk_appointm_accounts_f0b3de2b";
        ALTER TABLE "appointments" DROP COLUMN "end";
        ALTER TABLE "appointments" DROP COLUMN "patient_id";
        ALTER TABLE "appointments" DROP COLUMN "resource_id";
        ALTER TABLE "appointments" DROP COLUMN "name";
        ALTER TABLE "appointments" DROP COLUMN "start";
        DROP TABLE IF EXISTS "resources";"""
