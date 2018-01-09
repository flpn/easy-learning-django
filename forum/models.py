from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save

from .utils import unique_slug_generator


User = settings.AUTH_USER_MODEL

class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    text = models.TextField(max_length=500)
    views = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
    tags = models.TextField()
    published = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField()

    def __str__(self):
        return self.title


def pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(pre_save_receiver, sender=Question)
