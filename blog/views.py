from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from .models import Post
from .forms import PostForm

#def index(request):
#    data = {'indexdata': 'Data from views.py file.'}
#    return render(request, 'blog/index.html', data)

def post_list(request):
    queryset_list = Post.objects.all()
    paginator = Paginator(queryset_list, 5) # Show 5 entries per page
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)

    context = {
        'object_list': queryset,
        'title': 'Posts',
        'page_request_var': page_request_var,
    }
    return render(request, 'blog/post_list.html', context)

def post_detail(request, id):
    instance = get_object_or_404(Post, id=id)
    context = {
        'title': instance.title,
        'instance': instance
    }
    return render(request, 'blog/post_detail.html', context)
    
def post_create(request):
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, 'Sucessfully Created')
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        'title': 'Create Post',
        'form': form
    }
    return render(request, 'blog/post_create.html', context)

def post_update(request, id):
    instance = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, 'Sucessfully updated', extra_tags='some-tag')
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        'title': instance.title,
        'form': form,
        'instance': instance
    }
    return render(request, 'blog/post_create.html', context)

def post_delete(request, id):
    instance = get_object_or_404(Post, id=id)
    instance.delete()
    messages.success(request, 'Successfully deleted.')
    return redirect('blogs:list')
