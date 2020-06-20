from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from .models import Post
# Create your views here.
def post_home(request):
    qs = Post.objects.all()
    context = {
        "object_list": qs
    }
    # return HttpResponse("Hello")
    return render(request, "posts/home.html", context)

def post_detail(request):
    instance = get_object_or_404(Post, id=1)
    context = {
        'object_list': instance
    }
    return render(request, "posts/detail.html", context)