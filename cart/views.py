from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from data.models import Post
from .models import CartItem






@login_required
def add_to_cart(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Optional: check if the post has an associated product
    if not hasattr(post, 'product'):
        return redirect('home')  # or show an error message

    CartItem.objects.get_or_create(user=request.user, post=post)
    return redirect('view_cart')  # Adjust this if your cart view has a different name


@login_required
def remove_from_cart(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    CartItem.objects.filter(user=request.user, post=post).delete()
    return redirect('view_cart')

@login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user).select_related('post')
    return render(request, 'cart/view_cart.html', {'cart_items': cart_items})