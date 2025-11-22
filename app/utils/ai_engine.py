import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import ServerError


load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)
messages = []


def classify_intent(message, retries=3, delay=2):
    system_prompt = f"""
                You are a maternal health chatbot assistant. Classify the
                user's message into one of the following intents:
                STATUS, REPORT_SYMPTOM, CYCLE_START, PREGNANCY_ANNOUNCE,
                REQUEST_REPORT, SMALL_TALK, UNSURE.

                Return JSON like this:
                {{"intent": "...", "confidence": 0.0}}
            """

    messages.append(
        types.Content(
            role="user",
            parts=[
                types.Part(text=message)
            ]
        )
    )

    config = types.GenerateContentConfig(
        system_instruction=system_prompt
    )

    for attempt in range(retries):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=messages,
                config=config
            )

            if response.candidates:
                for candidate in response.candidates:
                    if candidate is None or candidate.content is None:
                        continue
                    messages.append(candidate.content)
            return response.text
        except ServerError as e:
            if "503" in str(e) and attempt < retries - 1:
                print(f"Model overloaded. Retrying in {delay} seconds...")
                time.sleep(delay)
                delay *= 2
            else:
                raise e
