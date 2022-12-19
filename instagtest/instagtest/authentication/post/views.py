from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

from post.models import Stream, Post, Likes, PostFileContent  #не видит

from django.contrib.auth.decorators import login_required

from django.urls import reverse
from authentication.models import Profile


# Create your views here.
@login_required
def index(request):
    user = request.user
    posts = Stream.objects.filter(user=user)
    group_ids = []
    for post in posts:
        group_ids.append(post.post_id)
    post_items = Post.objects.filter(id__in=group_ids).all().order_by('-posted')

    template = loader.get_template('index.html')

    context = {
        'post_items': post_items,
    }

    return HttpResponse(template.render(context, request))


def PostDetails(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user
    profile = Profile.objects.get(user=user)

    if request.user.is_authenticated:
        profile = Profile.objects.get(user=user)

@login_required
def NewPost(request):
    user = request.user
    tags_objs = []
    files_objs = []

    if request.method == 'POST':
        form = NewPostForm(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist('content')
            caption = form.cleaned_data.get('caption')
            tags_form = form.cleaned_data.get('tags')

            tags_list = list(tags_form.split(','))

            for tag in tags_list:
                t, created = Tag.objects.get_or_create(title=tag)
                tags_objs.append(t)

            for file in files:
                file_instance = PostFileContent(file=file, user=user)
                file_instance.save()
                files_objs.append(file_instance)

            p, created = Post.objects.get_or_create(caption=caption, user=user)
            p.tags.set(tags_objs)
            p.content.set(files_objs)
            p.save()
            return redirect('index')
    else:
        form = NewPostForm()

    context = {
        'form': form,
    }

    return render(request, 'newpost.html', context)


