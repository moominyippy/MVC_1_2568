# ข้อสอบข้อที่2 รหัสของ admin คือ admin123

โครงสร้างระบบ MVC และหน้าที่ของแต่ละไฟล์
1. main.py
หน้าที่: จุดเริ่มต้นของโปรแกรม สร้าง Controller และเริ่มระบบ
def main():
    controller = RegistrationController()  # สร้าง Controller
    controller.run()  # เริ่มทำงาน

2. CONTROLLER
controllers/registration_controller.py
หน้าที่: ประสานงานระหว่าง Model และ View
ฟังก์ชันหลัก
2.1 run(): เริ่มระบบ แสดงเมนูหลัก
2.2 student_login(): ตรวจสอบการเข้าสู่ระบบนักเรียน
2.3 admin_login(): ตรวจสอบการเข้าสู่ระบบแอดมิน
2.4 register_for_subject(): ลงทะเบียนเรียน (ตรวจสอบ prerequisite, อายุ, จำนวนคน)
2.5 add_student_grade(): ให้เกรดนักเรียน (ตรวจสอบการลงทะเบียนก่อน)
2.6 view_available_subjects(): แสดงวิชาที่สามารถลงทะเบียนได้
การทำงานร่วมกัน:
รับข้อมูลจาก View
เรียกใช้ Model เพื่อประมวลผลข้อมูล
ส่งผลลัพธ์กลับไป View

3. MODEL

models/student.py
หน้าที่: จัดการข้อมูลนักเรียน
- Student: ข้อมูลนักเรียนแต่ละคน
เก็บข้อมูลส่วนตัว (ID, ชื่อ, วันเกิด, อายุ)
ตรวจสอบอายุ (ต้อง ≥ 15 ปี)
จัดการเกรดและวิชาที่ลงทะเบียน
- StudentModel: จัดการข้อมูลนักเรียนทั้งหมด
โหลด/บันทึกข้อมูลจาก CSV
ตรวจสอบความถูกต้องของ Student ID
ค้นหานักเรียน

models/subject.py
หน้าที่: จัดการข้อมูลวิชาเรียน
- Subject: ข้อมูลวิชาแต่ละวิชา
เก็บข้อมูลวิชา (ID, ชื่อ, หน่วยกิต, อาจารย์)
ตรวจสอบจำนวนคนสูงสุด
จัดการการลงทะเบียน/ยกเลิก
- SubjectModel: จัดการข้อมูลวิชาทั้งหมด
โหลด/บันทึกข้อมูลจาก CSV
ค้นหาวิชาที่ว่าง
ตรวจสอบ prerequisite

models/registration.py
หน้าที่: จัดการข้อมูลการลงทะเบียน
- Registration: ข้อมูลการลงทะเบียนแต่ละครั้ง
- RegistrationModel: จัดการข้อมูลการลงทะเบียนทั้งหมด
ตรวจสอบการลงทะเบียนซ้ำ
นับจำนวนการลงทะเบียนในแต่ละวิชา

models/grade.py
หน้าที่:จัดการข้อมูลเกรดนักเรียน
- Grade: ข้อมูลเกรดแต่ละรายการ
- GradeModel: จัดการข้อมูลเกรดทั้งหมด
ตรวจสอบเกรดผ่าน (A, B+, B, C+, C, D+, D)
ตรวจสอบ prerequisite จากเกรด

4. VIEW
views/student_view.py
หน้าที่: แสดงผลและรับข้อมูลจากผู้ใช้
ฟังก์ชันหลัก
4.1 display_login_menu(): แสดงเมนูเข้าสู่ระบบ
4.2 display_student_menu(): แสดงเมนูนักเรียน
4.3 display_available_subjects(): แสดงรายวิชาที่ว่าง
4.4 display_subject_details(): แสดงรายละเอียดวิชา
4.5 display_student_profile(): แสดงประวัตินักเรียน
4.6 get_student_id(), get_subject_id(): รับข้อมูลจากผู้ใช้

5. DATA (CSV Files)
- data/students.csv
student_id,title,first_name,last_name,birth_date,school,email
เช่น 69000001,Mr.,John,Smith,2005-03-15,St. Mary's International School,john.smith@email.com
หน้าที่: เก็บข้อมูลนักเรียน

- data/subjects.csv
subject_id,subject_name,credits,instructor,prerequisite,max_students,current_students
เช่น 05501001,Basic Mathematics,3,Prof. John Smith,,30,0
หน้าที่: เก็บข้อมูลวิชาเรียน

- data/registrations.csv
student_id,subject_id,registration_date
เช่น 69000001,90690008,2025-09-20 15:17:20
หน้าที่: เก็บข้อมูลการลงทะเบียน

- data/grades.csv
student_id,subject_id,grade,semester
เช่น 69000001,90690007,A,1/2024
หน้าที่: เก็บข้อมูลเกรดนักเรียน


การทำงานร่วมกันของระบบ MVC
1. การเริ่มต้นระบบ
main.py -> RegistrationController -> StudentView (แสดงเมนู)

2. การลงทะเบียนเรียน
View (รับข้อมูล) -> Controller -> Model (ตรวจสอบ) -> View (แสดงผล)

ขั้นตอน
1.View: รับ Student ID และ Subject ID
2.Controller: เรียกใช้ Model ต่างๆ
3.StudentModel: ตรวจสอบอายุ ≥ 15 ปี
4.GradeModel: ตรวจสอบ prerequisite
5.SubjectModel: ตรวจสอบจำนวนคนว่าง
6.RegistrationModel: บันทึกการลงทะเบียน
7.View: แสดงผลสำเร็จ/ผิดพลาด

3. การให้เกรด
View (รับข้อมูล) -> Controller -> Model (ตรวจสอบ) -> CSV (บันทึก) -> View (แสดงผล)

ขั้นตอน
1.View: รับ Student ID, Subject ID, Grade
2.Controller: ตรวจสอบการลงทะเบียน
3.GradeModel: บันทึกเกรดใน CSV
4.StudentModel: อัปเดตข้อมูลใน memory
5.View: แสดงผลสำเร็จ

4. การตรวจสอบ Prerequisite
Controller -> GradeModel -> ตรวจสอบเกรดผ่าน -> SubjectModel -> RegistrationModel
