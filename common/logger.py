from models import Log

async def log(message: str):
    log = Log(
        text=message,
    )
    await log.save()