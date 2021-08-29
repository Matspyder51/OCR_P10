# Generated by Django 3.2.6 on 2021-08-29 15:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_created=True)),
                ('title', models.CharField(max_length=1024)),
                ('description', models.CharField(max_length=8192)),
                ('priority', models.CharField(choices=[('0', 'Faible'), ('1', 'Moyen'), ('2', 'Élevé')], default='0', max_length=1)),
                ('types', models.CharField(choices=[('0', 'Bug'), ('1', 'Amélioration'), ('2', 'Tâche')], default='0', max_length=1)),
                ('status', models.CharField(choices=[('0', 'A faire'), ('1', 'En cours'), ('2', 'Terminé')], default='0', max_length=1)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.project')),
            ],
        ),
    ]