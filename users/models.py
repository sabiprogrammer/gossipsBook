from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from PIL import Image
from django.urls import reverse


def upload_location(instance, filename, *args, **kwargs):
    file_path = 'profile/{author_id}/{filename}'.format(author_id=str(instance.user.id), filename=filename)
    return file_path


class Interests(models.Model):
    title = models.CharField(max_length=75, unique=True)
    description = models.TextField(max_length=300, blank=True, null=True, help_text='You can optionally provide a '
                                                                                    'description for this interest')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Interests'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default_profile_pic2.png', upload_to=upload_location, blank=True)
    bio = models.TextField(max_length=455, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    interests = models.ManyToManyField(Interests, related_name='interests', blank=True)
    followers = models.ManyToManyField(User, related_name='followers', blank=True)
    following = models.ManyToManyField(User, related_name='following', blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

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


def user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


post_save.connect(user_profile, sender=User)


@receiver(post_delete, sender=Profile)
def delete_image(sender, instance, *args, **kwargs):
    instance.image.delete(False)

# @receiver(post_delete, sender=User)
# def delete_profile(sender, instance, *args, **kwargs):
#     print('user: ', user)
#     user.delete(False)
