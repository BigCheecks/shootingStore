# Generated by Django 5.1.4 on 2024-12-06 14:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="weapon",
            name="image",
        ),
    ]
