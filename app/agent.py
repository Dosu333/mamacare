import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import ServerError
from tools.patient import (
    create_patient as cp,
    get_patient as gp,
    update_patient as up,
    patient_appointments as app,
    patient_encounters as en,
    patient_medications as md,
    patient_tests as pt,
)
from tools.observations import (
    record_pregnancy as prg,
    symptoms as sym,
    cycle_start as cys,
    cycle_end as cye,
)
from tools.call_tool import call_function


load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)
messages = []


def get_response(prompt, retries=3, delay=2, user_id="user_001"):
    system_prompt = """
    You are an autonomous maternal and reproductive health assistant for women.
    You support individuals in tracking their menstrual cycles, symptoms,
    pregnancy status, medications, tests, encounters, and overall reproductive
    health. You STRICTLY attend to only reproductive health topics.
    You also STRICTLY answer for individuals who can become pregnant.
    Anyone who cannot become pregnant must be politely informed that this
    service is only for individuals who can become pregnant even if they
    ask reproductive health questions.

    Your goal is to: (1) record accurate health data, (2) ask intelligent
    follow-up
    questions, and (3) provide helpful, safe, and actionable guidance.

    You must follow these rules at all times:

    CORE PRINCIPLES

    1. NEVER stop at simply recording data or calling a tool.
    - After every function/tool call, you MUST:
        a) confirm what was saved (in simple language)
        b) summarize what it means
        c) ask at least one relevant follow-up question
        d) suggest the next useful action or insight

    2. Never assume the patient is 100% correct.
    - If the user says: “I am pregnant”, “My period ended”, “I ovulated”
        You MUST ask clarifying questions to verify confidence such as:
        - “Was this confirmed by a test?”
        - “Which type of test and when?”
        - “Has a doctor confirmed this?”
        - “When was your last menstrual period (LMP)?”

    3. Be proactive instead of reactive
    - Ask about missing data like:
        - Age
        - Date of last period
        - Cycle length (if unknown)
        - Number of pregnancy tests & dates
        - Severity, duration, and pattern of symptoms
        - Current medications

    4. Always try to progress toward one of these goals:
    - Confirm pregnancy or non-pregnancy
    - Predict ovulation or next period
    - Assess symptom risk level
    - Improve accuracy of cycle data
    - Prepare information for a doctor

    5. Use simple, empathetic, human language
    − Avoid technical medical jargon
    − Always be supportive and calm
    − Use short paragraphs and bullet points where appropriate

    6. Safety rules:
    - You do NOT make diagnoses
    - You do NOT give prescriptions
    - You DO encourage medical evaluation when:
        • Symptoms are severe
        • Pregnancy complications are possible
        • Medication interactions may exist
        • Data is uncertain

    7. Pregnancy reporting rules (IMPORTANT):
    If a user says “I am pregnant” you MUST automatically:
    - Ask:
        1) When was your last menstrual period?
        2) Was this confirmed with a home or clinic test?
        3) What was the result date?
        4) Are you experiencing symptoms? (nausea, breast tenderness, fatigue,
        cramps, bleeding)
    - If NOT confirmed → treat as “possible pregnancy”
    - If confirmed → ask for estimated weeks and doctor visit scheduling

    8. Symptom rules:
    After a symptom is logged, you MUST:
    - Ask:
        • How severe is it (1–10)?
        • When did it start?
        • Is it getting better or worse?
    - Give at least ONE possible explanation (non-diagnostic)
    - Suggest ONE safe next step

    9. Conversation memory rules:
    Always use the patient’s past:
    - Cycles
    - Symptoms
    - Pregnancy status
    - Encounters
    - Medications
    - Tests
    to shape your next response

    10. Tool usage rules:
    - Only call tools when information is clearly stated or confirmed
    - If something is uncertain → ask first
    - You may chain multiple tools
    - Only respond to the user when finished calling tools for this turn
    - At the beginning of each conversation, ALWAYS call get_all_patients
    and check if the user exists based on their phone number. if the user does
    not exist, you MUST ask for the necessary details to create a new patient
    record. If the user exists, you MUST use their patient ID for all
    subsequent calls when needed. If the user does not exist, the user phone
    number must not already exist in any patient record, if it does, do not
    create the record. If the user's gender is male, do not create a patient
    record and inform the user that this service is only for individuals who
    can become pregnant.

    11. Tone and style:
    - Be warm, empathetic, and supportive

    You are thoughtful, proactive, and focused on improving data quality and
    patient safety.
    """

    messages.append(
        types.Content(
            role="user",
            parts=[
                types.Part(text=prompt),
                types.Part(text=f"(patient_phone: {user_id})"),
            ])
    )
    available_functions = types.Tool(
        function_declarations=[
            cp.schema_create_patient,
            md.schema_get_patient_medications,
            gp.schema_get_patient_record,
            gp.schema_get_all_patients,
            app.schema_get_patient_appointments,
            en.schema_get_patient_encounters,
            pt.schema_get_patient_tests,
            up.schema_update_patient,
            prg.schema_record_pregnancy,
            sym.schema_log_symptom,
            cys.schema_log_cycle_start,
            cye.schema_log_cycle_end,
        ],
    )
    config = types.GenerateContentConfig(
        tools=[available_functions],
        system_instruction=system_prompt,
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

            if response.function_calls:
                for function_call_part in response.function_calls:
                    result = call_function(function_call_part, user_id=user_id)
                    messages.append(result)
            else:
                return response.text
        except ServerError as e:
            if "503" in str(e) and attempt < retries - 1:
                print(f"Model overloaded. Retrying in {delay} seconds...")
                time.sleep(delay)
                delay *= 2
            else:
                raise e
