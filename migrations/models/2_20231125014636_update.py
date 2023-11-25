from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "appointments" DROP CONSTRAINT "fk_appointm_accounts_f0b3de2b";
        ALTER TABLE "accounts" ADD "last_name" TEXT;
        ALTER TABLE "accounts" ADD "first_name" TEXT;
        ALTER TABLE "appointments" ADD "demand_id" INT NOT NULL UNIQUE;
        ALTER TABLE "appointments" DROP COLUMN "name";
        ALTER TABLE "appointments" DROP COLUMN "patient_id";
        CREATE TABLE IF NOT EXISTS "demands" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "cancer_type" TEXT NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "fractions" INT NOT NULL,
    "patient_id" INT NOT NULL REFERENCES "accounts" ("id") ON DELETE CASCADE
);
        ALTER TABLE "resources" RENAME COLUMN "name" TO "type";
        CREATE UNIQUE INDEX "uid_appointment_resourc_286f64" ON "appointments" ("resource_id", "start");
        CREATE UNIQUE INDEX "uid_appointment_resourc_03aa82" ON "appointments" ("resource_id", "end");
        CREATE UNIQUE INDEX "uid_appointment_demand__aaa160" ON "appointments" ("demand_id");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP INDEX "idx_appointment_demand__aaa160";
        DROP INDEX "uid_appointment_resourc_03aa82";
        DROP INDEX "uid_appointment_resourc_286f64";
        ALTER TABLE "accounts" DROP COLUMN "last_name";
        ALTER TABLE "accounts" DROP COLUMN "first_name";
        ALTER TABLE "resources" RENAME COLUMN "type" TO "name";
        ALTER TABLE "appointments" ADD "name" TEXT NOT NULL;
        ALTER TABLE "appointments" ADD "patient_id" INT NOT NULL;
        ALTER TABLE "appointments" DROP COLUMN "demand_id";
        DROP TABLE IF EXISTS "demands";
        ALTER TABLE "appointments" ADD CONSTRAINT "fk_appointm_accounts_f0b3de2b" FOREIGN KEY ("patient_id") REFERENCES "accounts" ("id") ON DELETE CASCADE;"""
