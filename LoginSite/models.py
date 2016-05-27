from django.contrib.auth.models import User
from django.db import models


# class UploadFile(models.Model):
#
# 	img = models.FileField(null=True, blank=True)
# 	likes = models.IntegerField(default=0)
# 	dislikes = models.IntegerField(default=0)
# 	captions = models.CharField(max_length=100, default="")
# 	comments = models.TextField(default="")
#
# 	def __unicode__(self):
# 		return self.img


class Album(models.Model):
    user = models.ForeignKey(User, default=1)
    photo_title = models.CharField(max_length=500)
    upload = models.FileField()
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.photo_title



