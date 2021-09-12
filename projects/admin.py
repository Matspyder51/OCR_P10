from projects.models import Project, Issue, IssueComment, Contributor
from django.contrib import admin

# Register your models here.
admin.site.register([Project, Issue, IssueComment, Contributor])