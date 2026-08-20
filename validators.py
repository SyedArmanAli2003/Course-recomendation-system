VALID_LEVELS = {"beginner", "intermediate", "advanced"}


def normalize_text(value: str) -> str:
    """Normalize text for case-insensitive comparisons."""
    return " ".join(value.strip().lower().split())


def normalize_list(values):
    """
    Normalize, remove blanks, and remove duplicates while preserving order.
    Accepts either a comma-separated string or an iterable of strings.
    """
    if isinstance(values, str):
        values = values.split(",")

    result = []
    seen = set()

    for value in values:
        cleaned = normalize_text(str(value))
        if cleaned and cleaned not in seen:
            seen.add(cleaned)
            result.append(cleaned)

    return result


def validate_level(level: str) -> str:
    cleaned = normalize_text(level)
    if cleaned not in VALID_LEVELS:
        raise ValueError(
            "Invalid level. Choose Beginner, Intermediate, or Advanced."
        )
    return cleaned.title()


def validate_top_n(value) -> int:
    try:
        number = int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError("Number of recommendations must be an integer.") from exc

    if number < 1 or number > 10:
        raise ValueError("Choose between 1 and 10 recommendations.")
    return number


def require_non_empty(value: str, field_name: str) -> str:
    cleaned = value.strip()
    if not cleaned:
        raise ValueError(f"{field_name} cannot be empty.")
    return cleaned
