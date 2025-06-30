from threading import Lock
from typing import Dict, List
import uuid

class Student:
    def __init__(self, name: str):
        self.student_id = str(uuid.uuid4())
        self.name = name
        self.registered_courses: List[str] = []

    def register_course(self, course_code: str):
        self.registered_courses.append(course_code)

    def get_courses(self) -> List[str]:
        return self.registered_courses

class Course:
    def __init__(self, course_code: str, name: str, instructor: str, max_capacity: int):
        self.course_code = course_code
        self.name = name
        self.instructor = instructor
        self.max_capacity = max_capacity
        self.enrolled_students: List[str] = []
        self.lock = Lock()

    def has_seat(self) -> bool:
        return len(self.enrolled_students) < self.max_capacity

    def enroll_student(self, student_id: str) -> bool:
        with self.lock:  # Prevent overbooking
            if self.has_seat():
                self.enrolled_students.append(student_id)
                return True
            return False

    def __str__(self):
        return f"{self.course_code} - {self.name} (Instructor: {self.instructor}) [{len(self.enrolled_students)}/{self.max_capacity}]"

class UniversitySystem:
    def __init__(self):
        self.students: Dict[str, Student] = {}
        self.courses: Dict[str, Course] = {}
        self.lock = Lock()

    def add_course(self, course: Course):
        self.courses[course.course_code] = course

    def register_student(self, name: str) -> Student:
        student = Student(name)
        self.students[student.student_id] = student
        return student

    def register_for_course(self, student_id: str, course_code: str) -> bool:
        student = self.students.get(student_id)
        course = self.courses.get(course_code)
        if not student or not course:
            return False

        if course.enroll_student(student_id):
            student.register_course(course_code)
            print(f"Student {student.name} registered for course {course_code}")
            return True
        else:
            print(f"Course {course_code} is full. Student {student.name} could not register.")
            return False

    def search_course(self, keyword: str) -> List[Course]:
        keyword = keyword.lower()
        return [
            course for course in self.courses.values()
            if keyword in course.course_code.lower() or keyword in course.name.lower()
        ]

    def get_student_courses(self, student_id: str) -> List[str]:
        student = self.students.get(student_id)
        return student.get_courses() if student else []

# -----------------------------
# Example Usage
if __name__ == "__main__":
    system = UniversitySystem()

    # Add sample courses
    system.add_course(Course("CS101", "Intro to CS", "Prof. Alan", 2))
    system.add_course(Course("DS201", "Data Structures", "Prof. Beth", 1))

    # Register students
    s1 = system.register_student("Alice")
    s2 = system.register_student("Bob")
    s3 = system.register_student("Charlie")

    # Course registrations
    system.register_for_course(s1.student_id, "CS101")
    system.register_for_course(s2.student_id, "CS101")
    system.register_for_course(s3.student_id, "CS101")  # Should fail (course full)

    # Search
    print("\nSearch Results for 'data':")
    for c in system.search_course("data"):
        print(c)

    # Student courses
    print(f"\nCourses for {s1.name}: {system.get_student_courses(s1.student_id)}")
