from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from datetime import datetime
class UserProfile(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    # email = models.EmailField(max_length=120)
    #Manual way of doing countries

    # COUNTRY_CHOICE = [("ET", "Ethiopia"),("NZ","New Zealand"), ("US", "United States")]
    # country = models.CharField(max_length=2, choices=COUNTRY_CHOICE, default = "ET")

    # Automated way by using Django Countries module

    # from django_countries.fields import CountryField
    # country = CountryField()

    country = CountryField()

    def __str__(self):
        return "Profile of " + self.user.username


class Following(models.Model):

    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followed')

    class Meta:
        unique_together = ["follower", "followed"]

    def __str__(self):
        return f"{self.follower.username} followed {self.followed.username}"

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post_time = models.DateTimeField()
    content = models.TextField(max_length=1000)

    def __str__(self):
        return self.author.username + " | " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")