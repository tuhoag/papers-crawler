from dotenv import load_dotenv
import arcas
import os

api = arcas.Ieee()

key = load_dotenv(".env")

print(os.getenv("IEEE_KEY"))