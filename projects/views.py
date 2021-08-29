from rest_framework import viewsets
from rest_framework import permissions
from projects.serializers import ProjectSerializer
from projects.models import Project


# Create your views here.
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        user_id = request.user.id
        pass
