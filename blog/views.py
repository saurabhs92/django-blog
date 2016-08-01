from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Post

#def index(request):
#    data = {'indexdata': 'Data from views.py file.'}
#    return render(request, 'blog/index.html', data)

def post_list(request):
    queryset = Post.objects.all()
    context = {
        'object_list': queryset,
        'title': 'Posts'
    }
    return render(request, 'blog/index.html', context)

def post_detail(request, id):
    instance = get_object_or_404(Post, id=id)
    context = {
        'title': instance.title,
        'instance': instance
    }
    return render(request, 'blog/post_detail.html', context)
    
def post_create(request):
    return HttpResponse('<h1>Create</h1>')

def post_update(request):
    return HttpResponse('<h1>Update</h1>')

def post_delete(request):
    return HttpResponse('<h1>Delete</h1>')
