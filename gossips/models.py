from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_delete, pre_save, post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.text import slugify

from answers.models import AnswersModel


def upload_location(instance, filename, *args, **kwargs):
    file_path = 'gossips/{author_id}/{filename}'.format(author_id=str(instance.author.id), filename=filename)
    return file_path


class Tags(models.Model):
    title = models.CharField(max_length=55, unique=True)
    description = models.TextField(max_length=300, blank=True, null=True, help_text='You can optionally provide a '
                                                                                    'description for this tag')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Tags'


class GossipsModel(models.Model):
    title = models.CharField(max_length=75, unique=True, help_text='What is the title of your gossip?',
                             verbose_name='Title')
    content = models.TextField(max_length=3000)
    slug = models.SlugField(max_length=255, unique=True)
    date_published = models.DateTimeField(auto_now_add=True, verbose_name='Date Published')
    date_updated = models.DateTimeField(auto_now=True, verbose_name='Date Updated')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='gossip_author')
    image = models.ImageField(upload_to=upload_location, blank=True, null=True, help_text='Add image (optional)')
    tags = models.ManyToManyField(Tags, name='q_tags', blank=True)
    shares = models.IntegerField(default=0)
    true = models.ManyToManyField(User, related_name='true', blank=True)
    false = models.ManyToManyField(User, related_name='false', blank=True)

    def get_absolute_url(self):
        return reverse('gossips:gossip_detail', kwargs={'gossip_slug': self.slug})

    def get_delete_url(self):
        return reverse('gossips:gossip_delete', kwargs={'gossip_slug': self.slug})

    def get_update_url(self):
        return reverse('gossips:gossip_update', kwargs={'gossip_slug': self.slug})
    
    def get_total_comments(self):
        return self.comments_set.all().order_by('-date_published')

    @property
    def percent_true(self):
        true_number = int(self.true.all().count())
        false_number = int(self.false.all().count())
        total_number = true_number + false_number

        try:
            calculate = (true_number / total_number) * 100
        except ZeroDivisionError:
            calculate = 0
        return calculate

    @property
    def percent_false(self):
        true_number = int(self.true.all().count())
        false_number = int(self.false.all().count())
        total_number = true_number + false_number
        try:
            calculate = (false_number / total_number) * 100
        except ZeroDivisionError:
            calculate = 0
        return calculate

    def get_total_voters(self):
        true_number = int(self.true.all().count())
        false_number = int(self.false.all().count())
        total_voters = true_number + false_number
        return total_voters

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Gossips'


class Comments(models.Model):
    gossip = models.ForeignKey(GossipsModel, on_delete=models.CASCADE)
    content = models.TextField(max_length=300)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_author')
    date_published = models.DateTimeField(auto_now_add=True, verbose_name='Date Published')
    date_updated = models.DateTimeField(auto_now=True, verbose_name='Date Updated')

    def __str__(self):
        return f"{self.author}'s comment on {self.gossip}"

    class Meta:
        verbose_name_plural = 'Comments'


# signal that creates and saves gossips slug upon creation of a gossip
def save_gossip_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)

pre_save.connect(save_gossip_slug, sender=GossipsModel)


def save_tag_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)

pre_save.connect(save_tag_slug, sender=Tags)
