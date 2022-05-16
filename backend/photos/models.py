from django.db import models


class Photo(models.Model):
    photo = models.FileField(upload_to='raw')
