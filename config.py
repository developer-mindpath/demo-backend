import os
from dotenv import load_dotenv

load_dotenv()

PRIVATE_KEY = os.getenv("PRIVATE_KEY")
FRONT_END_DOMAIN = os.getenv("FRONT_END_DOMAIN")
BACK_END_DOMAIN = os.getenv("BACK_END_DOMAIN")
