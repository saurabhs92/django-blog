from urllib.parse import quote_plus
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib import messages
from django.utils import timezone
from .models import Post
from .forms import PostForm
from comments.models import Comment

#def index(request):
#    data = {'indexdata': 'Data from views.py file.'}
#    return render(request, 'blog/index.html', data)

def post_list(request):
    today = timezone.now().date()
    queryset_list = Post.objects.active()
    if request.user.is_staff or request.user.is_superuser:
        queryset_list = Post.objects.all()
    query = request.GET.get('q')
    if query:
        queryset_list = Post.objects.filter(
            Q(title__icontains=query)|
            Q(body__icontains=query)|
            Q(author__name__icontains=query)
        ).distinct()
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
        'today': today,
    }
    return render(request, 'blog/post_list.html', context)

def post_detail(request, slug):
    instance = get_object_or_404(Post, slug=slug)
    if instance.draft or instance.publish > timezone.now().date():
        if not request.user.is_staff or not request.user.is_superuser:
            raise Http404
    share_string = quote_plus(instance.body)
    
    comments = instance.comments
    
    context = {
        'title': instance.title,
        'instance': instance,
        'share_string': share_string,
        'comments': comments,
    }
    return render(request, 'blog/post_detail.html', context)
    
def post_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
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

def post_update(request, slug):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, slug=slug)
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

def post_delete(request, slug):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, slug=slug)
    instance.delete()
    messages.success(request, 'Successfully deleted.')
    return redirect('blogs:list')
