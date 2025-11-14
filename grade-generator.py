#!/usr/bin/python3
"""
Grade Generator Calculator
Transcript-style table view
Author: Your Name
"""

import csv

def calculate_gpa(score):
    if score >= 80:
        return 4.0
    elif score >= 70:
        return 3.5
    elif score >= 60:
        return 3.0
    elif score >= 50:
        return 2.5
    else:
        return 0.0

assignments = []

print("GRADE GENERATOR CALCULATOR")
print("Type 'done' at any time to finish.\n")

while True:
    name = input("Enter assignment name (or 'done'): ").strip()
    if name.lower() == "done":
        break

    # CATEGORY INPUT VALIDATION
    while True:
        category = input("Enter category (FA/SA): ").upper().strip()
        if category in ["FA", "SA"]:
            break
        print("Invalid input! Please enter only 'FA' or 'SA'.")

    # GRADE INPUT VALIDATION
    while True:
        try:
            grade = float(input("Enter grade (0–100): "))
            if 0 <= grade <= 100:
                break
            print("Grade must be between 0 and 100.")
        except ValueError:
            print("Invalid input! Please enter a number.")

    # WEIGHT INPUT VALIDATION
    while True:
        try:
            weight = float(input("Enter weight: "))
            if weight >= 0:
                break
            print("Weight must be a positive number.")
        except ValueError:
            print("Invalid input! Please enter a number.")

    weighted_score = (grade * weight) / 100

    assignments.append({
        "Assignment": name,
        "Category": category,
        "Grade": grade,
        "Weight": weight,
        "Weighted": weighted_score
    })

    # DISPLAY UPDATED TABLE
    print("\nUPDATED TABLE")
    print("-------------------------------------------------------------------")
    print("| Assignment            | Category | Grade | Weight | Weighted %  |")
    print("-------------------------------------------------------------------")
    for a in assignments:
        print(f"| {a['Assignment']:<22} | {a['Category']:^8} | {a['Grade']:^5} | {a['Weight']:^6} | {a['Weighted']:^11.2f} |")
    print("-------------------------------------------------------------------\n")

# ----- FINAL CALCULATIONS -----
fa_total_weight = sum(a["Weight"] for a in assignments if a["Category"] == "FA")
sa_total_weight = sum(a["Weight"] for a in assignments if a["Category"] == "SA")

fa_score = sum(a["Weighted"] for a in assignments if a["Category"] == "FA")
sa_score = sum(a["Weighted"] for a in assignments if a["Category"] == "SA")

fa_percentage = (fa_score / fa_total_weight * 60) if fa_total_weight > 0 else 0
sa_percentage = (sa_score / sa_total_weight * 40) if sa_total_weight > 0 else 0

final_grade = fa_percentage + sa_percentage
gpa = calculate_gpa(final_grade)
status = "PASSED" if final_grade >= 50 else "FAILED"
resub = "None" if status == "PASSED" else "Lowest scoring FA/SA assignment"

print("\nFINAL RESULTS")
print("---------------------------------------------------")
print(f"Formative Total (FA): {fa_percentage:.2f} / 60")
print(f"Summative Total (SA): {sa_percentage:.2f} / 40")
print("---------------------------------------------------")
print(f"Final Grade: {final_grade:.2f} / 100")
print(f"GPA: {gpa:.2f}")
print(f"Status: {status}")
print(f"Resubmission: {resub}")
print("---------------------------------------------------")

# ----- SAVE TO CSV -----
with open("grades.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["Assignment", "Category", "Grade", "Weight", "Weighted"])
    writer.writeheader()
    writer.writerows(assignments)

print("\nCSV saved as grades.csv")
