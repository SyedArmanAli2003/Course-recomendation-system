from typing import List
from models import Course, UserProfile, Recommendation
from validators import normalize_text, normalize_list


class RecommendationEngine:
    INTEREST_WEIGHT = 30.0
    GOAL_WEIGHT = 25.0
    LEVEL_WEIGHT = 20.0
    PREREQUISITE_WEIGHT = 25.0

    LEVEL_VALUES = {
        "beginner": 1,
        "intermediate": 2,
        "advanced": 3,
    }

    def __init__(self, courses: List[Course]):
        self.courses = courses

    def _interest_score(self, course: Course, profile: UserProfile):
        course_interests = set(normalize_list(course.interests))
        user_interests = set(normalize_list(profile.interests))

        if not course_interests:
            return 0.0, []

        matched = course_interests & user_interests
        score = (len(matched) / len(course_interests)) * self.INTEREST_WEIGHT
        return score, sorted(matched)

    def _goal_score(self, course: Course, profile: UserProfile):
        goal = normalize_text(profile.goal)
        course_goals = set(normalize_list(course.career_goals))
        return self.GOAL_WEIGHT if goal in course_goals else 0.0

    def _level_score(self, course: Course, profile: UserProfile):
        user_level = self.LEVEL_VALUES[normalize_text(profile.level)]
        course_level = self.LEVEL_VALUES[normalize_text(course.level)]
        difference = abs(user_level - course_level)

        if difference == 0:
            return self.LEVEL_WEIGHT
        if difference == 1:
            return self.LEVEL_WEIGHT / 2
        return 0.0

    def _prerequisite_details(self, course: Course, profile: UserProfile):
        prerequisites = normalize_list(course.prerequisites)
        user_skills = set(normalize_list(profile.skills))

        if not prerequisites:
            return self.PREREQUISITE_WEIGHT, 1.0, [], []

        satisfied = [p for p in prerequisites if p in user_skills]
        missing = [p for p in prerequisites if p not in user_skills]
        ratio = len(satisfied) / len(prerequisites)
        score = ratio * self.PREREQUISITE_WEIGHT
        return score, ratio, satisfied, missing

    def _is_eligible(self, course: Course, profile: UserProfile, prereq_ratio: float):
        user_level = self.LEVEL_VALUES[normalize_text(profile.level)]
        course_level = self.LEVEL_VALUES[normalize_text(course.level)]

        level_ok = course_level <= user_level + 1
        prerequisites_ok = prereq_ratio >= 0.5
        return level_ok and prerequisites_ok

    def _build_reasons(
        self,
        course: Course,
        profile: UserProfile,
        matched_interests,
        goal_score,
        level_score,
        satisfied_prereqs,
        missing_prereqs,
    ):
        reasons = []

        if matched_interests:
            display = ", ".join(item.title() for item in matched_interests)
            reasons.append(f"Matches your interest(s): {display}")

        if goal_score > 0:
            reasons.append(f"Supports your career goal: {profile.goal}")

        if level_score == self.LEVEL_WEIGHT:
            reasons.append(f"Exact level match: {course.level}")
        elif level_score > 0:
            reasons.append(f"Reasonable level progression: {course.level}")

        if not course.prerequisites:
            reasons.append("No prerequisites required")
        elif not missing_prereqs:
            reasons.append("You satisfy all prerequisites")
        elif satisfied_prereqs:
            reasons.append(
                "You already satisfy: "
                + ", ".join(item.title() for item in satisfied_prereqs)
            )

        if missing_prereqs:
            reasons.append(
                "Missing prerequisite(s): "
                + ", ".join(item.title() for item in missing_prereqs)
            )

        if not reasons:
            reasons.append("General course match based on your profile")

        return reasons

    def score_course(self, course: Course, profile: UserProfile) -> Recommendation:
        interest_score, matched_interests = self._interest_score(course, profile)
        goal_score = self._goal_score(course, profile)
        level_score = self._level_score(course, profile)
        (
            prerequisite_score,
            prereq_ratio,
            satisfied_prereqs,
            missing_prereqs,
        ) = self._prerequisite_details(course, profile)

        total = interest_score + goal_score + level_score + prerequisite_score
        eligible = self._is_eligible(course, profile, prereq_ratio)

        reasons = self._build_reasons(
            course,
            profile,
            matched_interests,
            goal_score,
            level_score,
            satisfied_prereqs,
            missing_prereqs,
        )

        return Recommendation(
            course=course,
            score=round(total, 2),
            eligible=eligible,
            reasons=reasons,
            missing_prerequisites=[item.title() for item in missing_prereqs],
        )

    def recommend(self, profile: UserProfile, top_n: int = 5):
        recommendations = [
            self.score_course(course, profile)
            for course in self.courses
        ]

        eligible = [item for item in recommendations if item.eligible]
        eligible.sort(key=lambda item: (-item.score, item.course.title.lower()))
        return eligible[:top_n]

    def future_options(self, profile: UserProfile, limit: int = 3):
        recommendations = [
            self.score_course(course, profile)
            for course in self.courses
        ]
        future = [item for item in recommendations if not item.eligible]
        future.sort(key=lambda item: (-item.score, item.course.title.lower()))
        return future[:limit]
