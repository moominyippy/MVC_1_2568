import csv
import os
from typing import List, Optional

class Subject:
    def __init__(self, subject_id: str, subject_name: str, credits: int, instructor: str,
                 prerequisite: str, max_students: int, current_students: int = 0):
        self.subject_id = subject_id
        self.subject_name = subject_name
        self.credits = credits
        self.instructor = instructor
        self.prerequisite = prerequisite if prerequisite else ""
        self.max_students = max_students
        self.current_students = current_students
    
    def is_available(self) -> bool:
        if self.max_students == -1:
            return True
        return self.current_students < self.max_students
    
    def can_register(self) -> bool:
        return self.is_available()
    
    def register_student(self) -> bool:
        if self.can_register():
            self.current_students += 1
            return True
        return False
    
    def unregister_student(self) -> bool:
        if self.current_students > 0:
            self.current_students -= 1
            return True
        return False
    
    def to_dict(self) -> dict:
        return {
            "subject_id": self.subject_id,
            "subject_name": self.subject_name,
            "credits": self.credits,
            "instructor": self.instructor,
            "prerequisite": self.prerequisite,
            "max_students": self.max_students,
            "current_students": self.current_students
        }
    
    @staticmethod
    def from_dict(data: dict) -> "Subject":
        return Subject(
            subject_id=data["subject_id"],
            subject_name=data["subject_name"],
            credits=int(data["credits"]),
            instructor=data["instructor"],
            prerequisite=data.get("prerequisite", ""),
            max_students=int(data["max_students"]),
            current_students=int(data.get("current_students", 0))
        )


class SubjectModel:
    def __init__(self, data_file: str = "data/subjects.csv"):
        self.data_file = data_file
        self.subjects = {}
        self.load_subjects()
    
    def load_subjects(self):
        if not os.path.exists(self.data_file):
            return
        
        with open(self.data_file, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                subject = Subject.from_dict(row)
                self.subjects[subject.subject_id] = subject
    
    def save_subjects(self):
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        
        with open(self.data_file, "w", newline="", encoding="utf-8") as file:
            if self.subjects:
                fieldnames = ["subject_id", "subject_name", "credits", "instructor", 
                             "prerequisite", "max_students", "current_students"]
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for subject in self.subjects.values():
                    writer.writerow(subject.to_dict())
    
    def add_subject(self, subject: Subject) -> bool:
        if not self.validate_subject_id(subject.subject_id):
            return False
        
        if subject.credits <= 0:
            return False
        
        if subject.max_students != -1 and subject.max_students <= 0:
            return False
        
        self.subjects[subject.subject_id] = subject
        self.save_subjects()
        return True
    
    def get_subject(self, subject_id: str) -> Optional[Subject]:
        return self.subjects.get(subject_id)
    
    def get_all_subjects(self) -> List[Subject]:
        return list(self.subjects.values())
    
    def get_available_subjects(self) -> List[Subject]:
        return [subject for subject in self.subjects.values() if subject.is_available()]
    
    def validate_subject_id(self, subject_id: str) -> bool:
        if not subject_id.isdigit() or len(subject_id) != 8:
            return False
        return subject_id.startswith("0550") or subject_id.startswith("9069")
    
    def get_subjects_by_prerequisite(self, prerequisite_id: str) -> List[Subject]:
        return [subject for subject in self.subjects.values() 
                if subject.prerequisite == prerequisite_id]
