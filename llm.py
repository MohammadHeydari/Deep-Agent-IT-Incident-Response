from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(
    base_url=os.getenv("AVVALAI_BASE_URL"),
    api_key=os.getenv("AVVALAI_API_KEY"),
    model=os.getenv("AVVALAI_MODEL"),
    temperature=0,
)