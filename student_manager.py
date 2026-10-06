import json
import csv
import os

JSON_FILE = "students.json"
CSV_FILE = "students.csv"


# -------------------------------
# Load students from JSON
# -------------------------------
def load_students():
    if not os.path.exists(JSON_FILE):
        return []

    try:
        with open(JSON_FILE, "r") as file:
            return json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        return []


# -------------------------------
# Save students to JSON
# -------------------------------
def save_students(students):
    with open(JSON_FILE, "w") as file:
        json.dump(students, file, indent=4)


# -------------------------------
# Generate Student ID
# -------------------------------
def generate_student_id(students):
    if not students:
        return "STU001"

    numbers = []

    for student in students:
        try:
            number = int(student["id"][3:])
            numbers.append(number)
        except (ValueError, KeyError):
            pass

    next_number = max(numbers, default=0) + 1

    return f"STU{next_number:03d}"


# -------------------------------
# Calculate Grade
# -------------------------------
def calculate_grade(average):
    if average >= 90:
        return "A+"
    elif average >= 80:
        return "A"
    elif average >= 70:
        return "B"
    elif average >= 60:
        return "C"
    elif average >= 50:
        return "D"
    else:
        return "F"


# -------------------------------
# Get valid marks
# -------------------------------
def get_marks(subject):
    while True:
        try:
            marks = float(input(f"Enter {subject} marks (0-100): "))

            if 0 <= marks <= 100:
                return marks

            print("Please enter marks between 0 and 100.")

        except ValueError:
            print("Please enter a valid number.")


# -------------------------------
# Add Student
# -------------------------------
def add_student(students):

    print("\n========== ADD STUDENT ==========")

    student_id = generate_student_id(students)

    name = input("Enter student name: ").strip()

    while not name:
        print("Name cannot be empty.")
        name = input("Enter student name: ").strip()

    department = input("Enter department: ").strip()
    year = input("Enter year: ").strip()

    python_marks = get_marks("Python")
    maths_marks = get_marks("Maths")
    english_marks = get_marks("English")

    total = python_marks + maths_marks + english_marks
    average = total / 3
    grade = calculate_grade(average)

    student = {
        "id": student_id,
        "name": name,
        "department": department,
        "year": year,
        "python": python_marks,
        "maths": maths_marks,
        "english": english_marks,
        "total": total,
        "average": round(average, 2),
        "grade": grade
    }

    students.append(student)

    save_students(students)

    print("\nStudent added successfully!")
    print("Generated Student ID:", student_id)


# -------------------------------
# Display Students
# -------------------------------
def display_students(students):

    if not students:
        print("\nNo student records found.")
        return

    print("\n================ STUDENT RECORDS ================")

    for student in students:
        print("-----------------------------------------------")
        print("ID         :", student["id"])
        print("Name       :", student["name"])
        print("Department :", student["department"])
        print("Year       :", student["year"])
        print("Python     :", student["python"])
        print("Maths      :", student["maths"])
        print("English    :", student["english"])
        print("Total      :", student["total"])
        print("Average    :", student["average"])
        print("Grade      :", student["grade"])

    print("-----------------------------------------------")


# -------------------------------
# Search Student
# -------------------------------
def search_student(students):

    print("\n========== SEARCH STUDENT ==========")

    search = input("Enter Student ID or Name: ").strip().lower()

    found = False

    for student in students:

        if (
            search == student["id"].lower()
            or search in student["name"].lower()
        ):

            print("\nStudent Found!")
            print("-----------------------------")
            print("ID         :", student["id"])
            print("Name       :", student["name"])
            print("Department :", student["department"])
            print("Year       :", student["year"])
            print("Python     :", student["python"])
            print("Maths      :", student["maths"])
            print("English    :", student["english"])
            print("Total      :", student["total"])
            print("Average    :", student["average"])
            print("Grade      :", student["grade"])

            found = True

    if not found:
        print("No matching student found.")


# -------------------------------
# Update Student
# -------------------------------
def update_student(students):

    print("\n========== UPDATE STUDENT ==========")

    student_id = input("Enter Student ID: ").strip().upper()

    for student in students:

        if student["id"] == student_id:

            print("\nStudent found.")
            print("Press Enter to keep the existing value.")

            new_name = input(
                f"Name [{student['name']}]: "
            ).strip()

            if new_name:
                student["name"] = new_name

            new_department = input(
                f"Department [{student['department']}]: "
            ).strip()

            if new_department:
                student["department"] = new_department

            new_year = input(
                f"Year [{student['year']}]: "
            ).strip()

            if new_year:
                student["year"] = new_year

            print("\nEnter new marks.")

            student["python"] = get_marks("Python")
            student["maths"] = get_marks("Maths")
            student["english"] = get_marks("English")

            student["total"] = (
                student["python"]
                + student["maths"]
                + student["english"]
            )

            student["average"] = round(
                student["total"] / 3, 2
            )

            student["grade"] = calculate_grade(
                student["average"]
            )

            save_students(students)

            print("\nStudent record updated successfully!")

            return

    print("Student ID not found.")


# -------------------------------
# Delete Student
# -------------------------------
def delete_student(students):

    print("\n========== DELETE STUDENT ==========")

    student_id = input("Enter Student ID: ").strip().upper()

    for student in students:

        if student["id"] == student_id:

            print("\nStudent:", student["name"])

            confirmation = input(
                "Are you sure you want to delete? (yes/no): "
            ).lower()

            if confirmation == "yes":

                students.remove(student)

                save_students(students)

                print("Student deleted successfully.")

            else:
                print("Delete operation cancelled.")

            return

    print("Student ID not found.")


# -------------------------------
# Export to CSV
# -------------------------------
def export_to_csv(students):

    if not students:
        print("\nNo records available for export.")
        return

    fields = [
        "id",
        "name",
        "department",
        "year",
        "python",
        "maths",
        "english",
        "total",
        "average",
        "grade"
    ]

    with open(CSV_FILE, "w", newline="") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fields
        )

        writer.writeheader()
        writer.writerows(students)

    print("\nRecords exported successfully!")
    print("CSV file:", CSV_FILE)


# -------------------------------
# Main Menu
# -------------------------------
def main():

    students = load_students()

    while True:

        print("\n")
        print("╔══════════════════════════════════════╗")
        print("║     STUDENT RECORD MANAGEMENT        ║")
        print("╠══════════════════════════════════════╣")
        print("║ 1. Add Student                      ║")
        print("║ 2. View Students                    ║")
        print("║ 3. Search Student                   ║")
        print("║ 4. Update Student                   ║")
        print("║ 5. Delete Student                   ║")
        print("║ 6. Export to CSV                    ║")
        print("║ 7. Exit                             ║")
        print("╚══════════════════════════════════════╝")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_student(students)

        elif choice == "2":
            display_students(students)

        elif choice == "3":
            search_student(students)

        elif choice == "4":
            update_student(students)

        elif choice == "5":
            delete_student(students)

        elif choice == "6":
            export_to_csv(students)

        elif choice == "7":
            print("\nThank you for using Student Record Management System!")
            break

        else:
            print("\nInvalid choice. Please select 1-7.")


# -------------------------------
# Program starts here
# -------------------------------
if __name__ == "__main__":
    main()