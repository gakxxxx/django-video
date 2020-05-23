from django.db import models

class VideoContent(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    upload_date = models.DateTimeField()
    original_name = models.CharField(max_length=200)
    filename = models.CharField(max_length=200, default="")
    thumb_frame = models.IntegerField(default=0)

class VideoTagName(models.Model):
    name = models.CharField(max_length=200, default="")

class VideoTagList(models.Model):
    content = models.ForeignKey(VideoContent, on_delete=models.CASCADE)
    tag = models.ForeignKey(VideoTagName, on_delete=models.CASCADE)
