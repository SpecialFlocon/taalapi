# Generated by Django 3.0 on 2019-12-09 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('knowledgebase', '0004_woord_accurate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='woord',
            name='woord',
            field=models.CharField(max_length=256, unique=True),
        ),
    ]