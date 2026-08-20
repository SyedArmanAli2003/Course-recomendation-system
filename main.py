from data_manager import DataManager
from models import UserProfile
from recommendation_engine import RecommendationEngine
from validators import (
    normalize_list,
    require_non_empty,
    validate_level,
    validate_top_n,
)


CAREER_GOALS = [
    "ML Engineer",
    "Data Scientist",
    "Data Analyst",
    "AI Engineer",
    "Python Developer",
    "Backend Developer",
    "Cloud Engineer",
]


def print_header(title):
    print("\n" + "=" * 72)
    print(title.center(72))
    print("=" * 72)


def pause():
    input("\nPress Enter to continue...")


def choose_level():
    mapping = {
        "1": "Beginner",
        "2": "Intermediate",
        "3": "Advanced",
    }

    while True:
        print("\nSelect your current level:")
        print("1. Beginner")
        print("2. Intermediate")
        print("3. Advanced")
        choice = input("Choice: ").strip()

        if choice in mapping:
            return validate_level(mapping[choice])

        print("Invalid choice. Please enter 1, 2, or 3.")


def choose_goal():
    while True:
        print("\nSelect your learning/career goal:")
        for index, goal in enumerate(CAREER_GOALS, start=1):
            print(f"{index}. {goal}")

        choice = input("Choice: ").strip()

        try:
            index = int(choice) - 1
            if 0 <= index < len(CAREER_GOALS):
                return CAREER_GOALS[index]
        except ValueError:
            pass

        print("Invalid choice. Please select a number from the list.")


def create_profile():
    print_header("CREATE YOUR LEARNING PROFILE")

    while True:
        try:
            skills_text = input(
                "Current skills (comma separated, e.g. Python, SQL): "
            )
            skills_text = require_non_empty(skills_text, "Skills")
            skills = normalize_list(skills_text)

            interests_text = input(
                "Interests (comma separated, e.g. AI, Machine Learning): "
            )
            interests_text = require_non_empty(interests_text, "Interests")
            interests = normalize_list(interests_text)

            level = choose_level()
            goal = choose_goal()

            return UserProfile(
                skills=[item.title() for item in skills],
                interests=[item.title() for item in interests],
                level=level,
                goal=goal,
            )
        except ValueError as exc:
            print(f"Input error: {exc}")


def show_recommendation(item, rank):
    print(f"\n#{rank} {item.course.title}")
    print("-" * 72)
    print(f"Course ID : {item.course.course_id}")
    print(f"Category  : {item.course.category}")
    print(f"Level     : {item.course.level}")
    print(f"Match     : {item.score:.2f}%")
    print(f"About     : {item.course.description}")

    print("\nWhy recommended:")
    for reason in item.reasons:
        print(f"  - {reason}")

    print("\nSkills you can learn:")
    for skill in item.course.skills_taught:
        print(f"  - {skill}")


def recommend_courses(engine):
    profile = create_profile()

    while True:
        try:
            top_n = validate_top_n(
                input("\nHow many recommendations do you want? [1-10]: ")
            )
            break
        except ValueError as exc:
            print(f"Input error: {exc}")

    results = engine.recommend(profile, top_n=top_n)

    print_header("YOUR COURSE RECOMMENDATIONS")

    if not results:
        print("No currently eligible courses matched your profile.")
    else:
        for rank, item in enumerate(results, start=1):
            show_recommendation(item, rank)

        DataManager.save_history(profile, results)
        print("\nRecommendation history saved successfully.")

    future = engine.future_options(profile, limit=3)
    if future:
        print_header("FUTURE LEARNING OPTIONS")
        print("These may require a higher level or more prerequisites.")
        for item in future:
            missing = (
                ", ".join(item.missing_prerequisites)
                if item.missing_prerequisites
                else "Higher learning level recommended"
            )
            print(
                f"- {item.course.title} ({item.score:.2f}%) | "
                f"Prepare: {missing}"
            )


def browse_courses(courses):
    print_header("ALL COURSES")
    for course in courses:
        print(
            f"{course.course_id:<5} | "
            f"{course.title:<38} | "
            f"{course.level:<12} | "
            f"{course.category}"
        )


def search_courses(courses):
    query = input("Enter course title/category/skill to search: ").strip().lower()

    if not query:
        print("Search term cannot be empty.")
        return

    results = []
    for course in courses:
        searchable = " ".join(
            [
                course.title,
                course.category,
                course.description,
                *course.skills_taught,
                *course.interests,
            ]
        ).lower()

        if query in searchable:
            results.append(course)

    print_header("SEARCH RESULTS")
    if not results:
        print("No matching courses found.")
        return

    for course in results:
        print(
            f"{course.course_id} | {course.title} | "
            f"{course.level} | {course.category}"
        )


def filter_courses(courses):
    level = choose_level()

    results = [
        course
        for course in courses
        if course.level.lower() == level.lower()
    ]

    print_header(f"{level.upper()} COURSES")
    if not results:
        print("No courses found.")
        return

    for course in results:
        print(
            f"{course.course_id} | {course.title} | {course.category}"
        )


def view_history():
    print_header("RECOMMENDATION HISTORY")

    try:
        history = DataManager.load_history()
    except ValueError as exc:
        print(f"Could not read history: {exc}")
        return

    if not history:
        print("No recommendation history yet.")
        return

    for number, entry in enumerate(history[-5:], start=1):
        profile = entry.get("profile", {})
        print(f"\nSession {number} | {entry.get('timestamp', 'Unknown time')}")
        print(
            f"Level: {profile.get('level')} | "
            f"Goal: {profile.get('goal')}"
        )

        for recommendation in entry.get("recommendations", []):
            print(
                f"  - {recommendation.get('title')} "
                f"({recommendation.get('score')}%)"
            )


def main():
    try:
        courses = DataManager.load_courses()
    except (FileNotFoundError, ValueError) as exc:
        print(f"Startup error: {exc}")
        return

    engine = RecommendationEngine(courses)

    while True:
        print_header("COURSE RECOMMENDATION TOOL")
        print("1. Get Course Recommendations")
        print("2. Browse All Courses")
        print("3. Search Courses")
        print("4. Filter Courses by Level")
        print("5. View Recommendation History")
        print("6. Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            recommend_courses(engine)
            pause()
        elif choice == "2":
            browse_courses(courses)
            pause()
        elif choice == "3":
            search_courses(courses)
            pause()
        elif choice == "4":
            filter_courses(courses)
            pause()
        elif choice == "5":
            view_history()
            pause()
        elif choice == "6":
            print("\nThank you for using the Course Recommendation Tool.")
            break
        else:
            print("Invalid menu choice. Please choose 1-6.")


if __name__ == "__main__":
    main()
