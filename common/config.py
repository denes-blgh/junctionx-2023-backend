import dotenv
import os

dotenv.load_dotenv()

try:
    BRANCH = os.environ["BRANCH"]
    PREFIX = f"/junctionx/{BRANCH}"
except KeyError:
    BRANCH = None
    PREFIX = ""
