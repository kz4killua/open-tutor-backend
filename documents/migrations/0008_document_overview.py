# Generated by Django 5.0.4 on 2024-09-28 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0007_remove_flashcard_referenced_page_number_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='overview',
            field=models.TextField(blank=True, max_length=2048, null=True),
        ),
    ]
