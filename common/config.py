import dotenv
import os

dotenv.load_dotenv()

try:
    BRANCH = os.environ["BRANCH"]
    PREFIX = f"/junctionx/{BRANCH}/api"
except KeyError:
    BRANCH = None
    PREFIX = ""

try:
    GOOGLE_REDIRECT_URI = os.environ["OAUTH2_REDIRECT_URI"]
except:
    if BRANCH is None:
        GOOGLE_REDIRECT_URI = "http://localhost:7000/v1/auth/google/callback"
    else:
        GOOGLE_REDIRECT_URI = f"https://dene.sh/junctionx/{BRANCH}/api/v1/auth/google/callback"
