from rest_framework import viewsets

from .models import Album
from .permissions import IsAdminOrReadOnly
from .serializers import AlbumSerializer
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

@method_decorator(cache_page(60 * 5), name='list')
class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all().order_by('title')
    serializer_class = AlbumSerializer
    permission_classes = [IsAdminOrReadOnly]