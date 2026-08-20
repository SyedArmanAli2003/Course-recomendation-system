import json
from datetime import datetime
from pathlib import Path
from typing import List
from models import Course, UserProfile, Recommendation


BASE_DIR = Path(__file__).resolve().parent
DEFAULT_COURSES_FILE = BASE_DIR / "data" / "courses.json"
DEFAULT_HISTORY_FILE = BASE_DIR / "data" / "recommendation_history.json"


class DataManager:
    @staticmethod
    def load_courses(path=DEFAULT_COURSES_FILE) -> List[Course]:
        path = Path(path)

        try:
            with path.open("r", encoding="utf-8") as file:
                data = json.load(file)
        except FileNotFoundError as exc:
            raise FileNotFoundError(
                f"Course data file not found: {path}"
            ) from exc
        except json.JSONDecodeError as exc:
            raise ValueError(
                f"Course data contains invalid JSON: {path}"
            ) from exc

        if not isinstance(data, list):
            raise ValueError("courses.json must contain a JSON list.")

        courses = []
        for index, item in enumerate(data, start=1):
            try:
                courses.append(Course.from_dict(item))
            except (KeyError, TypeError) as exc:
                raise ValueError(
                    f"Invalid course record at position {index}."
                ) from exc

        return courses

    @staticmethod
    def load_history(path=DEFAULT_HISTORY_FILE):
        path = Path(path)

        if not path.exists():
            return []

        try:
            with path.open("r", encoding="utf-8") as file:
                data = json.load(file)
        except json.JSONDecodeError as exc:
            raise ValueError("History file contains invalid JSON.") from exc

        return data if isinstance(data, list) else []

    @staticmethod
    def save_history(
        profile: UserProfile,
        recommendations: List[Recommendation],
        path=DEFAULT_HISTORY_FILE,
    ):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        history = DataManager.load_history(path)

        history.append(
            {
                "timestamp": datetime.now().isoformat(timespec="seconds"),
                "profile": {
                    "skills": profile.skills,
                    "interests": profile.interests,
                    "level": profile.level,
                    "goal": profile.goal,
                },
                "recommendations": [
                    item.to_history_dict()
                    for item in recommendations
                ],
            }
        )

        with path.open("w", encoding="utf-8") as file:
            json.dump(history, file, indent=2, ensure_ascii=False)
