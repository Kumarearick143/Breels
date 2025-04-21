

# Create your views here.
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from data.models import Post
from .models import Like
from .forms import CommentForm



# In a helper or model method
@login_required
def follow_toggle(request, username):
    user_to_follow = get_object_or_404(User, username=username)

    if request.user == user_to_follow:
        messages.error(request, "You can't follow yourself.")
        return redirect('profile', username=username)  # early return

    if user_to_follow.profile.followers.filter(id=request.user.id).exists():
        user_to_follow.profile.followers.remove(request.user)
    else:
        user_to_follow.profile.followers.add(request.user)

    return redirect('profile', username=username)
    
    
@login_required
def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()
    return redirect(request.META.get('HTTP_REFERER', 'home'))
    
    from .forms import CommentForm
from .models import Comment

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
    return redirect(request.META.get('HTTP_REFERER', 'home'))