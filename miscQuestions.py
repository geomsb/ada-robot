import wolframalpha
from dotenv import load_dotenv
import os

load_dotenv()

def misc_question(user_response):
    wolframalpha_key = os.getenv("WOLF_KEY")
    client = wolframalpha.Client(wolframalpha_key)
    try:
        res = client.query(user_response)
        return next(res.results).text
    except (StopIteration, AttributeError):
        return []
