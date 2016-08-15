from django.db import models
from django.core.urlresolvers import reverse

class Author(models.Model):
    """
    Defines the blog_author table
    """
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    bio = models.TextField()
    
    def __str__(self):
        return self.name

class Category(models.Model):
    cat_name = models.CharField('category name', max_length=50)
    cat_description = models.CharField('category description', max_length=255)
    
    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.cat_name

class Tag(models.Model):
    tag_name = models.CharField(max_length=50)
    tag_description = models.CharField(max_length=255)
    
    def __str__(self):
        return self.tag_name

class Post(models.Model):
    """
    Defines the blog_post table
    """
    title = models.CharField(max_length=200)
    image = models.FileField(null=True, blank=True)
    #, height_field='height_field', width_field='width_field')
    #height_field = models.IntegerField(default=0)
    #width_field = models.IntegerField(default=0)
    body  = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_date = models.DateTimeField(auto_now_add=False, auto_now=True)
    author   = models.ForeignKey(Author)
    categories = models.ManyToManyField(Category)
    tags = models.ManyToManyField(Tag)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('blogs:detail', kwargs={"id": self.id})
    
    class Meta:
        ordering = ['-created_date', '-updated_date']
