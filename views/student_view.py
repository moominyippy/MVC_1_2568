import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import List, Optional
from models.student import Student
from models.subject import Subject
from models.registration import Registration

class StudentView:
    def __init__(self):
        pass
    
    def display_login_menu(self):
        print("\n" + "="*50)
        print("STUDENT REGISTRATION SYSTEM")
        print("="*50)
        print("1. Student Login")
        print("2. Admin Login")
        print("3. Exit")
        print("="*50)
    
    def get_student_id(self) -> str:
        while True:
            student_id = input("Enter Student ID (8 digits starting with 69): ").strip()
            if len(student_id) == 8 and student_id.isdigit() and student_id.startswith("69"):
                return student_id
            print("Invalid Student ID format. Please enter 8 digits starting with 69.")
    
    def get_admin_password(self) -> str:
        return input("Enter Admin Password: ").strip()
    
    def display_student_menu(self, student: Student):
        print(f"\nWelcome, {student.get_full_name()}")
        print("="*50)
        print("STUDENT MENU")
        print("="*50)
        print("1. View Available Subjects")
        print("2. View Subject Details")
        print("3. Register for Subject")
        print("4. View My Registrations")
        print("5. View My Profile")
        print("6. Logout")
        print("="*50)
    
    def display_admin_menu(self):
        print("\n" + "="*50)
        print("ADMIN MENU")
        print("="*50)
        print("1. View All Students")
        print("2. View All Subjects")
        print("3. Add Student Grade")
        print("4. View Registration Statistics")
        print("5. Logout")
        print("="*50)
    
    def display_available_subjects(self, subjects: List[Subject]):
        print("\n" + "="*80)
        print("AVAILABLE SUBJECTS")
        print("="*80)
        print(f"{'ID':<10} {'Subject Name':<30} {'Credits':<8} {'Instructor':<20} {'Available':<10}")
        print("-"*80)
        
        for subject in subjects:
            available = "Yes" if subject.is_available() else "No"
            print(f"{subject.subject_id:<10} {subject.subject_name:<30} {subject.credits:<8} {subject.instructor:<20} {available:<10}")
        print("="*80)
    
    def display_subject_details(self, subject: Subject):
        print("\n" + "="*60)
        print("SUBJECT DETAILS")
        print("="*60)
        print(f"Subject ID: {subject.subject_id}")
        print(f"Subject Name: {subject.subject_name}")
        print(f"Credits: {subject.credits}")
        print(f"Instructor: {subject.instructor}")
        print(f"Prerequisite: {subject.prerequisite if subject.prerequisite else 'None'}")
        print(f"Max Students: {subject.max_students if subject.max_students != -1 else 'Unlimited'}")
        print(f"Current Students: {subject.current_students}")
        print(f"Available: {'Yes' if subject.is_available() else 'No'}")
        print("="*60)
    
    def get_subject_id(self) -> str:
        return input("Enter Subject ID: ").strip()
    
    def display_registration_success(self, subject_name: str):
        print(f"\n Successfully registered for {subject_name}")
        input("Press Enter to continue...")
    
    def display_registration_error(self, message: str):
        print(f"\n Registration Error: {message}")
        input("Press Enter to continue...")
    
    def display_student_registrations(self, student: Student, registrations: List[Registration], subjects: dict):
        print(f"\n{student.get_full_name()}'s Registrations")
        print("="*60)
        if not registrations:
            print("No registrations found.")
        else:
            print(f"{'Subject ID':<12} {'Subject Name':<30} {'Registration Date':<20}")
            print("-"*60)
            for reg in registrations:
                subject = subjects.get(reg.subject_id)
                subject_name = subject.subject_name if subject else "Unknown"
                print(f"{reg.subject_id:<12} {subject_name:<30} {reg.registration_date:<20}")
        print("="*60)
    
    def display_student_profile(self, student: Student):
        print(f"\n{student.get_full_name()}'s Profile")
        print("="*50)
        print(f"Student ID: {student.student_id}")
        print(f"Full Name: {student.get_full_name()}")
        print(f"Birth Date: {student.birth_date}")
        print(f"Age: {student.get_age()} years old")
        print(f"School: {student.school}")
        print(f"Email: {student.email}")
        print(f"Valid Age: {'Yes' if student.is_valid_age() else 'No'}")
        print("="*50)
    
    def display_student_grades(self, student: Student, grades: List):
        print(f"\n{student.get_full_name()}'s Grades")
        print("="*60)
        if not grades:
            print("No grades found.")
        else:
            print(f"{'Subject ID':<12} {'Subject Name':<30} {'Grade':<8} {'Semester':<10}")
            print("-"*60)
            for grade in grades:
                print(f"{grade.subject_id:<12} {'N/A':<30} {grade.grade:<8} {grade.semester:<10}")
        print("="*60)
    
    def display_all_students(self, students: List[Student]):
        print("\n" + "="*100)
        print("ALL STUDENTS")
        print("="*100)
        print(f"{'ID':<10} {'Name':<30} {'Age':<5} {'School':<30} {'Email':<25}")
        print("-"*100)
        for student in students:
            print(f"{student.student_id:<10} {student.get_full_name():<30} {student.get_age():<5} {student.school:<30} {student.email:<25}")
        print("="*100)
    
    def display_all_subjects(self, subjects: List[Subject]):
        print("\n" + "="*100)
        print("ALL SUBJECTS")
        print("="*100)
        print(f"{'ID':<10} {'Subject Name':<30} {'Credits':<8} {'Instructor':<20} {'Max':<8} {'Current':<8}")
        print("-"*100)
        for subject in subjects:
            max_students = str(subject.max_students) if subject.max_students != -1 else "Unlimited"
            print(f"{subject.subject_id:<10} {subject.subject_name:<30} {subject.credits:<8} {subject.instructor:<20} {max_students:<8} {subject.current_students:<8}")
        print("="*100)
    
    def get_grade_input(self) -> str:
        while True:
            grade = input("Enter Grade (A, B+, B, C+, C, D+, D, F): ").strip().upper()
            valid_grades = ["A", "B+", "B", "C+", "C", "D+", "D", "F"]
            if grade in valid_grades:
                return grade
            print("Invalid grade. Please enter A, B+, B, C+, C, D+, D, or F.")
    
    def display_grade_added(self, student_name: str, subject_name: str, grade: str):
        print(f"\n Grade {grade} added for {student_name} in {subject_name}")
        input("Press Enter to continue...")
    
    def display_registration_statistics(self, subjects: List[Subject]):
        print("\n" + "="*80)
        print("REGISTRATION STATISTICS")
        print("="*80)
        print(f"{'Subject ID':<12} {'Subject Name':<30} {'Current':<8} {'Max':<8} {'Available':<10}")
        print("-"*80)
        for subject in subjects:
            max_students = str(subject.max_students) if subject.max_students != -1 else "Unlimited"
            available = "Yes" if subject.is_available() else "No"
            print(f"{subject.subject_id:<12} {subject.subject_name:<30} {subject.current_students:<8} {max_students:<8} {available:<10}")
        print("="*80)
    
    def display_message(self, message: str):
        print(f"\n{message}")
        input("Press Enter to continue...")
    
    def get_menu_choice(self) -> str:
        return input("Enter your choice: ").strip()
    
    def clear_screen(self):
        print("\n" * 50)

    def display_grade_error(self, message: str):
        print(f"\n❌ Grade Error: {message}")
        input("Press Enter to continue...")
