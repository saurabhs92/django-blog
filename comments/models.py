from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from blog.models import Post, Author

class Comment(models.Model):
    user 	= models.ForeignKey(Author)
    # post 	= models.ForeignKey(Post)
    
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    
    content 	= models.TextField()
    timestamp 	= models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return str(self.user.name)

    def __unicode__(self):
        return str(self.user.name)
