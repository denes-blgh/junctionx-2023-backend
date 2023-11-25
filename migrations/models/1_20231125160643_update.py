from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "resources" ADD "status" VARCHAR(11) NOT NULL  DEFAULT 'operating';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "resources" DROP COLUMN "status";"""
