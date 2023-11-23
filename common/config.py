import dotenv
import os

dotenv.load_dotenv()

try:
    BRANCH = os.environ["BRANCH"]
    PREFIX = f"/junctionx/{BRANCH}/api"
except KeyError:
    BRANCH = None
    PREFIX = ""

if BRANCH is None:
    GOOGLE_REDIRECT_URI = "http://localhost:7000/v1/auth/google/callback"
else:
    GOOGLE_REDIRECT_URI = f"https://dene.sh/{PREFIX}/v1/auth/google/callback"
