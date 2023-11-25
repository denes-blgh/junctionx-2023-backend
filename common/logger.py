from models import Log

def log(message: str):
    log = Log(
        text=message,
    )
    log.save()