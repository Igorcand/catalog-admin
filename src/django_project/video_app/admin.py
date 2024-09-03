from django.contrib import admin
from src.django_project.video_app.models import Video

class VideoAdmin(admin.ModelAdmin):
    pass

admin.site.register(Video, VideoAdmin)
