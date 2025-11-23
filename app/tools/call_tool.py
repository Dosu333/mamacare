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
from google.genai import types


def call_function(function_call_part, verbose=True, user_id=None):
    if verbose:
        print(f"""Calling function:
            {function_call_part.name}({function_call_part.args})""")
    else:
        print(f"Calling function: {function_call_part.name}")

    result = ""

    # Patient management
    if function_call_part.name == "create_patient":
        result = cp.create_patient(**function_call_part.args)
    elif function_call_part.name == "get_patient_record":
        result = gp.get_patient_record(**function_call_part.args)
    elif function_call_part.name == "update_patient":
        result = up.update_patient_record(**function_call_part.args)
    elif function_call_part.name == "get_all_patients":
        result = gp.get_all_patients(**function_call_part.args)

    # Appointments & encounters
    elif function_call_part.name == "get_patient_appointments":
        result = app.get_patient_appointments(**function_call_part.args)
    elif function_call_part.name == "get_patient_encounters":
        result = en.get_patient_encounters(**function_call_part.args)

    # Medications & tests
    elif function_call_part.name == "get_patient_medications":
        result = md.get_patient_medications(**function_call_part.args)
    elif function_call_part.name == "get_patient_tests":
        result = pt.get_patient_tests(**function_call_part.args)

    # Observations & cycles
    elif function_call_part.name == "record_pregnancy":
        result = prg.record_pregnancy(**function_call_part.args)
    elif function_call_part.name == "log_symptom":
        result = sym.log_symptom(**function_call_part.args)
    elif function_call_part.name == "log_cycle_start":
        result = cys.log_cycle_start(**function_call_part.args)
    elif function_call_part.name == "log_cycle_end":
        result = cye.log_cycle_end(**function_call_part.args)

    else:
        result = {"status": "failure", "message": "Function not found"}

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response=result
            )
        ]
    )
