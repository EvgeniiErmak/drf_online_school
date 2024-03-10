# materials/tasks.py
from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth import get_user_model
from .models import Course

User = get_user_model()


@shared_task
def send_course_update_notification(course_id):
    course = Course.objects.get(pk=course_id)
    subscribers = User.objects.filter(subscriptions__course=course)

    subject = f"Обновление курса: {course.title}"
    html_message = render_to_string('materials/course_update_email.html', {'course': course})
    plain_message = strip_tags(html_message)

    for subscriber in subscribers:
        send_mail(subject, plain_message, 'from@example.com', [subscriber.email], html_message=html_message)
