from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from blog.forms import CommentForm
from .models import Post


# Create your views here.
def index(request):
    posts = Post.objects.filter(published_at__lte = timezone.now())
    # posts = Post.objects.all()
    data = {'posts': posts}

    return render(request, 'blog/index.html', data)


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if request.user.is_active:      # inactive users == not logged-in users
        if request.method == "POST":
            comment_form = CommentForm(request.POST)

            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.content_object = post       # the current post being used
                comment.creator = request.user
                comment.save()
                return redirect(request.path_info)
        else:
            comment_form = CommentForm()
    else:
        comment_form = None


    params = {
        'post': post,
        'comment_form': comment_form,
        }
    return render(request, 'blog/post-detail.html', params)