from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse # the opposite of redirect?


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now) 
                # giving a function as default value
                # you're passing a callable to the model 
                # and it will be called each time a new instance is saved. 
                # With the parentheses, it's only being called once when models.py loads.
    author = models.ForeignKey(User, on_delete=models.CASCADE)
                # when usr is deleted, so will his posts be
                
                # i've just learned that here User object will be stored, not his id
    
    def __str__(self):
        return self.title

    # we need to tell django how to find specific post url
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
    
    