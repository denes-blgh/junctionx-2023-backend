from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "accounts" ADD "gender" VARCHAR(6);
        ALTER TABLE "appointments" ADD "room_id" INT;
        ALTER TABLE "demands" ADD "weight" DOUBLE PRECISION NOT NULL;
        CREATE TABLE IF NOT EXISTS "rooms" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "gender" VARCHAR(6) NOT NULL,
    "capacity" INT NOT NULL  DEFAULT 0
);
COMMENT ON COLUMN "accounts"."gender" IS 'MALE: male\nFEMALE: female';
COMMENT ON COLUMN "rooms"."gender" IS 'MALE: male\nFEMALE: female';
        ALTER TABLE "appointments" ADD CONSTRAINT "fk_appointm_rooms_535d531d" FOREIGN KEY ("room_id") REFERENCES "rooms" ("id") ON DELETE CASCADE;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "appointments" DROP CONSTRAINT "fk_appointm_rooms_535d531d";
        ALTER TABLE "demands" DROP COLUMN "weight";
        ALTER TABLE "accounts" DROP COLUMN "gender";
        ALTER TABLE "appointments" DROP COLUMN "room_id";
        DROP TABLE IF EXISTS "rooms";"""
