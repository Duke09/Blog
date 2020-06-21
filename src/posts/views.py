from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Post
from .forms import PostForm
# Create your views here.
def post_home(request):
    qs_list = Post.objects.all()        #.order_by("-timestamp")
    paginator = Paginator(qs_list, 2)
    page_num = 'page'
    page = request.GET.get(page_num)
    try:
        qs = paginator.page(page)
    except PageNotAnInteger:
        qs = paginator.page(1)
    except EmptyPage:
        qs = paginator.page(paginator.num_pages)

    context = {
        "object_list": qs,
        'page_num': page_num
    }
    # return HttpResponse("Hello")
    return render(request, "posts/home.html", context)

def post_detail(request, id):
    instance = get_object_or_404(Post, id=id)
    context = {
        'obj': instance,
    }
    return render(request, "posts/detail.html", context)

def post_create(request):
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Post Created")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "form": form
    }
    return render(request, "posts/create.html", context)

def post_update(request, id):
    instance = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Post Updated")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "obj": instance,
        "form": form
    }
    return render(request, "Posts/update.html", context)

def post_delete(request, id):
    instance = get_object_or_404(Post, id=id)
    instance.delete()
    messages.success(request, "Post Deleted")
    return redirect("posts:home")