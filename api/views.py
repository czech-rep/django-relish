from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import UserSerializer, GroupSerializer

class UserViewSet(viewsets.ModelViewSet):
    # API endpoint that allows users to be viewed or edited
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

from rest_framework import status
from rest_framework.decorators import api_view
from blog.models import Post

@api_view(['GET'])
def api_detail_blog_view(request, id):

    try:
        queryset = Post.objects.get(id=id)
    except BlogPost.DoesNotExist:
        return Responce(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BlogPostSerializer(queryset)
        return Response(serializer.data)
    