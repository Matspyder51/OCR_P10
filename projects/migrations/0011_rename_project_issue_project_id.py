# Generated by Django 3.2.6 on 2021-09-12 18:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0010_rename_author_project_author_user_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='issue',
            old_name='project',
            new_name='project_id',
        ),
    ]
