from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "accounts" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "email" VARCHAR(254)  UNIQUE,
    "email_verified" BOOL NOT NULL  DEFAULT False,
    "password" TEXT,
    "google_id" TEXT,
    "created_at" INT NOT NULL,
    "updated_at" INT NOT NULL,
    "type" VARCHAR(7) NOT NULL  DEFAULT 'patient'
);
COMMENT ON COLUMN "accounts"."type" IS 'PATIENT: patient\nSTAFF: staff';
CREATE TABLE IF NOT EXISTS "appointments" (
    "id" SERIAL NOT NULL PRIMARY KEY
);
CREATE TABLE IF NOT EXISTS "machines" (
    "id" SERIAL NOT NULL PRIMARY KEY
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
