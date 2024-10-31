import json

class Person:
    def __init__(self, name, age, address):    
        self.name = name
        self.age = age
        self.address = address

    def display_person_info(self):
        print(f"Name: {self.name}\nAge: {self.age}\nAddress: {self.address}")

class Student(Person):
    def __init__(self, name, age, address, id):
        super().__init__(name, age, address)
        self.student_id = id
        self.grades = {}
        self.courses = []
    
    def add_grade(self, course, grade):
        if course in self.courses:
            self.grades[course] = grade
            print(f"Grade {grade} added for {self.name} in {course}.\n")
        else:
            print(f"{self.name} is not enrolled in {course}. Cannot add grade.")
    
    def enroll_course(self, course):
        self.courses.append(course)

    def display_student_info(self):
        self.display_person_info()
        print(f"Student ID: {self.student_id}\nEnrolled Courses: {', '.join(self.courses)}\nGrades: {self.grades}\n")

    def to_dict(self):
        return {
            'name': self.name,
            'age': self.age,
            'address': self.address,
            'student_id': self.student_id,
            'grades': self.grades,
            'courses': self.courses
        }
    
class Course:
    def __init__(self, name, code, instructor):    
        self.course_name = name
        self.course_code = code
        self.instructor_name = instructor
        self.students = []

    def add_students(self, student):
        if student not in self.students:
            self.students.append(student)
            print(f"Student {student.name} (ID: {student.student_id}) enrolled in {self.course_name}.\n")
        else:
            print(f"{student.name} is already enrolled in {self.course_name}.\n")

    def display_course_info(self):
        print(f"Course Name: {self.course_name}\nCourse Code: {self.course_code}\nInstructor: {self.instructor_name}")
        print(f"Enrolled Students: {', '.join([student.name for student in self.students])}\n")

    def to_dict(self):
        return {
            'course_name': self.course_name,
            'course_code': self.course_code,
            'instructor': self.instructor_name,
            'students': [student.student_id for student in self.students]
        }
    
class StudentManagementSystem:
    def __init__(self):
        self.students = {}
        self.courses = {}

    def add_student(self):
        try:
            name = input("Enter Name: ")
            age = int(input("Enter Age: "))
            address = input("Enter Address: ")
            student_id = input("Enter Student ID: ")
        except:
            print("Invalid input! Try again!\n")

        if student_id not in self.students:
            student = Student(name, age, address, student_id)
            self.students[student_id] = student
            print(f"Student {name} (ID: {student_id}) added successfully.\n")
        else:
            print(f"Student ID: {student_id} already exist! Try again!\n")

    def add_course(self):
        name = input("Enter Course Name: ")
        code = input("Enter Course Code: ")
        instructor = input("Enter Instructor Name: ")

        if code not in self.courses:
            course = Course(name, code, instructor)
            self.courses[code] = course
            print(f"Course {name} (Code: {code}) created with instructor {instructor}.\n")
        else:
            print(f"Course code: {code} already exist.\n")

    def enroll_course(self):
        student_id = input("Enter Student ID: ")
        course_code = input("Enter Course Code: ")

        if student_id in self.students and course_code  in self.courses:
            student = self.students[student_id]
            course = self.courses[course_code]
            student.enroll_course(course.course_name)
            course.add_students(student)
        else:
            print("Student ID or Course code doesn't exist! Try again!\n")

    def add_grade(self):
        student_id = input("Enter Student ID: ")
        course_code = input("Enter Course Code: ")
        grade = input("Enter Grade: ")

        if student_id in self.students and course_code in self.courses:
            student = self.students[student_id]
            course = self.courses[course_code]
            student.add_grade(course.course_name, grade)
        else:
            print("Invalid stident ID or course code! Try again!\n")

    def display_student_info(self):
        student_id = input("Enter Student ID: ")
        if student_id in self.students:
            student = self.students[student_id]
            student.display_student_info()
        else:
            print("Student not found.")

    def display_course_info(self):
        course_code = input("Enter Course Code: ")
        if course_code in self.courses:
            course = self.courses[course_code]
            course.display_course_info()
        else:
            print("Course not found.")

    def save_data(self):
        data = {
            "students": {student_id : student.to_dict() for student_id, student in self.students.items()},
            "courses": {course_code : course.to_dict() for course_code, course in self.courses.items()},
        }

        with open("studentdata.json", "w") as file:
            json.dump(data, file, indent=4)

        print("All student and course data saved successfully.\n")

    def load_data(self):
        try:
            with open('studentdata.json', 'r') as file:
                data = json.load(file)

            self.students = {}
            for student_id, student_data in data["students"].items():
                student = Student(
                    student_data['name'],
                    student_data['age'],
                    student_data['address'],
                    student_data['student_id']
                )
                student.grades = student_data['grades']
                student.courses = student_data['courses']
                self.students[student_id] = student

            self.courses = {}
            for course_code, course_data in data["courses"].items():
                course = Course(
                    course_data['course_name'],
                    course_data['course_code'],
                    course_data['instructor']
                )
                course.students = [self.students[student_id] for student_id in course_data['students']]
                self.courses[course_code] = course

            print("Data loaded successfully.")
        except FileNotFoundError:
            print("No saved data found.")

    def menu(self):
        while True:
            print("""
            ==== Student Management System ====
            1. Add New Student
            2. Add New Course
            3. Enroll Student in Course
            4. Add Grade for Student
            5. Display Student Details
            6. Display Course Details
            7. Save Data to File
            8. Load Data from File
            0. Exit
            """)
            
            try:
                choice = int(input("Select Option: "))

                if choice == 0:
                    print("Exiting Student Management System. Goodbye!\n")
                    break
                elif choice == 1:
                    self.add_student()
                elif choice == 2:
                    self.add_course()
                elif choice == 3:
                    self.enroll_course()
                elif choice == 4:
                    self.add_grade()
                elif choice == 5:
                    self.display_student_info()
                elif choice == 6:
                    self.display_course_info()
                elif choice == 7:
                    self.save_data()
                elif choice == 8:
                    self.load_data()
                else:
                    print("Choice doesn't exist! Please, choose among the list below!\n")
            except:
                print("Invalid Choice! Try Again!\n")

if __name__ == "__main__":
    system = StudentManagementSystem()
    system.menu()