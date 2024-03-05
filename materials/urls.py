# materials/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .payment import CreateProductView, CreatePriceView, CreateCheckoutSession
from .views import (
    CourseViewSet,
    LessonListView,
    LessonCreateView,
    LessonRetrieveView,
    LessonUpdateView,
    LessonDestroyView,
    PaymentListCreateView,
    SubscriptionViewSet,
    HomeView,
)

app_name = 'materials'

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'subscriptions', SubscriptionViewSet, basename='subscription')

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('lessons/', LessonListView.as_view(), name='lesson-list'),
    path('lessons/<int:pk>/', LessonRetrieveView.as_view(), name='lesson-detail'),
    path('lessons/create/', LessonCreateView.as_view(), name='lesson-create'),
    path('lessons/<int:pk>/update/', LessonUpdateView.as_view(), name='lesson-update'),
    path('lessons/<int:pk>/destroy/', LessonDestroyView.as_view(), name='lesson-destroy'),
    path('payments/', PaymentListCreateView.as_view(), name='payment-list-create'),

    path('', include(router.urls)),

    path('create-product/', CreateProductView.as_view(), name='create-product'),
    path('create-price/', CreatePriceView.as_view(), name='create-price'),
    path('create-checkout-session/', CreateCheckoutSession.as_view(), name='create-checkout-session'),
]
