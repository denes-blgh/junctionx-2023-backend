import dotenv
import os

dotenv.load_dotenv()

try:
    BRANCH = os.environ["BRANCH"]
    PREFIX = f"/junctionx/{BRANCH}/api"
except KeyError:
    BRANCH = None
    PREFIX = "/api"
