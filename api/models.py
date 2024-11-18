from django.db import models

class User(models.Model):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)  # Store hashed passwords
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"
    


class Course(models.Model):
    course_name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.course_name


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    lesson_title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    position = models.IntegerField()  # Order of lessons in the course
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.lesson_title

class CourseTeacher(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='teachers')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='teaching_courses')

    class Meta:
        unique_together = ('course', 'teacher')

    def __str__(self):
        return f"{self.teacher} teaches {self.course}"


class CourseEnrollment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrolled_courses')
    enrollment_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('course', 'student')

    def __str__(self):
        return f"{self.student} enrolled in {self.course}"

class LessonCompletion(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='completions')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='completed_lessons')
    completion_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('lesson', 'student')

    def __str__(self):
        return f"{self.student} completed {self.lesson}"
