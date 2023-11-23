from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from tortoise.contrib.fastapi import register_tortoise

import dotenv
import os

from routers import router

app = FastAPI(
    default_response_class=ORJSONResponse,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(router, prefix="/v1")

dotenv.load_dotenv()

db_config: dict = {
    'connections': {
        # Dict format for connection
        'default': {
            'engine': 'tortoise.backends.asyncpg',
            'credentials': {
                'host': os.environ["DB_HOST"],
                'port': os.environ["DB_PORT"],
                'user': os.environ["DB_USER"],
                'password': os.environ["DB_PASSWORD"],
                'database': os.environ["DB_DATABASE"],
            },
        },
    },
    'apps': {
        'models': {
            'models': ['models'],
            # If no default_connection specified, defaults to 'default'
            'default_connection': 'default',
        }
    }
}

register_tortoise(
    app=app,
    config=db_config,
    generate_schemas=True
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7000)
