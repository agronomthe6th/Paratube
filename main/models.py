from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from taggit.managers import TaggableManager
from django.contrib.auth.models import User, AbstractUser
from django.contrib.contenttypes.fields import GenericRelation
from comment.models import Comment

video_input_path = '/youtube/static/videos/'
img_output_path = '/youtube/static/thumbnails/'
# Create your models here.

class Videos(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=30)
    description = models.TextField(max_length=300, default="Nothing yet", null=True)
    comments = GenericRelation(Comment)
    path = models.CharField(max_length=60)
    thumbnailpath = models.CharField(max_length=600, default=1, null=True)
    datetime = models.DateTimeField(blank=False, null=False) #todo: auto_now=True
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True)
    username = models.CharField(default=False, null=True, max_length=60)
    tags = TaggableManager()
    embedornot = models.BooleanField(default=False)
    likes = models.ManyToManyField(User, blank=True, related_name='likes')
    dislikes = models.ManyToManyField(User, blank=True, related_name='dislikes')
    viewers = models.ManyToManyField(User, blank=True, related_name='viewers')
    views = models.IntegerField(default=0)

    @property
    def views_num(self):
        return self.views 

    # @property
    def viewed(self, user):
        # print(self.viewers.all())
        if user in self.viewers.all():
            return True
        else:
            return False

    @property
    def total_likes(self):
        return self.likes.count() 

    @property
    def total_dislikes(self):
        return self.dislikes.count()
    
    def get_absolute_url(self):
        return reverse('video', kwargs={'id': self.id})

    class Meta:
        ordering = ['-datetime'] 

    def __str__(self):
        return self.title

