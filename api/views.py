from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView ,CreateAPIView , UpdateAPIView
from .models import Course, Lesson, CourseEnrollment, LessonCompletion, User
from .serializers import CourseSerializer, LessonSerializer, ProgressSerializer , CourseCreateSerializer , LessonsUpdateRequestSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated , AllowAny
# Create a course 
class CreateCourseView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CourseCreateSerializer
    def post(self, request):
        serializer = CourseCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Retrieve all courses 
class ListCoursesView(ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [AllowAny] 

# Add/remove lessons from a course 
class UpdateCourseLessonsView(UpdateAPIView):
    """
    # add an existing lesson to course 
    {
        "lessons": [
            {
            "id": id,
            "lesson_title": "string",
            "content": "string",
            "position": "string",
            }
        ]
    }
  #  add a new lesson + assign it to course
    {
        "lessons": [
            {
                "lesson_title": "string",
                "content": "string",
                "position": "string"
            }
        ]
    }
   # remove a lesson 
        {
        "lessons": [
            {
                "id": id,
                "remove": true
            }
        ]
    }
    """
    permission_classes = [IsAuthenticated]
    serializer_class=LessonsUpdateRequestSerializer
    queryset = Lesson.objects.all() 
    def put(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        
        
        serializer = LessonsUpdateRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        lesson_data = serializer.validated_data['lessons']

        for lesson in lesson_data:
            lesson_id = lesson.get('id')
            if lesson_id:  # Update, delete, or sign an existing lesson
                lesson_instance = get_object_or_404(Lesson, pk=lesson_id)

                if lesson.get('remove', False):  # Delete the lesson
                    lesson_instance.delete()
                else:  # Update lesson
                    lesson_instance.course = course  
                    for key, value in lesson.items():
                        if key not in ['id', 'remove']:
                            setattr(lesson_instance, key, value)
                    lesson_instance.save()
            else:  # Create a new lesson
                new_lesson_serializer = LessonSerializer(data=lesson)
                if new_lesson_serializer.is_valid():
                    new_lesson_serializer.save(course=course)
                else:
                    return Response(new_lesson_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Lessons updated successfully."}, status=status.HTTP_200_OK)



# Track student progress 
class TrackProgressView(APIView):
    def get(self, request):
        courses = Course.objects.all()
        progress_data = []

        for course in courses:
            students = User.objects.filter(role='student', enrolled_courses__course=course).distinct()
            
            for student in students:
                total_lessons = course.lessons.count()
                completed_lessons = LessonCompletion.objects.filter(student=student, lesson__course=course).count()
                progress_percentage = (completed_lessons / total_lessons) * 100 if total_lessons > 0 else 0
                
                progress_data.append({
                    "course_id": course.id,
                    "course_name": course.course_name,
                    "student_id": student.id,
                    "student_name": f"{student.first_name} {student.last_name}",
                    "lessons_completed": completed_lessons,
                    "total_lessons": total_lessons,
                    "progress_percentage": round(progress_percentage, 2),
                })

        return Response(progress_data, status=status.HTTP_200_OK)