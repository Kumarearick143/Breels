from django.shortcuts import render
from django.contrib.auth.models import User
from data.models import Post
from django.db.models import Q

def search(request):
    query = request.GET.get('q', '')
    users = User.objects.filter(username__icontains=query)
    posts = Post.objects.filter(
        Q(title__icontains=query) |
        Q(content__icontains=query)
    )
    return render(request, 'search/results.html', {
        'query': query,
        'users': users,
        'posts': posts
    })