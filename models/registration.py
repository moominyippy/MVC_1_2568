import csv
import os
from typing import List, Optional
from datetime import datetime

class Registration:
    def __init__(self, student_id: str, subject_id: str, registration_date: str = None):
        self.student_id = student_id
        self.subject_id = subject_id
        self.registration_date = registration_date or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def to_dict(self) -> dict:
        return {
            "student_id": self.student_id,
            "subject_id": self.subject_id,
            "registration_date": self.registration_date
        }
    
    @staticmethod
    def from_dict(data: dict) -> "Registration":
        return Registration(
            student_id=data["student_id"],
            subject_id=data["subject_id"],
            registration_date=data.get("registration_date", "")
        )

class RegistrationModel:
    def __init__(self, data_file: str = "data/registrations.csv"):
        self.data_file = data_file
        self.registrations = []
        self.load_registrations()
    
    def load_registrations(self):
        if not os.path.exists(self.data_file):
            return
        
        with open(self.data_file, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                registration = Registration.from_dict(row)
                self.registrations.append(registration)
    
    def save_registrations(self):
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        
        with open(self.data_file, "w", newline="", encoding="utf-8") as file:
            if self.registrations:
                fieldnames = ["student_id", "subject_id", "registration_date"]
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for registration in self.registrations:
                    writer.writerow(registration.to_dict())
    
    def add_registration(self, student_id: str, subject_id: str) -> bool:
        if self.is_registered(student_id, subject_id):
            return False
        
        registration = Registration(student_id, subject_id)
        self.registrations.append(registration)
        self.save_registrations()
        return True
    
    def remove_registration(self, student_id: str, subject_id: str) -> bool:
        for i, registration in enumerate(self.registrations):
            if registration.student_id == student_id and registration.subject_id == subject_id:
                del self.registrations[i]
                self.save_registrations()
                return True
        return False
    
    def is_registered(self, student_id: str, subject_id: str) -> bool:
        for registration in self.registrations:
            if registration.student_id == student_id and registration.subject_id == subject_id:
                return True
        return False
    
    def get_student_registrations(self, student_id: str) -> List[Registration]:
        return [reg for reg in self.registrations if reg.student_id == student_id]
    
    def get_subject_registrations(self, subject_id: str) -> List[Registration]:
        return [reg for reg in self.registrations if reg.subject_id == subject_id]
    
    def get_registration_count(self, subject_id: str) -> int:
        return len(self.get_subject_registrations(subject_id))
