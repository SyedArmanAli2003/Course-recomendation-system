# Project Report — Course Recommendation Tool

## 1. Problem Understanding
The problem is to recommend courses according to a learner's interests, existing skills, learning level, prerequisites, and career goal. The expected result is a personalized and ranked shortlist of courses with clear reasons.

A simple keyword search would not be sufficient because a course may match a learner's interest but still be too advanced or require skills the learner does not yet have.

## 2. Proposed Approach
I designed a local Python console application using a transparent weighted rule-based recommendation algorithm.

The learner provides:
- current skills,
- interests,
- current level,
- career goal,
- desired number of recommendations.

The application loads course data from JSON, calculates a score for each course, checks eligibility, sorts eligible courses by score, shows the best matches, and saves recommendation history.

## 3. Implementation
The project is divided into modules:

- `main.py`: user interface and application flow.
- `models.py`: data classes for courses, user profiles, and recommendations.
- `recommendation_engine.py`: scoring, prerequisite checks, eligibility, reasons, and ranking.
- `data_manager.py`: JSON loading and persistence.
- `validators.py`: normalization and input validation.
- `data/courses.json`: local course catalog.
- `tests/`: automated unit tests.

## 4. Important Technical Decisions

### Weighted scoring
The match score is out of 100:

- Interest match: 30
- Career goal: 25
- Level suitability: 20
- Prerequisites: 25

The weighting gives the strongest importance to learner interest and prerequisite readiness while still considering goal and level.

### Partial interest matching
Interest points are proportional to the percentage of course interests matched by the learner.

### Prerequisite readiness
Prerequisite points are proportional to how many prerequisites the learner already satisfies.

### Eligibility rule
A course is considered currently eligible when:
- it is not more than one learning level above the learner, and
- at least 50% of its prerequisites are satisfied.

This prevents unsuitable advanced courses from ranking highly only because the topic and career goal match.

### JSON persistence
JSON was selected because it is zero-cost, human-readable, easy to inspect, and appropriate for a foundational local Python application.

### Case-insensitive normalization
User-entered skills and interests are normalized so values such as `Python`, `python`, and ` PYTHON ` are treated consistently.

## 5. Testing Performed
Automated unit tests verify:
1. a full course/profile match scores 100,
2. a beginner learner is not eligible for an advanced course,
3. missing prerequisites are detected,
4. a course with no prerequisites receives full readiness points,
5. Top-N limits are respected,
6. matching is case-insensitive,
7. duplicate skills are removed,
8. invalid levels are rejected,
9. invalid recommendation counts are rejected.

Manual testing also covers browsing, searching, filtering, recommendation history, and invalid menu choices.

## 6. Challenges Encountered

### Challenge 1: Matching without machine learning
The requirement needs explainable recommendations. A black-box model would make the project unnecessarily difficult to explain.

**Solution:** I used deterministic weighted rules so every score can be justified.

### Challenge 2: Relevant but unsuitable courses
A course may strongly match the learner's goal but be too advanced.

**Solution:** I separated score from eligibility and added level/prerequisite rules.

### Challenge 3: Inconsistent user input
Users may type the same skill with different capitalization or spaces.

**Solution:** Inputs are normalized and duplicates are removed before comparison.

### Challenge 4: Persistence failures
JSON files may be missing or malformed.

**Solution:** File operations include exception handling and clear error messages.

## 7. Future Scope
Future versions can include:
- SQLite persistence,
- a web interface,
- course administration,
- CSV import/export,
- prerequisite graphs,
- learner ratings,
- feedback-based ranking,
- live course-provider integrations.

## 8. Conclusion
The Course Recommendation Tool demonstrates Python fundamentals, modular programming, object-oriented design, lists/dictionaries/sets, input validation, exception handling, JSON file handling, search/filtering/sorting, persistence, and automated testing while remaining explainable and easy to run.
