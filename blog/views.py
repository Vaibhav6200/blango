from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post


# Create your views here.
def index(request):
    posts = Post.objects.filter(published_at__lte = timezone.now())
    # posts = Post.objects.all()
    data = {'posts': posts}

    return render(request, 'blog/index.html', data)


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'blog/post-detail.html', {'post': post})