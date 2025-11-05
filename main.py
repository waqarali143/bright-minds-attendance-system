"""
Bright Minds Academy - Classroom Attendance System
Author: Waqar Ali
Filename: attendance_system.py
Description: A simple CLI attendance manager using dictionaries and JSON persistence.
"""

import json
from datetime import datetime
import csv

# ----------------------------------------------------------
# File to store data persistently
# ----------------------------------------------------------
DATA_FILE = "attendance_data.json"

# ----------------------------------------------------------
# Data Structures
# ----------------------------------------------------------
# Preloaded dummy student data
students = {
    "Ali Khan": "Class A",
    "Sara Ahmed": "Class A",
    "Hassan Raza": "Class B",
    "Ayesha Noor": "Class B",
    "Bilal Hussain": "Class C",
    "Fatima Zia": "Class C",
    "Usman Tariq": "Class D",
    "Zainab Iqbal": "Class D",
    "Ahmed Faraz": "Class E",
    "Maryam Ali": "Class E"
}

# Attendance records: { "YYYY-MM-DD": {"Ali Khan": "Present", ...}, ... }
attendance = {}


# ----------------------------------------------------------
# Utility / Validation Functions
# ----------------------------------------------------------
def is_valid_date(date_str):
    """Return True if date_str is in YYYY-MM-DD and is a real date."""
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def prompt_nonempty(prompt_text):
    """Prompt user for input that cannot be empty."""
    while True:
        val = input(prompt_text).strip()
        if val:
            return val
        print("Input cannot be empty. Please try again.")


# ----------------------------------------------------------
# Persistence (Load and Save Data)
# ----------------------------------------------------------
def load_data():
    """Load existing student and attendance data from a JSON file."""
    global students, attendance
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            students.update(data.get("students", {}))
            attendance.update(data.get("attendance", {}))
            print(f"Loaded data: {len(students)} students, {len(attendance)} dates.")
    except FileNotFoundError:
        print("No saved data found — starting with 10 dummy students.")
    except json.JSONDecodeError:
        print("Warning: Data file corrupted. Starting with dummy data.")


def save_data():
    """Save student and attendance data to a JSON file."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump({"students": students, "attendance": attendance}, f, ensure_ascii=False, indent=2)
    print(f"Data saved to {DATA_FILE}.")


# ----------------------------------------------------------
# Core Features
# ----------------------------------------------------------
def add_student():
    """Add a new student to the system."""
    print("\n--- Add New Student ---")
    name = prompt_nonempty("Enter student's full name: ")
    if name in students:
        print("A student with that name already exists.")
        return
    group = prompt_nonempty("Enter class group (e.g., Class A): ")
    students[name] = group
    print(f"Added student: {name} (Group: {group})")


def list_students():
    """Display a list of all students."""
    print("\n--- Student List ---")
    if not students:
        print("No students have been added yet.")
        return
    for i, (name, group) in enumerate(sorted(students.items(), key=lambda x: x[0]), start=1):
        print(f"{i}. {name} — {group}")


def record_attendance():
    """Record attendance for all students for a given date."""
    print("\n--- Record Attendance ---")
    if not students:
        print("No students found. Add students first.")
        return
    date_str = prompt_nonempty("Enter date (YYYY-MM-DD): ")
    if not is_valid_date(date_str):
        print("Invalid date format. Use YYYY-MM-DD.")
        return

    # Create an empty record for the date if not present
    day_record = attendance.setdefault(date_str, {})

    print(f"\nMarking attendance for {date_str}. Enter 'p' for Present, 'a' for Absent, or 's' to skip.\n")
    for name in sorted(students.keys()):
        existing = day_record.get(name)
        prompt = f"{name} [{existing if existing else 'Not recorded'}] (p/a/s): "
        while True:
            choice = input(prompt).strip().lower()
            if choice == "p":
                day_record[name] = "Present"
                break
            elif choice == "a":
                day_record[name] = "Absent"
                break
            elif choice == "s":
                break
            else:
                print("Invalid input. Use 'p' for present, 'a' for absent, 's' to skip.")

    attendance[date_str] = day_record
    print(f"Attendance recorded for {date_str}.")


def view_attendance_by_date():
    """View attendance details for a specific date."""
    print("\n--- View Attendance by Date ---")
    if not attendance:
        print("No attendance records available.")
        return
    date_str = prompt_nonempty("Enter date (YYYY-MM-DD): ")
    if date_str not in attendance:
        print("No records for that date.")
        return

    print(f"\nAttendance for {date_str}:")
    for name in sorted(students.keys()):
        status = attendance[date_str].get(name, "Not recorded")
        print(f"- {name}: {status}")


def search_student_record():
    """Search and display attendance history for a specific student."""
    print("\n--- Search Student Record ---")
    if not students:
        print("No students in the system.")
        return
    name = prompt_nonempty("Enter student's full name: ")
    if name not in students:
        print("Student not found.")
        return

    print(f"\nAttendance history for {name} (Group: {students[name]}):")
    if not attendance:
        print("No attendance recorded yet.")
        return
    for date_str in sorted(attendance.keys()):
        status = attendance[date_str].get(name, "Not recorded")
        print(f"{date_str}: {status}")


def export_attendance_csv():
    """Export attendance for a specific date to a CSV file."""
    date_str = prompt_nonempty("Enter date to export (YYYY-MM-DD): ")
    if date_str not in attendance:
        print("No records for that date.")
        return
    filename = f"attendance_{date_str}.csv"
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Name", "Class Group", "Status"])
        for name in sorted(students.keys()):
            writer.writerow([name, students[name], attendance[date_str].get(name, "Not recorded")])
    print(f"Exported attendance to {filename}.")


# ----------------------------------------------------------
# Menu & Main Function
# ----------------------------------------------------------
def show_menu():
    """Display the main menu."""
    print("\n=== Bright Minds Attendance System ===")
    print("1. Add new student")
    print("2. Record attendance for a date")
    print("3. View attendance by date")
    print("4. Search student attendance record")
    print("5. List students")
    print("6. Export attendance (CSV)")
    print("7. Save & exit")
    print("0. Exit without saving")


def main():
    """Main function to run the CLI-based attendance system."""
    load_data()
    while True:
        show_menu()
        choice = input("Choose an option: ").strip()
        if choice == "1":
            add_student()
        elif choice == "2":
            record_attendance()
        elif choice == "3":
            view_attendance_by_date()
        elif choice == "4":
            search_student_record()
        elif choice == "5":
            list_students()
        elif choice == "6":
            export_attendance_csv()
        elif choice == "7":
            save_data()
            print("Exiting. Goodbye!")
            break
        elif choice == "0":
            print("Exiting without saving. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a valid option.")


# ----------------------------------------------------------
# Entry Point
# ----------------------------------------------------------
if __name__ == "__main__":
    main()
