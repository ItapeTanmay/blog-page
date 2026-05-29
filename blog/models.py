from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse

class Post(models.Model):
    CATEGORY_CHOICES = [
        ('tech','Technology'),
        ('lifestyle','Lifestyle'),
        ('travel','Travel'),
        ('food','Food'),
        ('other','Other'),
    ]

    title = models.CharField(max_length = 200)
    slug = models.SlugField(max_length = 200, unique = True, blank = True)
    body = models.TextField()
    author = models.ForeignKey(User, on_delete = models.CASCADE, related_name='posts')
    category = models.CharField(max_length=20, choices = CATEGORY_CHOICES, default='other')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={"slug": self.slug})


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name = 'likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user','post']  # one like per uer per post

    def __str__(self):
        return f"{self.user.username} likes {self.post.title}"

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']     # oldest first for natural reading

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"














































