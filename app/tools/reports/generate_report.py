from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
from reportlab.lib import colors
from datetime import datetime
from models import Cycle


schema_generate_patient_report = {
    "name": "generate_patient_report",
    "description": "Generate a structured PDF medical report for a patient that can be shared with a doctor",
    "parameters": {
        "type": "object",
        "properties": {
            "patient_id": {
                "type": "integer",
                "description": "The unique ID of the patient"
            }
        },
        "required": ["patient_id"]
    }
}


def generate_patient_report(patient_id: int, ai_insight: str):
    from tools.patient.get_patient import get_patient_record
    from tools.patient.patient_medications import get_patient_medications
    from tools.patient.patient_tests import get_patient_tests
    from tools.observations.symptoms import get_recent_symptoms
    from tools.patient.patient_encounters import get_patient_encounters
    from tools.observations.record_pregnancy import get_pregnancy_status

    patient = get_patient_record(patient_id)

    if not patient:
        return {"status": "error", "message": "Patient not found"}

    cycles = Cycle.query.filter_by(
            patient_id=patient_id
        ).order_by(Cycle.start_date.desc()).all()
    symptoms = get_recent_symptoms(patient_id).get("symptoms", [])
    meds = get_patient_medications(patient_id)
    tests = get_patient_tests(patient_id)
    encounters = get_patient_encounters(patient_id)
    pregnancy = get_pregnancy_status(patient_id)

    filename = f"mamacare_report_{patient_id}.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()

    elements = []

    # ========== HEADER ==========
    elements.append(Paragraph("MAMACARE – REPRODUCTIVE HEALTH REPORT", styles["Title"]))
    elements.append(Spacer(1, 12))

    # ========== PATIENT INFO ==========
    elements.append(Paragraph("Patient Information", styles["Heading2"]))
    elements.append(Paragraph(f"Full Name: {patient['first_name']} {patient['last_name']}", styles["Normal"]))
    elements.append(Paragraph(f"Phone: {patient['phone']}", styles["Normal"]))
    elements.append(Paragraph(f"Generated On: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}", styles["Normal"]))

    # ========== CYCLE HISTORY ==========
    elements.append(Spacer(1, 15))
    elements.append(Paragraph("Recent Cycle History", styles["Heading2"]))

    cycle_data = [["Start Date", "End Date", "Notes"]]
    for c in cycles[:6]:
        cycle_data.append([
            str(c.start_date),
            str(c.end_date) if c.end_date else "—",
            c.notes or ""
        ])

    cycle_table = Table(cycle_data)
    cycle_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.pink),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
    ]))

    elements.append(cycle_table)

    # ========== SYMPTOMS ==========
    if symptoms:
        elements.append(Spacer(1, 15))
        elements.append(Paragraph("Symptoms History", styles["Heading2"]))

        symptom_data = [["Date", "Symptom", "Severity"]]
        for s in symptoms:
            symptom_data.append([
                s["recorded_at"].split("T")[0],
                s["value"],
                s.get("unit", "—")
            ])
        elements.append(Table(symptom_data))

    # ========== PREGNANCY ==========
    if pregnancy.get("pregnancy_status"):
        elements.append(Paragraph(
            f"Status: {pregnancy['pregnancy_status']}",
            styles["Normal"]
        ))
        elements.append(Paragraph(
            f"Recorded at: {pregnancy['recorded_at']}",
            styles["Normal"]
        ))

    # ========== MEDICATIONS ==========
    if meds:
        elements.append(Spacer(1, 15))
        elements.append(Paragraph("Medications", styles["Heading2"]))

        med_data = [["Name", "Dosage", "Start Date"]]
        for m in meds:
            med_data.append([
                m.name,
                m.dosage,
                str(m.start_date)
            ])

        elements.append(Table(med_data))

    # ========== TESTS ==========
    if tests:
        elements.append(Spacer(1, 15))
        elements.append(Paragraph("Medical Tests", styles["Heading2"]))

        test_data = [["Test Name", "Result", "Date"]]
        for t in tests:
            test_data.append([t.name, t.result, str(t.test_date)])

        elements.append(Table(test_data))

    # ========== ENCOUNTERS ==========
    if encounters:
        elements.append(Spacer(1, 15))
        elements.append(Paragraph("Clinical Encounters", styles["Heading2"]))

        enc_data = [["Date", "Reason", "Summary"]]
        for e in encounters:
            enc_data.append([str(e.date), e.reason, e.summary])

        elements.append(Table(enc_data))

    # ========== AI INSIGHT ==========
    elements.append(Spacer(1, 15))
    elements.append(Paragraph("AI Insight (Non-diagnostic)", styles["Heading2"]))
    elements.append(Paragraph(
        ai_insight,
        styles["Italic"]
    ))

    doc.build(elements)

    return {
        "status": "success",
        "file": filename,
        "message": "Patient report successfully generated"
    }
