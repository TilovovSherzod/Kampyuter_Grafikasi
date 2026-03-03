from django.core.management.base import BaseCommand
from django.apps import apps

class Command(BaseCommand):
    help = 'Populate slug fields for BaseResource subclasses when empty (uses model.save()).'

    def handle(self, *args, **options):
        labels = ['core.Presentation', 'core.Guide', 'core.Video', 'core.Practical', 'core.Lab', 'core.Test']
        for label in labels:
            Model = apps.get_model(label)
            self.stdout.write(f'Processing {label}...')
            # Only process models that actually have a 'slug' field
            field_names = [f.name for f in Model._meta.get_fields()]
            if 'slug' not in field_names:
                self.stdout.write('  model has no slug field, skipping')
                continue
            qs = Model.objects.filter(slug='')
            count = qs.count()
            if count == 0:
                self.stdout.write('  none to update')
                continue
            for obj in qs:
                obj.save()
            self.stdout.write(f'  populated {count} slugs')
