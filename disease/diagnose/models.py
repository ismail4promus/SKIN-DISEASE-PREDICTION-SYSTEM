from django.db import models
from django.contrib.auth.models import User

class Disease(models.Model) :
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', blank=False, null=False)
    summary = models.TextField(blank=True, null=True)
    summary_val = models.TextField(blank=True, null=True)
    summary_desc = models.TextField(blank=True, null=True)
    summary_inception = models.TextField(blank=True, null=True)
    summary_inception_val = models.TextField(blank=True, null=True)
    summary_inception_desc = models.TextField(blank=True, null=True)
    summary_vgg = models.TextField(blank=True, null=True)
    summary_vgg_val = models.TextField(blank=True, null=True)
    summary_vgg_desc = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Diseasetype(models.Model):
    name = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    
    def get_image(self) :
        if self.image :
            return 'http://127.0.0.1:8000' + self.image.url
        else :
            return ''
