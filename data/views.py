from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm
from interaction.models import PostView
from .models import Product  # you'll need to define this model if not already done
from .forms import ProductForm  # we'll define this form below





@login_required
def home(request):
    user = request.user
    seen_post_ids = request.session.get('seen_posts', [])

    fresh_posts = Post.objects.exclude(id__in=seen_post_ids).order_by('-created_at')[:10]

    # Update session with newly seen post IDs
    request.session['seen_posts'] = seen_post_ids + [post.id for post in fresh_posts]

    return render(request, 'main/home.html', {'posts': fresh_posts})
    
@login_required
def dashboard(request):
    posts = Post.objects.filter(author=request.user)
    return render(request, 'user/dashboard.html', {'posts': posts})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('dashboard')
    else:
        form = PostForm()
    return render(request, 'user/create_post.html', {'form': form})

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = PostForm(instance=post)
    return render(request, 'user/edit_post.html', {'form': form})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if request.method == 'POST':
        post.delete()
        return redirect('dashboard')
    return render(request, 'user/delete_post.html', {'post': post})
    
    
    from interaction.models import PostView

def home(request):
    posts = Post.objects.all().order_by('-created_at')
    if request.user.is_authenticated:
        for post in posts:
            PostView.objects.get_or_create(user=request.user, post=post)
    return render(request, 'main/home.html', {'posts': posts})
    
    
  

def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            return redirect('dashboard')
        else:
            print(form.errors)  # Optional: log errors
    else:
        form = ProductForm()
    
    return render(request, 'user/create_product.html', {'form': form})