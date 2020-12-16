from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.urls import reverse


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='profile.jpg', upload_to='profile_pics')
    bio = models.TextField(max_length=655, null=True, blank=True)
    followers = models.ManyToManyField(User, related_name='followers')
    following = models.ManyToManyField(User, related_name='following')
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} profile"

    # def save(self):
    #     super().save()
    #
    #     img = Image.open(self.image.path)
    #     if img.height > 200 or img.width > 200:
    #         output = (150, 150)
    #         img.thumbnail(output)
    #         img.save(self.image.path)

    # setting a redirect url after post/profile has been created (classed based view)
    # def get_absolute_url(self):
    #     return reverse('post-view', kwargs={'pk': self.pk})
    #
    # def get_delete_url(self):
    #     return reverse('post-view', kwargs={'pk': self.pk})
    #
    # def get_update_url(self):
    #     return reverse('post-view', kwargs={'pk': self.pk})
