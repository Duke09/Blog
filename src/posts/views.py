from urllib.parse import quote_plus
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.contenttypes.models import ContentType

from comments.models import Comment
from comments.forms import CommentForm

from .models import Post
from .forms import PostForm
from django.db.models import Q

# Create your views here.
def post_home(request):
    qs_list = Post.objects.active()        #.order_by("-timestamp")
    
    if request.user.is_staff or request.user.is_superuser:
        qs_list = Post.objects.all()

    query = request.GET.get("q")
    
    if query:
        qs_list = qs_list.filter(
            Q(title__icontains=query)|
            Q(content__icontains=query)
        )

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
        'page_num': page_num,
    }
    return render(request, "posts/home.html", context)

def post_detail(request, id):
    instance = get_object_or_404(Post, id=id)

    initial_data = {
        'content_type': instance.get_content_type,
        'object_id': instance.id
    }

    form = CommentForm(
        request.POST or None, 
        initial=initial_data
    )

    if form.is_valid():
        c_type = form.cleaned_data.get('content_type').split()
        
        content_type = ContentType.objects.get(
            app_label=c_type[0], 
            model=c_type[2]
        )    #app_label, comment, id, logentry, model, permission
        
        obj_id = form.cleaned_data.get('object_id')
        content_data = form.cleaned_data.get('content')

        new_comment, created = Comment.objects.get_or_create(
            user=request.user,
            content_type=content_type,
            object_id=obj_id,
            content=content_data
        )
        return HttpResponseRedirect(
            new_comment.content_object.get_absolute_url()
        )

    comments = instance.comments

    context = {
        'obj': instance,
        'comments': comments,
        'form': form
    }
    return render(request, "posts/detail.html", context)

def post_create(request):
    if not request.user.is_authenticated:
        raise Http404

    form = PostForm(
        request.POST or None, 
        request.FILES or None
    )
    
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        messages.success(request, "Post Created")
        return HttpResponseRedirect(instance.get_absolute_url())
    
    context = {
        "form": form,
        "title": "New"
    }
    return render(request, "posts/form.html", context)

def post_update(request, id):
    if not request.user.is_authenticated:
        raise Http404

    instance = get_object_or_404(Post, id=id)
    
    form = PostForm(
        request.POST or None, request.FILES or None, 
        instance=instance
    )
    
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Post Updated")
        return HttpResponseRedirect(instance.get_absolute_url())
    
    context = {
        "obj": instance,
        "form": form,
        "title": "Edit"
    }
    return render(request, "Posts/form.html", context)

def post_delete(request, id):
    instance = get_object_or_404(Post, id=id)
    # instance.delete()
    print(id)
    messages.success(request, "Post Deleted")
    return redirect("posts:home")