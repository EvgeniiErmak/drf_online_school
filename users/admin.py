# users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('phone', 'city', 'avatar')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone', 'city', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
    )
    list_display = ('email', 'phone', 'city', 'is_staff', 'is_superuser')
    search_fields = ('email', 'phone', 'city')
    list_filter = ('is_staff', 'is_superuser', 'groups', 'date_joined')

    # Переопределение метода для отображения полей при редактировании
    def get_fieldsets(self, request, obj=None):
        if obj is None or request.user.is_superuser:
            return (
                (None, {'fields': ('email', 'password')}),
                ('Personal info', {'fields': ('phone', 'city', 'avatar')}),
                ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups')}),
                ('Important dates', {'fields': ('last_login',)}),
            )
        return super().get_fieldsets(request, obj)

    # Переопределение метода для отображения полей при добавлении нового пользователя
    def get_add_fieldsets(self, request, obj=None):
        if request.user.is_superuser:
            return (
                (None, {
                    'classes': ('wide',),
                    'fields': ('email', 'phone', 'city', 'password1', 'password2', 'groups'),
                }),
            )
        return super().get_add_fieldsets(request, obj)

    # Добавляем фильтрацию курсов и уроков для группы "Пользователи"
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser and request.user.groups.filter(name='Пользователи').exists():
            qs = qs.filter(owned_courses__owner=request.user) | qs.filter(owned_lessons__owner=request.user)
        return qs

    # Определяем, может ли пользователь изменять курсы и уроки
    def has_change_permission(self, request, obj=None):
        if obj is not None and not request.user.is_superuser and request.user.groups.filter(name='Пользователи').exists():
            # Разрешаем изменение только своих курсов и уроков
            return obj.owned_courses.filter(owner=request.user).exists() or obj.owned_lessons.filter(
                owner=request.user).exists()
        return super().has_change_permission(request, obj)

    # Определяем, может ли пользователь удалять курсы и уроки
    def has_delete_permission(self, request, obj=None):
        if obj is not None and not request.user.is_superuser and request.user.groups.filter(name='Пользователи').exists():
            # Разрешаем удаление только своих курсов и уроков
            return obj.owned_courses.filter(owner=request.user).exists() or obj.owned_lessons.filter(
                owner=request.user).exists()
        return super().has_delete_permission(request, obj)


# Переопределяем 'ordering' для CustomUserAdmin
CustomUserAdmin.ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)
