import csv
import os
from datetime import datetime, date
from typing import List, Optional

class Student:
    def __init__(self, student_id: str, title: str, first_name: str, last_name: str, 
                 birth_date: str, school: str, email: str):
        self.student_id = student_id
        self.title = title
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.school = school
        self.email = email
        self.grades = {}
        self.registered_subjects = []
    
    def get_full_name(self) -> str:
        return f"{self.title}{self.first_name} {self.last_name}"
    
    def get_age(self) -> int:
        try:
            birth = datetime.strptime(self.birth_date, "%Y-%m-%d").date()
            today = date.today()
            age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
            return age
        except:
            return 0
    
    def is_valid_age(self) -> bool:
        return self.get_age() >= 15
    
    def add_grade(self, subject_id: str, grade: str):
        self.grades[subject_id] = grade
    
    def get_grade(self, subject_id: str) -> Optional[str]:
        return self.grades.get(subject_id)
    
    def register_subject(self, subject_id: str):
        if subject_id not in self.registered_subjects:
            self.registered_subjects.append(subject_id)
    
    def is_registered(self, subject_id: str) -> bool:
        return subject_id in self.registered_subjects
    
    def to_dict(self) -> dict:
        return {
            "student_id": self.student_id,
            "title": self.title,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "birth_date": self.birth_date,
            "school": self.school,
            "email": self.email
        }
    
    @staticmethod
    def from_dict(data: dict) -> "Student":
        return Student(
            student_id=data["student_id"],
            title=data["title"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            birth_date=data["birth_date"],
            school=data["school"],
            email=data["email"]
        )

class StudentModel:
    def __init__(self, data_file: str = "data/students.csv"):
        self.data_file = data_file
        self.students = {}
        self.load_students()
    
    def load_students(self):
        if not os.path.exists(self.data_file):
            return
        
        with open(self.data_file, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                student = Student.from_dict(row)
                self.students[student.student_id] = student
    
    def save_students(self):
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        
        with open(self.data_file, "w", newline="", encoding="utf-8") as file:
            if self.students:
                fieldnames = ["student_id", "title", "first_name", "last_name", 
                             "birth_date", "school", "email"]
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for student in self.students.values():
                    writer.writerow(student.to_dict())
    
    def add_student(self, student: Student) -> bool:
        if not self.validate_student_id(student.student_id):
            return False
        
        if not student.is_valid_age():
            return False
        
        self.students[student.student_id] = student
        self.save_students()
        return True
    
    def get_student(self, student_id: str) -> Optional[Student]:
        return self.students.get(student_id)
    
    def get_all_students(self) -> List[Student]:
        return list(self.students.values())
    
    def validate_student_id(self, student_id: str) -> bool:
        if not student_id.isdigit() or len(student_id) != 8:
            return False
        return student_id.startswith("69")
    
    def authenticate_student(self, student_id: str) -> Optional[Student]:
        return self.get_student(student_id)
