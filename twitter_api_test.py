import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Read values
api_key = os.getenv("API_KEY")
api_key_secret = os.getenv("API_KEY_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")
bearer_token = os.getenv("BEARER_TOKEN")

print("API Key:", api_key[:5] + "*****")   # print only part for security
print("Bearer Token loaded:", bool(bearer_token))
