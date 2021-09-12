# Generated by Django 3.2.6 on 2021-09-05 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_alter_project_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='type',
            field=models.CharField(choices=[('0', 'Back-end'), ('1', 'Front-end'), ('2', 'iOS'), ('3', 'Android')], max_length=1, null=True),
        ),
    ]
