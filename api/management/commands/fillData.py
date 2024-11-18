from django.core.management.base import BaseCommand
from ...models import User , Course , Lesson , CourseTeacher , CourseEnrollment ,LessonCompletion


class Command(BaseCommand):
    help = 'Insert dummy data into the database'
    def handle(self, *args, **kwargs):
        # Add your dummy data script here
        self.stdout.write("Inserting dummy data...")
        # Create teachers
        teacher1 = User.objects.create(first_name="Alice", last_name="Smith", email="alice@mail.com", role="teacher", password_hash="hashed_password_1")
        teacher2 = User.objects.create(first_name="Bob", last_name="Johnson", email="bob@mail.com", role="teacher", password_hash="hashed_password_2")

        # Create students
        student1 = User.objects.create(first_name="Charlie", last_name="Brown", email="charlie@mail.com", role="student", password_hash="hashed_password_3")
        student2 = User.objects.create(first_name="Diana", last_name="Prince", email="diana@mail.com", role="student", password_hash="hashed_password_4")

        course1 = Course.objects.create(course_name="Math 101", description="Basic Mathematics")
        course2 = Course.objects.create(course_name="History 101", description="World History Overview")

        # Lessons for Math 101
        lesson1_math = Lesson.objects.create(course=course1, lesson_title="Algebra Basics", content="Intro to algebra", position=1)
        lesson2_math = Lesson.objects.create(course=course1, lesson_title="Geometry Basics", content="Intro to geometry", position=2)

        # Lessons for History 101
        lesson1_history = Lesson.objects.create(course=course2, lesson_title="Ancient Civilizations", content="History of ancient civilizations", position=1)
        lesson2_history = Lesson.objects.create(course=course2, lesson_title="World Wars", content="Overview of WWI and WWII", position=2)


        CourseTeacher.objects.create(course=course1, teacher=teacher1)
        CourseTeacher.objects.create(course=course2, teacher=teacher2)


        # Enroll Charlie and Diana in Math 101
        CourseEnrollment.objects.create(course=course1, student=student1)
        CourseEnrollment.objects.create(course=course1, student=student2)

        # Enroll Diana in History 101
        CourseEnrollment.objects.create(course=course2, student=student2)

        # Charlie completes Algebra Basics in Math 101
        LessonCompletion.objects.create(lesson=lesson1_math, student=student1)

        # Diana completes both lessons in Math 101
        LessonCompletion.objects.create(lesson=lesson1_math, student=student2)
        LessonCompletion.objects.create(lesson=lesson2_math, student=student2)

        self.stdout.write("Dummy data inserted successfully!")
