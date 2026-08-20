# Test Cases

| ID | Scenario | Input | Expected Result |
|---|---|---|---|
| TC01 | Exact profile/course match | Beginner, Python, AI + ML, ML Engineer | Course receives 100 score and is eligible |
| TC02 | Invalid level | `SuperExpert` | `ValueError` is raised |
| TC03 | Duplicate skills | `Python, python, SQL, PYTHON` | Normalized to `python, sql` |
| TC04 | Beginner vs advanced course | Beginner profile, Advanced Deep Learning | Course is not currently eligible |
| TC05 | Missing prerequisites | User has Python only; course also needs ML and Linear Algebra | Missing prerequisites are reported |
| TC06 | Course with no prerequisites | Beginner course with `[]` prerequisites | Full prerequisite readiness points |
| TC07 | Top-N limit | Ask for 1 result from multiple matches | Exactly 1 result returned |
| TC08 | Case-insensitive matching | `PYTHON` vs `Python` | Treated as a match |
| TC09 | Invalid recommendation count | `0` or `11` | Validation error |
| TC10 | Search | Search `machine learning` | Relevant ML courses returned |

Run automated tests with:

```bash
python3 -m unittest discover -s tests -v
```
