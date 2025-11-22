import json


def safe_parse_json(text):
    """Try to extract valid JSON from AI response."""
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Try to find the first { ... } block
        import re
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError:
                pass
        # fallback
        return {"intent": "UNSURE", "confidence": 0.0}
