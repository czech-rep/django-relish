from django.db import models
# we'll extend build in User model provided by Django. lets import:
from django.contrib.auth.models import User

# from django import forms
# class User(User):
#     rozmiar_buta = forms.CharField(required=False)
# na później - dodaj pole do Usera modela

# we'll build a table profiles with one2one relation to users

from PIL import Image
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
        # CASCADE = one deleted makes other deleted too
        # one way
    image = models.ImageField(default='profile_pics/default.jpg', upload_to='profile_pics') 
        # specifies folder for picks

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            if img.height >= img.width:
                new_height = 300
                new_width = img.width / img.height * 300
            else:
                new_width = 300
                new_height = img.height / img.width * 300

            output_size = (new_height, new_width)
            img.thumbnail(output_size)
            img.save(self.image.path)

        # so, here we overwritted save method. First we save image, next we resize IT