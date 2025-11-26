from os import getenv
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = getenv("SECRET_KEY")
DB_NAME = getenv("DB_NAME")
DB_USERNAME = getenv("DB_USERNAME")
DB_PASSWORD = getenv("DB_PASSWORD")
DB_HOST = getenv("DB_HOST")
DB_PORT = getenv("DB_PORT", "5432")
BOOTSTRAP_SERVE_LOCAL = getenv("BOOTSTRAP_SERVE_LOCAL")
cloud_name= getenv("CLOUDINARY_CLOUD_NAME")
api_key= getenv("CLOUDINARY_API_KEY")
api_secret= getenv("CLOUDINARY_API_SECRET")