from django.db import models
from django.contrib.auth.models import User
import string,random
# Create your models here.
def generate_code():
    return ''.join(random.choices(string.ascii_letters+string.digits,k=6))

class ShortURL(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    original_url=models.URLField(max_length=500)
    short_code=models.CharField(max_length=10,unique=True,default=generate_code)
    created_at=models.DateTimeField(auto_now_add=True)
    clicks=models.IntegerField(default=0)

    def __str__(self):
        return f"{self.short_code}"

# class User(models.Model):
#     first_name = models.CharField(max_length=100,null=True)
#     last_name = models.CharField(max_length=100,null=True)
#     email = models.CharField(max_length=100,null=True,unique=True)
#     password = models.CharField(max_length=100)

#     def __str__(self):
#         return f"{self.first_name}  {self.last_name}"