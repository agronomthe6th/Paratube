from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import os
import shutil
from django.urls import reverse
from nanoid import generate

from main.models import Videos

def user_directory_path(instance, filename):
    path = 'users/static/profile_images/' + str(instance) 
    t = 'media/'+ path
    if os.path.exists(t):
        shutil.rmtree(t)
    filename = str(instance)+'_'+generate(size=5)+'.jpg'
    return os.path.join(path, filename)

class Profile(models.Model):
    # likedvideo = models.IntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='users/static/default.jpg', upload_to=user_directory_path)
    bio = models.TextField(default='Nothing yet')
    subscribers = models.ManyToManyField(User, related_name='subscribers')
    subscriptions = models.ManyToManyField(User, related_name='subscriptions')

    def __str__(self):
        return self.user.username

    @property
    def total_subscribers(self):
        return self.subscribers.count() 

    def save(self, *args, **kwargs):
        super().save()
        # print('ghytggy'+self.avatar.path)
        img = Image.open(self.avatar.path)
        newsize = (64, 64)
        img=img.resize(newsize)
        img=img.save(self.avatar.path)
        print(self.avatar.path)
    
    def get_absolute_url(self):
        return reverse('users-profile-view', kwargs={'user': self.user})

class Channel(models.Model):
    # profilepicpath = models.CharField(max_length=600,default="/static/playbutton.png" , null=True)
    # profilepic = models.ImageField(name='',default="/static/playbutton.png", null=True, blank=True )
    channel_name = models.CharField(max_length=50, blank=False, null=False,default="")
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
