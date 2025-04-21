

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile
from main.models import Post
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

@login_required
def dashboard(request):
    posts = Post.objects.filter(author=request.user)
    return render(request, 'user/dashboard.html', {'posts': posts})


@login_required
def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=profile_user)
    posts = Post.objects.filter(author=profile_user).order_by('-created_at')  # Get user's posts

    is_following = False
    if request.user.is_authenticated and request.user != profile_user:
        is_following = profile.followers.filter(id=request.user.id).exists()

    return render(request, 'user/profile.html', {
        'profile_user': profile_user,
        'profile': profile,
        'posts': posts,
        'is_following': is_following,
    })




@login_required
def profile_counts(request, username):
    user = get_object_or_404(User, username=username)
    profile = user.profile
    post_count = Post.objects.filter(author=user).count()
    follower_count = profile.followers.count()
    following_count = user.following.count()

    return JsonResponse({
        'posts': post_count,
        'followers': follower_count,
        'following': following_count
    })


@login_required
def follow_toggle(request, username):
    target = get_object_or_404(User, username=username)
    profile = target.profile
    if request.user in profile.followers.all():
        profile.followers.remove(request.user)
    else:
        profile.followers.add(request.user)
    return redirect('profile', username=username)
   

@login_required
def edit_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile', username=request.user.username)
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'user/edit_profile.html', {'form': form})