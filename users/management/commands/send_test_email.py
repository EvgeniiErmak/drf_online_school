# users/management/commands/send_test_email.py
from django.core.management.base import BaseCommand
from django.core.mail import send_mail


class Command(BaseCommand):
    help = 'Sends a test email'

    def handle(self, *args, **options):
        send_mail(
            'Тестовое сообщение',
            'Это тестовое сообщение для проверки рассылки.',
            'djermak9000@gmail.com',
            ['djermak3000@mail.ru'],
            fail_silently=False,
        )
