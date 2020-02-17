import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

DISCORD_WEBHOOK = os.environ.get("DISCORD_WEBHOOK")
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
CONSUMER_KEY = os.environ.get("CONSUMER_KEY")
CONSUMER_SERCRET = os.environ.get("CONSUMER_SERCRET")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
ACCESS_TOKEN_SERCRET = os.environ.get("ACCESS_TOKEN_SERCRET")
