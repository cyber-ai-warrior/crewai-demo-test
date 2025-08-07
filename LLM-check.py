import os
from crewai import Agent, Task, Crew, LLM


MODEL="groq/llama3-70b-8192"
GROQ_API_KEY="gsk..."


llm = LLM(model=MODEL,
          temperature=0,
          api_key=GROQ_API_KEY,
          stream=True
          )

response = llama3.call("Give me 5 question related to crewai.")
print(response)
