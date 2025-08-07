import os
from crewai import LLM
from dotenv import load_dotenv

load_dotenv()

MODEL=os.getenv("MODEL")
GROQ_API_KEY=os.getenv("GROQ_API_KEY")

llm = LLM(model=MODEL,
          temperature=0,
          api_key=GROQ_API_KEY,
          stream=True
          )

response = llm.call("Give me 5 question related to crewai.")
print(response)
