from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from comment.models import Comment

STATUS = (
    (0,"Draft"),
    (1,"Publish")
)

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.CharField(max_length=60)
    updated_on = models.DateTimeField(auto_now= True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    comments = GenericRelation(Comment)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title
