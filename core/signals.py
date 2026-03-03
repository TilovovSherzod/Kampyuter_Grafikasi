from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from django.apps import apps


@receiver(post_migrate)
def create_default_groups(sender, **kwargs):
    # Ensure groups exist: teacher and student
    if sender.name != 'core' and sender.name != 'django.contrib.auth':
        # run only when core or auth app migrates
        return
    Group.objects.get_or_create(name='teacher')
    Group.objects.get_or_create(name='student')