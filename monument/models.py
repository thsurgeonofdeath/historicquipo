from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.conf import settings
from django.db.models.signals import post_delete
from django.dispatch import receiver
from account.models import Account

def upload_location(instance, filename, **kwargs):
	file_path = 'monument/{title}-{filename}'.format(
				title=str(instance.title), filename=filename)
	return file_path

class Monument(models.Model):
	#attributes
	title 					= models.CharField(max_length=50, null=False, blank=False)
	description 			= models.TextField(max_length=10000, null=False, blank=False)
	image		 			= models.ImageField(upload_to=upload_location, null=True, blank=True)
	year					= models.CharField(max_length=50, null=False, blank=True)
	latitude				= models.FloatField(null=False, blank=True, default=0)
	longitude				= models.FloatField(null=False, blank=True, default=0)
	city					= models.CharField(max_length=50, null=True, blank=True, default="Casablanca")

	#to generate custom links for each monument
	slug 					= models.SlugField(blank=True, unique=True)

	#for the "saved" feature
	saved = models.ManyToManyField(Account, default=None, blank=True)

	def __str__(self):
		return self.title

	@property
	def imageURL(self):
		try:
			url = self.image.url
		except:
			url = ''
		return url 



@receiver(post_delete, sender=Monument)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False) 


def pre_save_monument_receiver(sender, instance, *args,**kwargs):
	if not instance.slug:
		instance.slug = slugify(instance.title)

pre_save.connect(pre_save_monument_receiver, sender=Monument)


