# MVC ระบบลงทะเบียนเรียนล่วงหน้า (Python + CSV)

> **ข้อสอบข้อที่ 2** · โครงงานตัวอย่างสำหรับระบบลงทะเบียนเรียนล่วงหน้าของนักเรียน ม.ปลาย โดยใช้รูปแบบ **Model–View–Controller (MVC)**

**ภาษา:** Python · **แหล่งข้อมูล:** CSV Files

> 🛡️ **Admin Login:** `admin123`

---

## สารบัญ (Table of Contents)

* [ภาพรวมโครงการ](#ภาพรวมโครงการ)
* [โครงสร้างโฟลเดอร์](#โครงสร้างโฟลเดอร์)
* [หน้าที่ของไฟล์หลัก](#หน้าที่ของไฟล์หลัก)
* [การติดตั้งและการใช้งาน](#การติดตั้งและการใช้งาน)
* [รูปแบบไฟล์ข้อมูล (CSV Schemas)](#รูปแบบไฟล์ข้อมูล-csv-schemas)
* [ฺBusiness Rules และการตรวจสอบความถูกต้อง](#Business-Rules-และการตรวจสอบความถูกต้อง)
* [ลำดับขั้นตอนการทำงานสำคัญ (Flows)](#ลำดับขั้นตอนการทำงานสำคัญ-flows)
* [ตัวอย่างการใช้งาน](#ตัวอย่างการใช้งาน)
* [กรณีใช้งานของผู้ดูแลระบบ (Admin)](#กรณีใช้งานของผู้ดูแลระบบ-admin)

---

## ภาพรวมโครงการ

ระบบนี้จำลองกระบวนการ **ลงทะเบียนล่วงหน้า** สำหรับรายวิชาปี 1 :

* **Model**: ดูแลข้อมูล นักเรียน/วิชา/การลงทะเบียน/เกรด และกฎตรวจสอบต่าง ๆ (อายุ, prerequisite, ที่นั่งว่าง ฯลฯ) ไปยัง CSV
* **View**: หน้าจอสำหรับแสดงผลและรับอินพุตจากผู้ใช้
* **Controller**: ตัวกลางประสานงาน รับคำสั่งจากผู้ใช้ผ่าน View แล้วเรียกใช้ Model เพื่อประมวลผล พร้อมส่งผลกลับไปที่ View

---

## โครงสร้างโฟลเดอร์

```
project-root/
├─ main.py
├─ controllers/
│  └─ registration_controller.py
├─ models/
│  ├─ student.py
│  ├─ subject.py
│  ├─ registration.py
│  └─ grade.py
├─ views/
│  └─ student_view.py
├─ data/
│  ├─ students.csv
│  ├─ subjects.csv
│  ├─ registrations.csv
│  └─ grades.csv
├─ requirements.txt   (แนะนำ)
└─ README.md
```

---

## หน้าที่ของไฟล์หลัก

### 1) `main.py`

จุดเริ่มต้นของโปรแกรม: สร้าง `RegistrationController` และเรียก `run()` เพื่อเริ่มระบบ

```python
# pseudo
from controllers.registration_controller import RegistrationController

def main():
    controller = RegistrationController()
    controller.run()

if __name__ == "__main__":
    main()
```

### 2) Controller — `controllers/registration_controller.py`

* `run()` แสดงเมนูหลัก / สลับหน้าเข้าสู่ระบบนักเรียน–ผู้ดูแลระบบ
* `student_login()` ตรวจสอบการเข้าใช้ของนักเรียน
* `admin_login()` ตรวจสอบการเข้าใช้ของแอดมิน (รหัสผ่านพื้นฐาน: `admin123`)
* `register_for_subject()` ลงทะเบียนเรียน (ตรวจ prerequisite, อายุ ≥ 15, ที่นั่งว่าง, ไม่ซ้ำ)
* `add_student_grade()` ให้เกรดนักเรียน (ต้องลงทะเบียนก่อน)
* `view_available_subjects()` แสดงรายวิชาที่ว่าง

> **บทบาท:** รับอินพุตจาก View → เรียก Model ประมวลผล → ส่งผลลัพธ์กลับ View

### 3) Models — `models/*.py`

* `student.py`

  * `Student`: เก็บข้อมูลส่วนบุคคล (ID, ชื่อ, วันเกิด, อายุคำนวณ)
  * ตรวจสอบอายุ (ต้อง ≥ 15 ปี)
  * จัดการเกรด/วิชาที่ลงทะเบียนในหน่วยความจำ
  * `StudentModel`: โหลด/บันทึก CSV, ตรวจรูปแบบ Student ID (ขึ้นต้นด้วย 69 และยาว 8 ตัว), ค้นหา

* `subject.py`

  * `Subject`: เก็บข้อมูลวิชา (ID, ชื่อ, หน่วยกิต, อาจารย์, prerequisite, max/current students)
  * จัดการจำนวนรับสูงสุด / เพิ่ม–ลดผู้ลงทะเบียน
  * `SubjectModel`: โหลด/บันทึก CSV, ค้นหาวิชาที่ว่าง, ตรวจ prerequisite

* `registration.py`

  * `Registration`: โครงสร้างข้อมูลการลงทะเบียน (student\_id, subject\_id, วันที่ลงทะเบียน)
  * `RegistrationModel`: โหลด/บันทึก CSV, ตรวจซ้ำ, นับจำนวนต่อวิชา

* `grade.py`

  * `Grade`: โครงสร้างข้อมูลเกรด (student\_id, subject\_id, grade, semester)
  * `GradeModel`: โหลด/บันทึก CSV, ตรวจรูปแบบเกรดที่อนุญาต `{A, B+, B, C+, C, D+, D}`
  * ตรวจสอบ prerequisite จากเกรด (ผ่านตามเงื่อนไขที่วิชากำหนด)

### 4) View — `views/student_view.py`

* `display_login_menu()` เมนูเข้าสู่ระบบ (นักเรียน/แอดมิน/ออก)
* `display_student_menu()` เมนูนักเรียน (ดูรายวิชาว่าง/ลงทะเบียน/ดูโปรไฟล์)
* `display_available_subjects()` แสดงรายวิชาที่ว่าง
* `display_subject_details()` แสดงรายละเอียดวิชา
* `display_student_profile()` แสดงประวัตินักเรียน
* `get_student_id()`, `get_subject_id()` รับข้อมูลจากผู้ใช้

---

## การติดตั้งและการใช้งาน

### 1) เตรียมสภาพแวดล้อม

* Python 3.10+
* (แนะนำ) สร้าง virtualenv และติดตั้ง dependencies

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
```

> **requirements.txt (แนะนำ)**

```
python-dateutil
```

### 2) เตรียมไฟล์ข้อมูลเริ่มต้น

ตรวจสอบให้มีไฟล์ในโฟลเดอร์ `data/` ตาม schema ด้านล่าง (สามารถใส่ตัวอย่างเริ่มต้น)

### 3) รันโปรแกรม

```bash
python main.py
```

---

## รูปแบบไฟล์ข้อมูล (CSV Schemas)

> **Encoding:** UTF-8, **Delimiter:** `,`

### `data/students.csv`

หัวตาราง: `student_id,title,first_name,last_name,birth_date,school,email`

ตัวอย่าง:

```
69000001,Mr.,John,Smith,2005-03-15,St. Mary's International School,john.smith@email.com
```

### `data/subjects.csv`

หัวตาราง: `subject_id,subject_name,credits,instructor,prerequisite,max_students,current_students`

ตัวอย่าง:

```
05501001,Basic Mathematics,3,Prof. John Smith,,30,0
```

### `data/registrations.csv`

หัวตาราง: `student_id,subject_id,registration_date`

ตัวอย่าง:

```
69000001,90690008,2025-09-20 15:17:20
```

### `data/grades.csv`

หัวตาราง: `student_id,subject_id,grade,semester`

ตัวอย่าง:

```
69000001,90690007,A,1/2024
```

---

## Business Rules และการตรวจสอบความถูกต้อง

* **Student ID**: ยาว 8 หลัก, สองหลักแรกต้องเป็น `69`
* **อายุขั้นต่ำ**: นักเรียนต้องมีอายุ **≥ 15 ปี** (คำนวณจาก `birth_date` ณ วันลงทะเบียน)
* **Prerequisite**: ถ้าวิชามี prerequisite ต้องตรวจจาก `GradeModel` ว่านักเรียน **ผ่าน** รายวิชาที่กำหนด (เช่น เกรดในชุด `{A, B+, B, C+, C, D+, D}` ตามเกณฑ์ผ่านของสถาบัน)
* **จำนวนที่นั่ง**: ตรวจ `max_students` เทียบ `current_students` ต้อง **ยังไม่เต็ม**
* **ลงทะเบียนซ้ำ**: ห้ามซ้ำรายวิชาเดิมในภาคการศึกษาเดียวกัน (กำหนดเกณฑ์ใน `RegistrationModel`)
* **รูปแบบเกรดที่ยอมรับ**: `{A, B+, B, C+, C, D+, D}`

---

## ลำดับขั้นตอนการทำงานสำคัญ (Flows)

### 1) เริ่มระบบ

```
main.py → RegistrationController.run() → View.display_login_menu()
```

### 2) ลงทะเบียนเรียน

```
View(รับ Student ID/Subject ID)
  → Controller.register_for_subject()
    → StudentModel: ตรวจอายุ ≥ 15
    → GradeModel: ตรวจ prerequisite
    → SubjectModel: ตรวจที่นั่งว่าง
    → RegistrationModel: ตรวจไม่ซ้ำ & บันทึก CSV
  → View: แสดงผลสำเร็จ/สาเหตุผิดพลาด
```

### 3) ให้เกรด (Admin)

```
View(รับ Student ID, Subject ID, Grade)
  → Controller.add_student_grade()
    → RegistrationModel: ตรวจว่าลงทะเบียนจริง
    → GradeModel: ตรวจรูปแบบเกรด & บันทึก CSV
    → StudentModel: อัปเดตในหน่วยความจำ (ถ้ามี)
  → View: แสดงผลสำเร็จ
```

### 4) ตรวจ prerequisite

```
Controller → GradeModel(ตรวจผ่าน) → SubjectModel(ยืนยัน) → RegistrationModel(บันทึก)
```

---

## ตัวอย่างการใช้งาน

> **โฟลว์นักเรียน**

1. เปิดโปรแกรม → เลือก "เข้าสู่ระบบนักเรียน"
2. กรอก `Student ID` → ดูรายวิชาที่ว่าง → เลือก `Subject ID` เพื่อขอลงทะเบียน
3. ระบบจะแจ้งผล: สำเร็จ / ผิดพลาด (พร้อมเหตุผล)

> **โฟลว์ผู้ดูแลระบบ (Admin)**

1. เปิดโปรแกรม → เลือก "เข้าสู่ระบบผู้ดูแลระบบ"
2. กรอกบัญชี `admin` และรหัสผ่าน `admin123`
3. เลือกเมนู: เพิ่มเกรดนักเรียน / ดูรายวิชาที่ว่าง / ตรวจรายการลงทะเบียน ฯลฯ

---

## กรณีใช้งานของผู้ดูแลระบบ (Admin)

* **เพิ่มเกรดนักเรียน**: ต้องมีข้อมูลการลงทะเบียนใน `registrations.csv` ก่อนเสมอ
* **ปรับที่นั่งวิชา**: เปลี่ยน `max_students` ใน `subjects.csv` (หรือทำเมนูให้แก้ไขผ่าน Controller)
* **สำรองข้อมูล**: ควรสำรองไฟล์ใน `data/` ก่อนใช้งานจริงทุกครั้ง

---




