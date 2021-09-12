from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


# Create your models here.
class Project(models.Model):
    title = models.CharField(max_length=1024)
    description = models.TextField()

    class ProjectTypes(models.TextChoices):
        BACKEND = 0, _('Back-end')
        FRONTEND = 1, _('Front-end')
        IOS = 2, _('iOS')
        ANDROID = 3, _('Android')

    type = models.CharField(
        max_length=1,
        choices=ProjectTypes.choices,
        # null=True
    )

    author_user_id = models.ForeignKey(to=User, on_delete=models.CASCADE)


class Issue(models.Model):

    class IssuePriorities(models.TextChoices):
        LOW = 0, _('Faible')
        MEDIUM = 1, _('Moyen')
        IMPORTANT = 2, _('Élevé')

    class IssueTypes(models.TextChoices):
        BUG = 0, _('Bug')
        FEATURE = 1, _('Amélioration')
        TASK = 2, _('Tâche')

    class IssueStatus(models.TextChoices):
        TODO = 0, _('A faire')
        WIP = 1, _('En cours')
        DONE = 2, _('Terminé')

    title = models.CharField(max_length=1024)
    description = models.TextField()
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    project_id = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_created=True, auto_now_add=True)

    priority = models.CharField(
        max_length=1,
        choices=IssuePriorities.choices,
        default=IssuePriorities.LOW
    )

    types = models.CharField(
        max_length=1,
        choices=IssueTypes.choices,
        default=IssueTypes.BUG
    )

    status = models.CharField(
        max_length=1,
        choices=IssueStatus.choices,
        default=IssueStatus.TODO
    )

    assignee_user_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='assignee_user'
    )


class IssueComment(models.Model):

    description = models.TextField()
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    issue = models.ForeignKey(to=Issue, on_delete=models.CASCADE)


class Contributor(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['user', 'project']