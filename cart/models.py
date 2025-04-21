

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from data.models import Post  # assuming posts are in 'data' app

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')  # prevent duplicate items

    def __str__(self):
        return f"{self.user.username} - {self.post.title}"
        
        
        
  