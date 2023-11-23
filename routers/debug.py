from fastapi import APIRouter, Response, Request, HTTPException, status

from models import *


router = APIRouter(tags=["debug"])

# here should go wrappers of common functions that should be tested

