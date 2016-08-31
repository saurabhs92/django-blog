from django.db import models
from blog.models import Post, Author

class Comment(models.Model):
    user 	= models.ForeignKey(Author)
    post 	= models.ForeignKey(Post)
    content 	= models.TextField()
    timestamp 	= models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return str(self.user.name)

    def __unicode__(self):
        return str(self.user.name)
