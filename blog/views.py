from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    data = {'indexdata': 'Data from views.py file.'}
    return render(request, 'blog/index.html', data)
