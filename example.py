from wordware import Wordware
from pathlib import Path


api_key = Path("api.txt").read_text()

print(api_key)

person = Wordware(prompt_id="b2f176c9-baa7-4db3-ac56-d6f641a05c53", api_key=api_key)