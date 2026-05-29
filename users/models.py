from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=300, blank = True)
    avatar = models.ImageField(default='avatars/default.png', upload_to='avatars/')

    def __str__(self):
        return f"{self.user.username}'s profile"

    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
        # re-size the avatar to smaller size
        if self.avatar:
            img = Image.open(self.avatar.path)
            if img.height > 200 or img.width > 200:
                output_size = (200,200)
                img.thumbnail(output_size)
                img.save(self.avatar.path)

