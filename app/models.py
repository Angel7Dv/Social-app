from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.



#    User:  
#    username 
#    first_name
#    last_name 
#    email 
#    user = foreikey(Profile)
#    post = foreikey(Posts)



class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	bio = models.CharField(default='Hola, twitter', max_length=100)
	image = models.ImageField(default='default.png')
	def __str__(self):
		return f'Perfil de {self.user.username}'
    # campos foraneos
    # user.posts

	def following(self):
		user_ids = Relationship.objects.filter(from_user=self.user)\
									.values_list('to_user_id', flat=True)
		return User.objects.filter(id__in=user_ids)

	def followers(self):
		user_ids = Relationship.objects.filter(to_user=self.user)\
									.values_list('from_user_id', flat=True)
		return User.objects.filter(id__in=user_ids)


class Post(models.Model):
	timestamp = models.DateTimeField(default=timezone.now)
	content = models.TextField()
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')

	class Meta:
		ordering = ['-timestamp']

	def __str__(self):
		return self.content


class Relationship(models.Model):
	# Deberia ser oneToMany por que se puede seguir todas las veces que se quiera
	from_user = models.ForeignKey(User, related_name='relationships', on_delete=models.CASCADE) 
	to_user = models.ForeignKey(User, related_name='related_to', on_delete=models.CASCADE)

	def __str__(self):
		return f'{self.from_user} to {self.to_user}'