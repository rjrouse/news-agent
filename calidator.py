from schema import (
    VALID_CATEGORIES,
    VALID_TONES,
    MAX_INSIGHTS,
    MIN_INSIGHTS,
    InsightOutput
)

def validate_insight_output(data: dict) -> tuple[bool, str]:
    """
    Returns:
        (is_valid, error_message)
    """

    # 1. Required top-level fields
    required_fields = [
        "title",
        "summary",
        "insights",
        "category",
        "tone",
        "link"
    ]

    for field in required_fields:
        if field not in data:
            return False, f"Missing field: {field}"

    # 2. Type checks
    if not isinstance(data["insights"], list):
        return False, "insights must be a list"

    # 3. Insight count constraints
    if len(data["insights"]) < MIN_INSIGHTS:
        return False, "Too few insights"

    if len(data["insights"]) > MAX_INSIGHTS:
        return False, "Too many insights"

    # 4. Category validation
    if data["category"] not in VALID_CATEGORIES:
        return False, f"Invalid category: {data['category']}"

    # 5. Tone validation
    if data["tone"] not in VALID_TONES:
        return False, f"Invalid tone: {data['tone']}"

    # 6. Insight-level validation
    for i, insight in enumerate(data["insights"]):

        required_insight_fields = [
            "point",
            "why_it_matters",
            "implication"
        ]

        for field in required_insight_fields:
            if field not in insight:
                return False, f"Missing {field} in insight {i}"

            if not isinstance(insight[field], str):
                return False, f"{field} must be string in insight {i}"

    # 7. Basic sanity checks (important for LLM quality control)
    if len(data["summary"]) < 20:
        return False, "summary too short (likely low-quality output)"

    if len(data["title"]) < 5:
        return False, "title too short"

    return True, "valid"

def validate_or_raise(data: dict) -> InsightOutput:
    is_valid, msg = validate_insight_output(data)

    if not is_valid:
        raise ValueError(f"Insight validation failed: {msg}")

    return data
