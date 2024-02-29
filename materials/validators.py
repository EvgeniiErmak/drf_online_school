# materials/validators.py
from rest_framework.exceptions import ValidationError


def validate_video_link(value):
    if not value.startswith('https://www.youtube.com'):
        raise ValidationError("Ссылка должна вести только на youtube.com")
