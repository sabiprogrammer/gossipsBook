from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.text import slugify


def upload_location(instance, filename, *args, **kwargs):
    file_path = 'cheaters/{author_id}/{filename}'.format(author_id=str(instance.author.id), filename=filename)
    return file_path


class Tags(models.Model):
    title = models.CharField(max_length=55, unique=True)
    description = models.TextField(max_length=300, blank=True, null=True, help_text='You can optionally provide a '
                                                                                    'description for this tag')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Tags'


class CheatersModel(models.Model):
    title = models.CharField(max_length=75, unique=True, help_text='What is the title of your cheater story?',
                             verbose_name='Title', null=False, blank=False)
    content = models.TextField(max_length=3000, null=False, blank=False)
    slug = models.SlugField(unique=True)
    date_published = models.DateTimeField(auto_now_add=True, verbose_name='Date Published')
    date_updated = models.DateTimeField(auto_now=True, verbose_name='Date Updated')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cheater_author')
    image = models.ImageField(upload_to=upload_location, default='', help_text='Add image (Mandatory)', null=False, blank=False)
    tags = models.ManyToManyField(Tags, name='q_tags', blank=True)
    shares = models.IntegerField(default=0)
    true = models.ManyToManyField(User, related_name='cheater_true', blank=True)
    false = models.ManyToManyField(User, related_name='cheater_false', blank=True)

    def get_absolute_url(self):
        return reverse('cheaters:cheater_detail', kwargs={'cheater_slug': self.slug})

    def get_delete_url(self):
        return reverse('cheaters:cheater_delete', kwargs={'cheater_slug': self.slug})

    def get_update_url(self):
        return reverse('cheaters:cheater_update', kwargs={'cheater_slug': self.slug})

    def percent_true(self):
        true_number = int(self.true.all().count())
        false_number = int(self.false.all().count())
        total_number = true_number + false_number

        try:
            calculate = (true_number / total_number) * 100
        except ZeroDivisionError:
            calculate = 0
        return calculate

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
        verbose_name_plural = 'Cheaters'


class Comments(models.Model):
    cheater = models.ForeignKey(CheatersModel, on_delete=models.CASCADE)
    content = models.TextField(max_length=500)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cheater_comment_author')
    date_published = models.DateTimeField(auto_now_add=True, verbose_name='Date Published')
    date_updated = models.DateTimeField(auto_now=True, verbose_name='Date Updated')

    def __str__(self):
        return f"{self.author}'s comment on {self.cheater}"

    class Meta:
        verbose_name_plural = 'Comments'


def save_cheater_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)


pre_save.connect(save_cheater_slug, sender=CheatersModel)


def save_tag_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)


pre_save.connect(save_tag_slug, sender=Tags)
