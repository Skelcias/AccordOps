from openai import OpenAI
from accordops.schemas import TicketExpenseLLM
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# response = client.responses.create(
#     model="gpt-5.6-luna",
#     instructions="Assigne 'merchant', 'date', 'amount', 'category' si tu les detectent dans le texte en input",
#     input="Respecte le format de sortie imposé, extrait si seulement l'information existe dans le texte fournit",
# )

# print(response.output_text)


def extract_receipt(text: str):
    response = client.responses.parse(
        model="gpt-5.6-luna",
        input=[
            {
                "role": "system",
                "content": "Extract the receipt information. "
                "Do not invent missing information. "
                "Use null when information is unavailable.",
            },
            {"role": "user", "content": text},
        ],
        text_format=TicketExpenseLLM,
    )
    return response.output_parsed


text = """
Restaurant Chez Marcel
22/09/2026
Total : 42.50 EUR
"""

print(extract_receipt(text))
