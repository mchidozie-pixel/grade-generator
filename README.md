# Grade Generator

**Description**  
This project automates student grade calculation and transcript generation. It reads student scores, applies weights, calculates totals, assigns grades (A–F), and outputs a formatted transcript. It also supports archiving CSV files with timestamps for record-keeping.

**How It Works**  
1. Input student scores (via CSV or direct input).  
2. Each score is weighted and summed to calculate the total.  
3. Grades are assigned based on thresholds:  
   - A: 90–100  
   - B: 80–89  
   - C: 70–79  
   - D: 60–69  
   - F: <60  
4. A transcript is generated in a clean table format.  
5. (Optional) CSV files can be archived automatically with timestamps using `organizer.sh`.

**Features**  
- Handles multiple students and subjects.  
- Auto-calculates total scores and grades.  
- Generates readable transcript tables.  
- Supports archiving CSV files for version tracking.

**Usage**  
1. Prepare a CSV file with student names, subjects, and scores.  
2. Run the grade generator script:  
```bash
python3 grade_generator.py
