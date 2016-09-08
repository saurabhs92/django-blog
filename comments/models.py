from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from blog.models import Author

class CommentManager(models.Manager):
    def filter_by_instance(self, instance):
        content_type = ContentType.objects.get_for_model(instance.__class__)
        obj_id = instance.id
        qs = super(CommentManager, self).filter(content_type=content_type, object_id=obj_id)
        return qs

class Comment(models.Model):
    user 	= models.ForeignKey(Author)
    
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    
    content 	= models.TextField()
    timestamp 	= models.DateTimeField(auto_now_add=True, auto_now=False)

    objects = CommentManager()

    def __str__(self):
        return str(self.user.name)

    def __unicode__(self):
        return str(self.user.name)
