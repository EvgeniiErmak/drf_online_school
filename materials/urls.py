# materials/urls.py
from django.urls import path
from .views import CourseViewSet, LessonListCreateView, LessonRetrieveUpdateDestroyView, HomeView

app_name = 'materials'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('courses/', CourseViewSet.as_view({'get': 'list', 'post': 'create'}), name='course-list'),
    path('courses/<int:pk>/', CourseViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='course-detail'),
    path('lessons/', LessonListCreateView.as_view(), name='lesson-list'),
    path('lessons/<int:pk>/', LessonRetrieveUpdateDestroyView.as_view(), name='lesson-detail'),
]
