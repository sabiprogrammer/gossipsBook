from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.text import slugify


def upload_location(instance, filename, *args, **kwargs):
    file_path = 'questions/{author_id}/{filename}'.format(author_id=str(instance.author.id), filename=filename)
    return file_path


class Tags(models.Model):
    content = models.TextField(max_length=3000)
    slug = models.SlugField(unique=True)


class User(models.Model):
    content = models.TextField(max_length=3000)
    slug = models.SlugField(unique=True)


class Questions(models.Model):
    title = models.CharField(max_length=100, unique=True, help_text='What is the title of your question?', verbose_name='Title')
    content = models.TextField(max_length=3000)
    slug = models.SlugField(unique=True)
    date_published = models.DateTimeField(auto_now_add=True, verbose_name='Date Published')
    date_updated = models.DateTimeField(auto_now=True, verbose_name='Date Updated')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    image = models.ImageField(upload_to=upload_location, blank=True, null=True)
    tags = models.ManyToManyField(Tags, name='q_tags')
    votes = models.ManyToManyField(User, related_name='votes')

    def get_absolute_url(self):
        return reverse('questions:question_detail', kwargs={'question': self.slug})

    def get_delete_url(self):
        return reverse('questions:question_delete', kwargs={'question': self.slug})

    def get_update_url(self):
        return reverse('questions:question_update', kwargs={'question': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Questions'


@receiver(post_delete, sender=Questions)
def delete_image(sender, instance, *args, **kwargs):
    instance.image.delete(False)


def save_question_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)


pre_save.connect(save_question_slug, sender=Questions)

