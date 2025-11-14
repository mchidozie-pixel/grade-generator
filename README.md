# Individual Lab – Grade Generator and CSV Organizer

This project contains two components:

1. **Python Grade Generator (grade-generator.py)**
2. **CSV Archiving Script (organizer.sh)**

Both scripts work together to create, evaluate, store, and organize student grade data.

---

## Part 1 – grade-generator.py

This script allows the user to enter multiple assignments and automatically displays:

- A transcript-style table
- Weighted score (grade × weight%)
- Total Formative score (out of 60)
- Total Summative score (out of 40)
- Final Grade (out of 100)
- GPA
- Pass/Fail status
- Required resubmission (if any)
- Saves everything into `grades.csv`

### How to Run
```bash
python3 grade-generator.py
