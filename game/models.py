from email.policy import default
from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length = 30)
    city = models.CharField(max_length = 30)
    contact = models.CharField(max_length = 30)
    email = models.EmailField(unique = True)
    password = models.CharField(max_length = 50)

    def  __str__(self):
        return self.name

class Addgame(models.Model):
    title = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    description = models.TextField()
    pic = models.FileField(upload_to='blogs', default= 'blog1.jpg')
    date = models.DateTimeField(auto_now_add = True)

    def __str__(self) -> str:
        return self.title

class Donations(models.Model):
    Addgame = models.ForeignKey(Addgame, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    amount = models.FloatField(default = 0.0)

    def __str__(self) -> str:
        return self.user + ' paid to ' + self.Game

class P_game(models.Model):
    name = models.CharField(max_length = 30)
    email = models.EmailField(unique = True)
    phone = models.CharField(max_length = 30)
    city = models.CharField(max_length = 30)
    message = models.CharField(max_length = 50)
    
    def  __str__(self):
        return self.name