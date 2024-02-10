# materials/urls.py
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, LessonListCreateView, LessonRetrieveUpdateDestroyView

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
# Используем as_view для преобразования generic-классов в view функции
router.register(r'lessons', LessonListCreateView.as_view(), basename='lesson-list')
router.register(r'lessons', LessonRetrieveUpdateDestroyView.as_view(), basename='lesson-detail')

urlpatterns = router.urls