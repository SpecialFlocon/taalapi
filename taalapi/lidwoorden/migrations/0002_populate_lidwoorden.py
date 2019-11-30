from django.db import migrations

from lidwoorden.models import Lidwoord


def populate_lidwoorden(apps, schema_editor):
    for lv in ['de', 'het']:
        Lidwoord(value=lv).save()

class Migration(migrations.Migration):

    dependencies = [
        ('lidwoorden', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_lidwoorden)
    ]
