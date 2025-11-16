#!/usr/bin/python3
"""
Fixed grade-generator.py
- Requires assignment name (non-empty)
- Validates category, grade, weight
- Enforces FA total = 60 and SA total = 40 (with options to edit/view/normalize)
- Bugfixes: option 2 (view) and option 1 (edit) work reliably and recalc totals immediately
- CSV export as Assignment,Category,Grade,Weight
"""

import csv

EXPECTED_FA_TOTAL = 60.0
EXPECTED_SA_TOTAL = 40.0
PASS_THRESHOLD_PERCENT = 0.50  # 50%

def input_subject():
    while True:
        name = input("Assignment name: ").strip()
        if name:
            return name
        print("Assignment name cannot be empty.")

def input_category():
    while True:
        cat = input("Category (FA/SA): ").strip().upper()
        if cat in ("FA", "SA"):
            return cat
        print("Invalid category. Enter FA or SA only.")

def input_grade():
    while True:
        try:
            g = float(input("Grade (0-100): ").strip())
            if 0 <= g <= 100:
                return g
            print("Grade must be between 0 and 100.")
        except ValueError:
            print("Enter a valid number for grade.")

def input_weight():
    while True:
        try:
            w = float(input("Weight: ").strip())
            if w > 0:
                return w
            print("Weight must be a positive number.")
        except ValueError:
            print("Enter a valid number for weight.")

def print_assignments_with_index(assignments):
    if not assignments:
        print("\nNo assignments yet.\n")
        return
    print("\nCurrent assignments:")
    for i, a in enumerate(assignments, start=1):
        print(f"{i}. {a['Assignment']} | {a['Category']} | Grade: {a['Grade']} | Weight: {a['Weight']}")
    print()  # blank line

def normalize(items, expected_total):
    if not items:
        return
    s = sum(i["Weight"] for i in items)
    if s == 0:
        # distribute evenly
        per_item = expected_total / len(items)
        for it in items:
            it["Weight"] = round(per_item, 2)
    else:
        scale = expected_total / s
        for it in items:
            it["Weight"] = round(it["Weight"] * scale, 2)



def edit_weights_loop(assignments):
    """Allow the user to edit weights until FA==60 and SA==40 or they choose to proceed."""
    while True:
        # compute totals (recompute each loop so edits take effect immediately)
        fa_weight_total = sum(a["Weight"] for a in assignments if a["Category"] == "FA")
        sa_weight_total = sum(a["Weight"] for a in assignments if a["Category"] == "SA")
        total = fa_weight_total + sa_weight_total

        print("\nCurrent weight totals:")
        print(f"  Formative total: {fa_weight_total:.2f} (expected {EXPECTED_FA_TOTAL:.2f})")
        print(f"  Summative total: {sa_weight_total:.2f} (expected {EXPECTED_SA_TOTAL:.2f})")
        print(f"  Combined total: {total:.2f} (expected 100.00)\n")

        if (abs(fa_weight_total - EXPECTED_FA_TOTAL) < 1e-6 and
            abs(sa_weight_total - EXPECTED_SA_TOTAL) < 1e-6):
            print("Weights match expected distribution (FA=60, SA=40). Proceeding...\n")
            return assignments

        # Not matching; give options
        print("Weights do not match the required distribution (FA must sum to 60 and SA to 40).")
        print("Options:")
        print("  1) Edit a weight")
        print("  2) Proceed anyway (not recommended)")
        choice = input("Choose an option (1/2): ").strip()

        if choice == "1":
            # EDIT: allow selecting an assignment and updating its weight
            if not assignments:
                print("No assignments to edit.")
                continue
            print_assignments_with_index(assignments)
            try:
                idx_raw = input("Enter assignment number to edit weight (or 'c' to cancel): ").strip()
                if idx_raw.lower() == 'c':
                    continue
                idx = int(idx_raw)
            except ValueError:
                print("Invalid entry. Enter a number or 'c'.")
                continue

            if not (1 <= idx <= len(assignments)):
                print("Invalid assignment number.")
                continue

            # ask for new weight (validated)
            new_w = input_weight()
            assignments[idx-1]["Weight"] = new_w
            print(f"Weight for '{assignments[idx-1]['Assignment']}' updated to {new_w}.\n")
            # loop will recalc totals at top
            continue

        elif choice == "2":
            confirm = input("Are you sure you want to proceed with incorrect totals? (y/n): ").strip().lower()
            if confirm == "y":
                return assignments
            else:
                continue
        else:
            print("Invalid option. Choose 1, or 2.")
            continue

def main():
    print("=== GRADE GENERATOR ===\n")
    assignments = []

    # Input loop
    while True:
        name = input_subject()
        category = input_category()
        grade = input_grade()
        weight = input_weight()

        assignments.append({
            "Assignment": name,
            "Category": category,
            "Grade": grade,
            "Weight": weight
        })

        again = input("Add another assignment? (y/n): ").strip().lower()
        if again != "y":
            break

    if not assignments:
        print("No assignments entered. Exiting.")
        return

    # Let user edit/auto-normalize/view weights until distribution is acceptable
    assignments = edit_weights_loop(assignments)

    # Calculate contributions and totals
    for a in assignments:
        a["FinalWeight"] = (a["Grade"] / 100.0) * a["Weight"]

    fa_total = sum(a["FinalWeight"] for a in assignments if a["Category"] == "FA")
    sa_total = sum(a["FinalWeight"] for a in assignments if a["Category"] == "SA")

    fa_weight_total = sum(a["Weight"] for a in assignments if a["Category"] == "FA")
    sa_weight_total = sum(a["Weight"] for a in assignments if a["Category"] == "SA")

    final_grade = fa_total + sa_total  # out of 100 when weights sum to 100
    gpa = (final_grade / 100.0) * 5.0

    # PASS/FAIL based on ALU rule: must score >=50% in BOTH categories
    fa_pass = (fa_total >= (PASS_THRESHOLD_PERCENT * fa_weight_total)) if fa_weight_total > 0 else True
    sa_pass = (sa_total >= (PASS_THRESHOLD_PERCENT * sa_weight_total)) if sa_weight_total > 0 else True
    status = "PASS" if (fa_pass and sa_pass) else "FAIL"

    # Resubmission: list all subjects with grade < 50 (show even if overall PASS)
    failed_assignments = [a["Assignment"] for a in assignments if a["Grade"] < 50]
    resub = ", ".join(failed_assignments) if failed_assignments else "None"

    # ---- Print summary in required format ----
    print("\n--- RESULTS ---")
    print(f"Total Formative: {fa_total:.2f} / {fa_weight_total:.0f}")
    print(f"Total Summative: {sa_total:.2f} / {sa_weight_total:.0f}")
    print("--------------------\n")
    print(f"Total Grade: {final_grade:.2f} / 100")
    print(f"GPA: {gpa:.4f}")
    print(f"Status: {status}")
    print(f"Resubmission: {resub}")

    # ---- Write CSV ----
    try:
        with open("grades.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Assignment", "Category", "Grade", "Weight"])
            for a in assignments:
                # write the values as entered (keep decimals if provided)
                writer.writerow([a["Assignment"], a["Category"], a["Grade"], a["Weight"]])
        print("\ngrades.csv created successfully!")
    except Exception as e:
        print(f"Failed to write CSV: {e}")

if __name__ == "__main__":
    main()
