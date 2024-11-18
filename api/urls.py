from django.urls import path
from .views import CreateCourseView, ListCoursesView, UpdateCourseLessonsView, TrackProgressView

urlpatterns = [
    path('courses/', CreateCourseView.as_view(), name='create-course'),
    path('courses/list/', ListCoursesView.as_view(), name='list-courses'),
    path('courses/<int:pk>/lessons/', UpdateCourseLessonsView.as_view(), name='update-course-lessons'),
    path('courses/progress/', TrackProgressView.as_view(), name='track-progress'),
]