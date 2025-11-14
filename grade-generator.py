#!/usr/bin/python3
"""
Professional Grade Generator
Subjects fixed, categories & weights automatic.
Teacher inputs only grades (0-100).
Calculations:
 - final weight per subject = (grade * weight) / 100
 - FA total out of 60, SA total out of 40
 - Total score = FA_total + SA_total
 - GPA = Total score / 20 (scale 0-5)
 - Status: PASS if Total >= 50 else FAIL
 - Resubmission: list all subjects where grade < 50 (shown even if overall PASS)
Author: Your Name
"""

import csv

# Fixed subject -> (Category, Weight)
SUBJECTS = {
    "Mathematics": ("FA", 30),
    "English": ("FA", 10),
    "Biology": ("FA", 20),
    "Physics": ("SA", 15),
    "Computer Science": ("SA", 25)
}

PASS_THRESHOLD = 50.0  # total score threshold for pass

def calculate_gpa(total_score):
    """
    GPA as used in your sheet: GPA = total_score / 20
    (Total score max = 100 -> GPA max = 5.0)
    """
    return total_score / 20.0

def input_grade(subject):
    """Prompt teacher for a grade between 0 and 100 for a given subject."""
    while True:
        try:
            raw = input(f"Enter grade for {subject} (0-100): ").strip()
            grade = float(raw)
            if 0 <= grade <= 100:
                return grade
            print("Grade must be between 0 and 100. Try again.")
        except ValueError:
            print("Invalid input. Please enter a number between 0 and 100.")

def format_row(name, cat, grade, weight, final_w):
    return f"| {name:<18} | {cat:^6} | {grade:>6.2f} | {weight:>6} | {final_w:>10.2f} |"

def main():
    print("\nPROFESSIONAL GRADE GENERATOR\n")
    print("Subjects (teacher only inputs grades):")
    for i, subj in enumerate(SUBJECTS.keys(), start=1):
        print(f"  {i}. {subj}")
    print("\nEnter grades for each subject.\n")

    # Collect grades and compute final weight per subject
    records = []
    for subj, (cat, weight) in SUBJECTS.items():
        grade = input_grade(subj)
        final_weight = (grade * weight) / 100.0
        records.append({
            "Subject": subj,
            "Category": cat,
            "Grade": grade,
            "Weight": weight,
            "FinalWeight": final_weight
        })

    # Calculate FA and SA totals
    fa_total = sum(r["FinalWeight"] for r in records if r["Category"] == "FA")
    sa_total = sum(r["FinalWeight"] for r in records if r["Category"] == "SA")
    total_score = fa_total + sa_total
    gpa = calculate_gpa(total_score)
    status = "PASSED" if total_score >= PASS_THRESHOLD else "FAILED"

    # Resubmission list: every subject with grade < 50
    resubjects = [r["Subject"] for r in records if r["Grade"] < 50]

    # Print a professional transcript-style table
    print("\n" + "-"*68)
    print("| Subject             | Cat.   | Grade  | Weight | Final weight |")
    print("-"*68)
    for r in records:
        print(format_row(r["Subject"], r["Category"], r["Grade"], r["Weight"], r["FinalWeight"]))
    print("-"*68)
    print(f"{'Formatives (60)':<48} {fa_total:>10.2f}")
    print(f"{'Summatives (40)':<48} {sa_total:>10.2f}")
    print("-"*68)
    print(f"{'TOTAL':<48} {total_score:>10.2f}")
    print(f"{'GPA (Total/20)':<48} {gpa:>10.4f}")
    print("-"*68)

    # Status and resubmission output (styled plain text)
    print("\nSTATUS:")
    print(f"  Overall result: {status}")
    if resubjects:
        print("  Available for resubmission:")
        for s in resubjects:
            print(f"   - {s}")
    else:
        print("  Available for resubmission: None")

    # Save CSV
    csv_filename = "grades_report.csv"
    with open(csv_filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["Subject", "Category", "Grade", "Weight", "FinalWeight"])
        writer.writeheader()
        writer.writerows(records)
    print(f"\nCSV exported: {csv_filename}\n")

if __name__ == "__main__":
    main()
