# my_bot.py
import os
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()

from system_prompt import KARE_SYSTEM_PROMPT

class CustomerSupportBot:
    def __init__(self):
        self.client = AsyncOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPENROUTER_API_KEY")
        )
        self.model = os.getenv("MODEL_NAME", "openai/gpt-4.1-mini")

    async def respond(self, messages):

        constraints = """
        You MUST follow:
        - Replies under 60 words.
        - Calm, warm tone.
        - DO NOT resolve before confirmation.
        - DO NOT jump phases.
        - If greeting/vague → show Smart Menu.
        - If complaint → extract issues → ask for order ID.
        """

        completion = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system",
                 "content": KARE_SYSTEM_PROMPT + "\n\n" + constraints},
                *messages
            ],
            max_tokens=180,
            temperature=0.2,
        )

        return completion.choices[0].message.content
