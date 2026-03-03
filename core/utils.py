from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect


def is_teacher(user):
    if not user.is_authenticated:
        return False
    # superusers are also teachers
    if user.is_superuser:
        return True
    return user.groups.filter(name='teacher').exists()


def teacher_required(view_func=None, login_url='login'):
    actual_decorator = user_passes_test(is_teacher, login_url=login_url)
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator
