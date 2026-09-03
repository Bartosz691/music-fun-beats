from django.contrib import admin

from .models import Album, Artist, Genre, Label, MusicFormat


admin.site.register(Artist)
admin.site.register(Genre)
admin.site.register(Label)
admin.site.register(MusicFormat)
admin.site.register(Album)