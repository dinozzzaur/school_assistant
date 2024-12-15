import re
import datetime
from tabulate import tabulate

# Regular expression for email validation
email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

# Data  to store users, schedules, homework, and grades
user_db = [] 
student_db = [] 
homework_db = []  
grade_db = [] 
reminder_db = []  

# Function to get the user's role
def get_role():
    print("Select your role:")
    print("1. Student")
    print("2. Teacher")
    print("3. Parent")
    while True:
        role = input("Please enter your choice: (1, 2 or 3): ")
        if role in ["1", "2", "3"]:
            return int(role)
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

# Function to manage login or sign up
def get_choice():
    print("1. Log in")
    print("2. Sign up")
    print("3. Exit")
    while True:
        choice = input("Please enter your choice: (1, 2 or 3): ")
        if choice == "1":
            return 1
        elif choice == "2":
            return 2
        elif choice == "3":
            print("Exiting...")
            exit()  # Exit the program
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

# Function for login
def login():
    email = input("Enter your email: ")
    password = input("Enter your password: ")

    if not re.match(email_pattern, email):
        print("Invalid email format!")
        return None
    
    # Check for matching email and password in user_db
    for user in user_db:
        if user['email'] == email and user['password'] == password:
            print(f"Login successful for {email}")
            return user  # Return the user object if login is successful
    print("Invalid credentials. Please try again.")
    return None

# Function for signup
def signup():
    name = input("Enter your name: ")
    surname = input("Enter your surname: ")
    email = input("Enter your email: ")
    password = input("Enter your password: ")

    # Validate email format
    if not re.match(email_pattern, email):
        print("Invalid email format!")
        return None

    # Check if the email already exists in the mock database
    for user in user_db:
        if user['email'] == email:
            print(f"Email {email} is already registered. Please log in.")
            return None

    # Store user data in the "database"
    role = get_role()  # Determine user role (1 = Student, 2 = Teacher, 3 = Parent)
    new_user = {
        'name': name,
        'surname': surname,
        'email': email,
        'password': password,
        'role': role
    }
    user_db.append(new_user)

    if role == 1:  # Student
        student_db.append(new_user)  # Add student to student_db
    print(f"Account created successfully for {email}! You are now logged in.")
    return new_user  # Return the newly created user object

# Teacher's sub-menu
def teacher_sub_menu():
    print("\nTeacher Sub-Menu:")
    print("1. View student list")
    print("2. Assign homework")
    print("3. View grades")
    print("4. Create reminder")
    print("5. Log out")
    
    while True:
        choice = input("Please select an option: (1/2/3/4/5): ")
        if choice == "1":
            view_students()
        elif choice == "2":
            assign_homework()
        elif choice == "3":
            view_grades()
        elif choice == "4":
            create_reminder()
        elif choice == "5":
            print("Logging out...")
            break
        else:
            print("Invalid choice, please try again.")

# Function to view the list of students (for teacher)
def view_students():
    if student_db:
        print("Student List:")
        headers = ["Name", "Surname", "Email"]  # Define the headers explicitly
        # Use tabulate to display the student list in a nice table
        print(tabulate(student_db, headers=headers, tablefmt="grid"))
    else:
        print("No students found.")

# Function to assign homework (for teachers)
def assign_homework():
    subject = input("Enter the subject of the homework: ")
    due_date = input("Enter the due date (YYYY-MM-DD): ")
    description = input("Enter the homework description: ")

    homework_db.append({
        'subject': subject,
        'due_date': due_date,
        'description': description
    })
    print(f"Homework assigned for {subject} due on {due_date}.")

# Function to view grades (for teachers or students)
def view_grades():
    if grade_db:
        print("Grades List:")
        headers = ["Student Name", "Subject", "Grade"]
        print(tabulate(grade_db, headers, tablefmt="grid"))
    else:
        print("No grades found.")

# Function to create a reminder (for teachers)
def create_reminder():
    subject = input("Enter the subject for the reminder: ")
    due_date = input("Enter the due date (YYYY-MM-DD): ")
    reminder_message = input("Enter the reminder message: ")

    reminder_db.append({
        'subject': subject,
        'due_date': due_date,
        'reminder_message': reminder_message
    })
    print(f"Reminder created for {subject} due on {due_date}.")

# Function to view schedule (for students)
def view_schedule(user):
    print(f"Schedule for {user['name']} {user['surname']}:")
    # A mock schedule (can be expanded or fetched from a database)
    schedule = [
        {"day": "Monday", "subject": "Math"},
        {"day": "Tuesday", "subject": "Science"},
        {"day": "Wednesday", "subject": "History"},
        {"day": "Thursday", "subject": "Physical Education"},
        {"day": "Friday", "subject": "English"}
    ]
    # Use the keys of the dictionaries as headers
    print(tabulate(schedule, headers="keys", tablefmt="grid"))

# Function to view homework (for students)
def view_homework():
    if homework_db:
        print("Homework List:")
        headers = ["Subject", "Due Date", "Description"]
        print(tabulate(homework_db, headers, tablefmt="grid"))
    else:
        print("No homework assigned.")

# Student's sub-menu
def student_sub_menu(user):
    print("\nStudent Sub-Menu:")
    print("1. View your schedule")
    print("2. View your homework")
    print("3. View your grades")
    print("4. Log out")

    while True:
        choice = input("Please select an option: (1/2/3/4): ")
        if choice == "1":
            view_schedule(user)
        elif choice == "2":
            view_homework()
        elif choice == "3":
            view_grades()
        elif choice == "4":
            print("Logging out...")
            break
        else:
            print("Invalid choice, please try again.")

# Parent's sub-menu
def parent_sub_menu(user):
    print("\nParent Sub-Menu:")
    print("1. View child's schedule")
    print("2. View child's grades")
    print("3. Log out")

    while True:
        choice = input("Please select an option: (1/2/3): ")
        if choice == "1":
            # Assuming the first student in the list is the child
            view_schedule(user)
        elif choice == "2":
            view_grades()
        elif choice == "3":
            print("Logging out...")
            break
        else:
            print("Invalid choice, please try again.")

# Main function
def main():
    user = None
    while True:
        choice = get_choice()

        if choice == 1:  # Log in
            user = login()
            if user:
                if user['role'] == 1:  # Student
                    print("Welcome, Student!")
                    student_sub_menu(user)
                elif user['role'] == 2:  # Teacher
                    print("Welcome, Teacher!")
                    teacher_sub_menu()
                elif user['role'] == 3:  # Parent
                    print("Welcome, Parent!")
                    parent_sub_menu(user)

        elif choice == 2:  # Sign up
            user = signup()
            if user:
                if user['role'] == 1:  # Student
                    print("Welcome, Student!")
                    student_sub_menu(user)
                elif user['role'] == 2:  # Teacher
                    print("Welcome, Teacher!")
                    teacher_sub_menu()
                elif user['role'] == 3:  # Parent
                    print("Welcome, Parent!")
                    parent_sub_menu(user)

# Run the program
if __name__ == "__main__":
    main()
