from django.db import models

from django.db.models.signals import pre_save, post_delete
from django.conf import settings
from django.utils.text import slugify
from django.dispatch import receiver


#define primary location for image files... 
def upload_location(instance, filename, **kwargs):
	file_path = 'blog/{author_id}/{title}-{filename}'.format(
			author_id=str(instance.author.id), title=str(instance.title), filename=filename
		)
	return file_path


class BlogPost(models.Model):
	title					= models.CharField(max_length=50, blank=True)
	body					= models.TextField(max_length=5000, blank=True)
	image					= models.ImageField(upload_to=upload_location, blank=True)
	date_published			= models.DateTimeField(auto_now_add=True, verbose_name="date published")
	date_updated			= models.DateTimeField(auto_now=True, verbose_name="date updated")
	author					= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='author')
	slug					= models.SlugField(blank=True, unique=True)
	likes					= models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='blog_posts')

	def __str__(self):
		return self.title

	@property
	def num_likes(self):
		return self.likes.all().count()


#If user deletes BLogPost then also delete image from db. 
@receiver(post_delete, sender=BlogPost)
def submission_delete(sender, instance, **kwargs):
	instance.image.delete(False)


#Checks if Blog is Unique and has a unique username.
def pre_save_blog_post_reciever(sender, instance, **kwargs):
	if not instance.slug:
		instance.slug = slugify(instance.author.username + "-" + instance.title)

#calls this before saving blog..
pre_save.connect(pre_save_blog_post_reciever, sender=BlogPost)




LIKE_CHOICES = {
	('Like', 'Like'),
	('Unlike', 'Unlike'),
}


class Like(models.Model):
	user 					= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	blog 					= models.ForeignKey(BlogPost, on_delete=models.CASCADE)
	value					= models.CharField(choices=LIKE_CHOICES, default='Like', max_length=10)


	def __str__(self):
		return str(self.blog)