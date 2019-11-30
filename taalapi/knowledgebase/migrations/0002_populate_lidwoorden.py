from django.db import migrations

from knowledgebase.models import Lidwoord


def populate_lidwoorden(apps, schema_editor):
    for lv in ['de', 'het']:
        Lidwoord(value=lv).save()

class Migration(migrations.Migration):

    dependencies = [
        ('knowledgebase', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_lidwoorden)
    ]
