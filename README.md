# Course Recommendation Tool

## Project Title
Course Recommendation Tool

## Problem Statement
Learners often have difficulty deciding which course best matches their current skills, interests, learning level, prerequisites, and career goal. This project provides a transparent, rule-based course recommendation system that ranks suitable courses and explains why each course is recommended.

## Objective
Build a functional Python application that:
- accepts a learner profile,
- evaluates a local course catalog,
- checks prerequisites and level suitability,
- calculates an explainable weighted match score,
- ranks suitable courses,
- saves recommendation history.

## Features
- Personalized course recommendations
- Weighted recommendation score out of 100
- Interest matching
- Career-goal matching
- Learning-level compatibility
- Prerequisite readiness checking
- Ranked Top-N recommendations
- Explanation for every recommendation
- Future learning options for currently ineligible courses
- Browse all courses
- Search by title, category, interest, description, or skill
- Filter courses by level
- JSON-based persistence
- Recommendation history
- Input validation and exception handling
- Automated unit tests

## Recommendation Algorithm
The system uses a transparent weighted rule-based algorithm:

| Factor | Weight |
|---|---:|
| Interest match | 30 |
| Career-goal match | 25 |
| Level suitability | 20 |
| Prerequisites satisfied | 25 |
| **Total** | **100** |

### Eligibility Rule
A course is currently eligible when:
1. it is not more than one level above the learner, and
2. the learner satisfies at least 50% of its prerequisites.

This prevents a high topic match from incorrectly ranking a course that the learner is not yet prepared to take.

## Technologies Used
- Python 3
- Standard library only
- JSON for persistence
- `unittest` for automated testing

No paid API, external service, or paid software is required.

## Installation / Setup

### Requirements
- Python 3.9 or newer

No third-party package installation is required.

### Fedora / Linux
```bash
cd course_recommendation_tool
python3 main.py
```

### Windows
```powershell
cd course_recommendation_tool
python main.py
```

## How to Run Tests

Linux:
```bash
python3 -m unittest discover -s tests -v
```

Windows:
```powershell
python -m unittest discover -s tests -v
```

## Project Structure
```text
course_recommendation_tool/
├── main.py
├── models.py
├── recommendation_engine.py
├── data_manager.py
├── validators.py
├── data/
│   ├── courses.json
│   └── recommendation_history.json
├── tests/
│   ├── __init__.py
│   ├── test_recommendation_engine.py
│   └── test_validators.py
├── screenshots/
├── README.md
├── PROJECT_REPORT.md
├── TEST_CASES.md
└── requirements.txt
```

## Testing Details
The test suite covers:
- exact full matches,
- invalid levels,
- duplicate skill normalization,
- invalid Top-N values,
- beginner-to-advanced incompatibility,
- missing prerequisites,
- courses with no prerequisites,
- Top-N limiting,
- case-insensitive matching.

## Limitations
- Uses a manually maintained local course catalog.
- Uses deterministic rule-based matching rather than a machine-learning model.
- Career goals are selected from a predefined list.
- It does not fetch live course data from the internet.

## Future Improvements
- Add a graphical or web interface.
- Store data in SQLite.
- Allow administrators to add/edit/delete courses from the application.
- Add richer skill relationships and prerequisite graphs.
- Import course catalogs from CSV.
- Add learner feedback to improve future rankings.

## Important Design Decision
This is intentionally an explainable rule-based recommendation system. The project requirement asks for ranked recommendations with reasons, so transparency and correctness were prioritized over unnecessary machine-learning complexity.
