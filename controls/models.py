from django.db import models
from django.db.models.signals import post_save

from gossips.models import GossipsModel
from cheaters.models import CheatersModel


class FalseInformation(models.Model):
   gossip = models.ForeignKey(GossipsModel, on_delete=models.CASCADE, related_name='false_gossip', null=True, blank=True)
   cheater = models.ForeignKey(CheatersModel, on_delete=models.CASCADE, related_name='false_cheater', null=True, blank=True)
   section = models.CharField(max_length=255)
   date_published = models.DateTimeField(auto_now_add=True, verbose_name='Date Published')
   date_updated = models.DateTimeField(auto_now=True, verbose_name='Date Updated')

   def __str__(self):
      return f"{self.gossip if self.gossip else self.cheater}"
    

# signal that calculates whether a gossip should be added to false information section or not
def gossip_false_information(sender, instance, *args, **kwargs):
   total_votes = instance.true.all().count() + instance.false.all().count()
   if total_votes >= 3:
      percent_false = instance.percent_false
      if int(percent_false) >= 51:
         if not FalseInformation.objects.filter(gossip__title=instance.title).exists():
            FalseInformation.objects.create(gossip=instance, section='gossip')
      else:
         if FalseInformation.objects.filter(gossip__title=instance.title).exists():
            FalseInformation.objects.get(gossip__title=instance.title).delete()
   else:
      print('NEGATIVE')

post_save.connect(gossip_false_information, sender=GossipsModel)


# signal that calculates whether a cheater should be added to false information section or not
def cheater_false_information(sender, instance, *args, **kwargs):
   total_votes = instance.true.all().count() + instance.false.all().count()
   if total_votes >= 3:
      percent_false = instance.percent_false
      if int(percent_false) >= 51:
         if not FalseInformation.objects.filter(cheater__title=instance.title).exists():
            FalseInformation.objects.create(cheater=instance, section='cheater')
      else:
         if FalseInformation.objects.filter(cheater__title=instance.title).exists():
            FalseInformation.objects.get(cheater__title=instance.title).delete()
   else:
      print('NEGATIVE')

post_save.connect(cheater_false_information, sender=CheatersModel)



