# Professional Grade Generator

## Overview
The **Professional Grade Generator** is a Python script designed to automate student grade calculations and generate a transcript-style report. Teachers only need to input grades (0-100) for a fixed set of subjects. All calculations, pass/fail determination, GPA computation, and resubmission lists are handled automatically.

## Features
- Pre-defined subjects with automatic category (FA/SA) and weight assignment.
- Calculates:
  - **Final weight per subject** = (Grade × Weight) / 100
  - **Formative Assessment (FA) total** out of 60
  - **Summative Assessment (SA) total** out of 40
  - **Total score** (FA + SA)
  - **GPA** on a 0-5 scale (`Total Score / 20`)
- Determines **overall status**:
  - `PASSED` if total ≥ 50  
  - `FAILED` if total < 50
- Lists **subjects eligible for resubmission** (grade < 50), even if the overall result is PASS.
- Generates a **professional transcript-style table** in the console.
- Exports all results to a CSV file (`grades_report.csv`) for record-keeping.

## Usage
1. Run the script:
   ```bash
   python3 grade_generator.py
