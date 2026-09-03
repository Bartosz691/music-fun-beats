from rest_framework import viewsets

from .models import Album
from .permissions import IsAdminOrReadOnly
from .serializers import AlbumSerializer


class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all().order_by('title')
    serializer_class = AlbumSerializer
    permission_classes = [IsAdminOrReadOnly]