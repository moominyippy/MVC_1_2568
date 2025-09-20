import csv
import os
from typing import List, Optional, Dict

class Grade:
    def __init__(self, student_id: str, subject_id: str, grade: str, semester: str = "1/2024"):
        self.student_id = student_id
        self.subject_id = subject_id
        self.grade = grade
        self.semester = semester
    
    def to_dict(self) -> dict:
        return {
            "student_id": self.student_id,
            "subject_id": self.subject_id,
            "grade": self.grade,
            "semester": self.semester
        }
    
    @staticmethod
    def from_dict(data: dict) -> "Grade":
        return Grade(
            student_id=data["student_id"],
            subject_id=data["subject_id"],
            grade=data["grade"],
            semester=data.get("semester", "1/2024")
        )

class GradeModel:
    def __init__(self, data_file: str = "data/grades.csv"):
        self.data_file = data_file
        self.grades = []
        self.load_grades()
    
    def load_grades(self):
        if not os.path.exists(self.data_file):
            return
        
        with open(self.data_file, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                grade = Grade.from_dict(row)
                self.grades.append(grade)
    
    def save_grades(self):
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        
        with open(self.data_file, "w", newline="", encoding="utf-8") as file:
            if self.grades:
                fieldnames = ["student_id", "subject_id", "grade", "semester"]
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for grade in self.grades:
                    writer.writerow(grade.to_dict())
    
    def add_grade(self, student_id: str, subject_id: str, grade: str, semester: str = "1/2024") -> bool:
        # ตรวจสอบว่ามีเกรดในวิชานี้แล้วหรือไม่
        if self.has_grade(student_id, subject_id):
            return False
        
        grade_obj = Grade(student_id, subject_id, grade, semester)
        self.grades.append(grade_obj)
        self.save_grades()
        return True
    
    def has_grade(self, student_id: str, subject_id: str) -> bool:
        for grade in self.grades:
            if grade.student_id == student_id and grade.subject_id == subject_id:
                return True
        return False
    
    def get_grade(self, student_id: str, subject_id: str) -> Optional[str]:
        for grade in self.grades:
            if grade.student_id == student_id and grade.subject_id == subject_id:
                return grade.grade
        return None
    
    def get_student_grades(self, student_id: str) -> List[Grade]:
        return [grade for grade in self.grades if grade.student_id == student_id]
    
    def is_passing_grade(self, grade: str) -> bool:
        passing_grades = ["A", "B+", "B", "C+", "C", "D+", "D"]
        return grade in passing_grades 