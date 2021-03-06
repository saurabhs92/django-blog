from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.utils.text import slugify
from django.utils.safestring import mark_safe
from markdown_deux import markdown
from .utils import get_read_time

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

def upload_location(instance, filename):
    return "%s/%s" % (instance.id, filename)

class PostManager(models.Manager):
    def active(self, *args, **kwargs):
        # super(PostManager, self).all() <=> Post.objects.all()
        return super(PostManager, self).filter(draft=False).filter(publish__lte=timezone.now())

class Post(models.Model):
    """
    Defines the blog_post table
    """
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    image = models.FileField(upload_to=upload_location, 
                             null=True, 
                             blank=True)
    #, height_field='height_field', width_field='width_field')
    #height_field = models.IntegerField(default=0)
    #width_field = models.IntegerField(default=0)
    body  = models.TextField()
    draft = models.BooleanField(default=False)
    publish = models.DateField(auto_now=False, auto_now_add=False)
    created_date = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_date = models.DateTimeField(auto_now_add=False, auto_now=True)
    # read_time = models.IntegerField(default=0) # Assume minutes
    author   = models.ForeignKey(Author)
    categories = models.ManyToManyField(Category)
    tags = models.ManyToManyField(Tag)

    objects = PostManager()

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('blogs:detail', kwargs={"slug": self.slug})
        
    def get_html(self):
        content = self.body
        html_text = markdown(content)
        return mark_safe(html_text)

    @property
    def comments(self):
        # not importing globally to avoid circular imports between both models 
        from comments.models import Comment
        instance = self
        qs = Comment.objects.filter_by_instance(instance)
        return qs

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type
    
    class Meta:
        ordering = ['-created_date', '-updated_date']

def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)
    
    # if instance.body:
    #     html_string = instance.get_html()
    #     read_time_var = get_read_time(html_string)
    #     instance.read_time = read_time_var



pre_save.connect(pre_save_post_receiver, sender=Post)

