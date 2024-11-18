from rest_framework import serializers
from .models import Course, Lesson, CourseEnrollment, LessonCompletion, User , CourseTeacher


class CourseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['course_name', 'description']



class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'

class ProgressSerializer(serializers.Serializer):
    student_id = serializers.IntegerField()
    lessons_completed = serializers.IntegerField()
    total_lessons = serializers.IntegerField()
    progress_percentage = serializers.FloatField()


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email']


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'lesson_title', 'content','position']


class CourseSerializer(serializers.ModelSerializer):
    teachers = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)


    class Meta:
        model = Course
        fields = ['id', 'course_name', 'description', 'teachers','lessons']

    def get_teachers(self, obj):

        course_teachers = CourseTeacher.objects.filter(course=obj).select_related('teacher')
        return TeacherSerializer([ct.teacher for ct in course_teachers], many=True).data



class LessonUpdateSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)  # Optional for new lessons
    lesson_title = serializers.CharField(required=False)
    content = serializers.CharField(required=False)
    position = serializers.CharField(required=False)
    remove = serializers.BooleanField(default=False)

class LessonsUpdateRequestSerializer(serializers.Serializer):
    lessons = LessonUpdateSerializer(many=True)