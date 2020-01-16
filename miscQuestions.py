import wolframalpha
from dotenv import load_dotenv
import os

load_dotenv()

wolframalpha_key = os.getenv("WOLF_KEY")
client = wolframalpha.Client(wolframalpha_key)

res = client.query('2 + 2')

print(next(res.results).text)