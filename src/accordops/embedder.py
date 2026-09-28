from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def embed_text(text: str):
    response = client.embeddings.create(input=text, model="text-embedding-3-small")
    return response.data[0].embedding
