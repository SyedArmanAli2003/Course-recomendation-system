from dataclasses import dataclass, asdict
from typing import List


@dataclass
class Course:
    course_id: str
    title: str
    category: str
    level: str
    interests: List[str]
    prerequisites: List[str]
    skills_taught: List[str]
    career_goals: List[str]
    description: str

    @classmethod
    def from_dict(cls, data: dict) -> "Course":
        return cls(
            course_id=data["course_id"],
            title=data["title"],
            category=data["category"],
            level=data["level"],
            interests=data.get("interests", []),
            prerequisites=data.get("prerequisites", []),
            skills_taught=data.get("skills_taught", []),
            career_goals=data.get("career_goals", []),
            description=data.get("description", ""),
        )


@dataclass
class UserProfile:
    skills: List[str]
    interests: List[str]
    level: str
    goal: str


@dataclass
class Recommendation:
    course: Course
    score: float
    eligible: bool
    reasons: List[str]
    missing_prerequisites: List[str]

    def to_history_dict(self) -> dict:
        return {
            "course_id": self.course.course_id,
            "title": self.course.title,
            "score": round(self.score, 2),
            "eligible": self.eligible,
            "missing_prerequisites": self.missing_prerequisites,
        }
