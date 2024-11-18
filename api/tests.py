import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

@pytest.fixture
def authenticated_client():
    """Fixture to provide an authenticated API client."""
    user = User.objects.create_user(username='testuser', password='testpass')
    token, _ = Token.objects.get_or_create(user=user)  
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')  
    return client

@pytest.mark.django_db
def test_create_course(authenticated_client):
    """Test the creation of a course using CreateCourseView."""
  
    payload = {
        "course_name": "Test Course",
        "description": "A sample course for testing."
    }

  
    response = authenticated_client.post("/api/lms/courses/", payload, format="json")

   
    assert response.status_code == status.HTTP_201_CREATED
    response_data = response.json()
    assert response_data["course_name"] == payload["course_name"]
    assert response_data["description"] == payload["description"]

    
    from .models import Course  
    course = Course.objects.get(course_name=payload["course_name"])
    assert course.description == payload["description"]


