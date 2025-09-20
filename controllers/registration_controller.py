import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Optional, List
from models.student import Student, StudentModel
from models.subject import Subject, SubjectModel
from models.registration import Registration, RegistrationModel
from models.grade import GradeModel
from views.student_view import StudentView

class RegistrationController:
    def __init__(self):
        self.student_model = StudentModel()
        self.subject_model = SubjectModel()
        self.registration_model = RegistrationModel()
        self.grade_model = GradeModel()
        self.view = StudentView()
        self.current_student = None
        self.admin_password = "admin123"  # Simple admin password
    
    def run(self):
        while True:
            self.view.display_login_menu()
            choice = self.view.get_menu_choice()
            
            if choice == "1":
                self.student_login()
            elif choice == "2":
                self.admin_login()
            elif choice == "3":
                print("Thank you for using the system. Goodbye!")
                break
            else:
                self.view.display_message("Invalid choice. Please try again.")
    
    def student_login(self):
        student_id = self.view.get_student_id()
        student = self.student_model.authenticate_student(student_id)
        
        if student:
            self.current_student = student
            self.student_menu()
        else:
            self.view.display_message("Student not found. Please check your Student ID.")
    
    def admin_login(self):
        password = self.view.get_admin_password()
        if password == self.admin_password:
            self.admin_menu()
        else:
            self.view.display_message("Invalid admin password.")
    
    def student_menu(self):
        while True:
            self.view.display_student_menu(self.current_student)
            choice = self.view.get_menu_choice()
            
            if choice == "1":
                self.view_available_subjects()
            elif choice == "2":
                self.view_subject_details()
            elif choice == "3":
                self.register_for_subject()
            elif choice == "4":
                self.view_my_registrations()
            elif choice == "5":
                self.view_my_profile()
            elif choice == "6":
                self.current_student = None
                break
            else:
                self.view.display_message("Invalid choice. Please try again.")
    
    def admin_menu(self):
        while True:
            self.view.display_admin_menu()
            choice = self.view.get_menu_choice()
            
            if choice == "1":
                self.view_all_students()
            elif choice == "2":
                self.view_all_subjects()
            elif choice == "3":
                self.add_student_grade()
            elif choice == "4":
                self.view_registration_statistics()
            elif choice == "5":
                break
            else:
                self.view.display_message("Invalid choice. Please try again.")
    
    def view_available_subjects(self):
        # Get subjects that student hasn't registered for
        available_subjects = []
        for subject in self.subject_model.get_available_subjects():
            if not self.registration_model.is_registered(self.current_student.student_id, subject.subject_id):
                available_subjects.append(subject)
        
        if available_subjects:
            self.view.display_available_subjects(available_subjects)
        else:
            self.view.display_message("No available subjects found.")
    
    def view_subject_details(self):
        subject_id = self.view.get_subject_id()
        subject = self.subject_model.get_subject(subject_id)
        
        if subject:
            self.view.display_subject_details(subject)
        else:
            self.view.display_message("Subject not found.")
    
    def register_for_subject(self):
        subject_id = self.view.get_subject_id()
        subject = self.subject_model.get_subject(subject_id)
        
        if not subject:
            self.view.display_registration_error("Subject not found.")
            return
        
        # Check if already registered
        if self.registration_model.is_registered(self.current_student.student_id, subject_id):
            self.view.display_registration_error("You are already registered for this subject.")
            return
        
        # Check age requirement
        if not self.current_student.is_valid_age():
            self.view.display_registration_error("You must be at least 15 years old to register.")
            return
        
        # Check prerequisite using grade model
        if subject.prerequisite:
            prerequisite_grade = self.grade_model.get_grade(self.current_student.student_id, subject.prerequisite)
            if not prerequisite_grade or not self.grade_model.is_passing_grade(prerequisite_grade):
                self.view.display_registration_error(f"You must pass {subject.prerequisite} before registering for this subject.")
                return
        
        # Check if subject is available
        if not subject.is_available():
            self.view.display_registration_error("This subject is not available (full or not accepting registrations).")
            return
        
        # Register student
        if self.registration_model.add_registration(self.current_student.student_id, subject_id):
            # Update subject current students count
            subject.register_student()
            self.subject_model.save_subjects()
            
            # Update student's registered subjects
            self.current_student.register_subject(subject_id)
            
            self.view.display_registration_success(subject.subject_name)
            # กลับไปหน้าประวัตินักเรียนหลังลงทะเบียนสำเร็จ
            self.view_my_profile()
        else:
            self.view.display_registration_error("Registration failed. Please try again.")
    
    def view_my_registrations(self):
        registrations = self.registration_model.get_student_registrations(self.current_student.student_id)
        subjects_dict = {subject.subject_id: subject for subject in self.subject_model.get_all_subjects()}
        self.view.display_student_registrations(self.current_student, registrations, subjects_dict)
    
    def view_my_profile(self):
        self.view.display_student_profile(self.current_student)
    
    def view_all_students(self):
        students = self.student_model.get_all_students()
        self.view.display_all_students(students)
    
    def view_all_subjects(self):
        subjects = self.subject_model.get_all_subjects()
        self.view.display_all_subjects(subjects)
    
    def add_student_grade(self):
        student_id = self.view.get_student_id()
        student = self.student_model.get_student(student_id)
        
        if not student:
            self.view.display_message("Student not found.")
            return
        
        subject_id = self.view.get_subject_id()
        subject = self.subject_model.get_subject(subject_id)
        
        if not subject:
            self.view.display_message("Subject not found.")
            return
        
        # ตรวจสอบว่านักเรียนได้ลงทะเบียนวิชานี้แล้วหรือไม่
        if not self.registration_model.is_registered(student_id, subject_id):
            self.view.display_grade_error(f"Student {student.get_full_name()} has not registered for {subject.subject_name} yet. Cannot add grade.")
            return
        
        grade = self.view.get_grade_input()
        
        # บันทึกเกรดในไฟล์ CSV
        if self.grade_model.add_grade(student_id, subject_id, grade):
            # บันทึกเกรดใน student object ด้วย
            student.add_grade(subject_id, grade)
            self.student_model.save_students()
            
            self.view.display_grade_added(student.get_full_name(), subject.subject_name, grade)
        else:
            self.view.display_grade_error(f"Grade already exists for {student.get_full_name()} in {subject.subject_name}.")
    
    def view_registration_statistics(self):
        subjects = self.subject_model.get_all_subjects()
        self.view.display_registration_statistics(subjects)
