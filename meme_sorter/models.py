from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User

class TagName(models.Model):
    name = models.CharField(max_length=50)      # make that unique
    children = models.IntegerField(default=0) # carries information about number tag is used

    def __str__(self):
        return self.name


class Image(models.Model):
    title = models.CharField(max_length=60)
    image = models.ImageField(upload_to='meme_warehouse/') # {{ object.image.url }} - stores image's path
    # upload to - string value will be appended to your MEDIA_ROOT path
    resized_image = models.ImageField(upload_to='resizing/', blank=True)
    
    # date_added = models.DateTimeField(default=timezone.now)
    # tags = models.JSONField(default=list) # here json array with pk of tags
    tags = models.ManyToManyField(TagName)
    added_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def add_tag(self, tag_pk):
        # metoda wywoływana po sprawdzeniu czy tag istnieje
        # lub po utworzeniu. w każdym razie nie martwimy się o to w tym module
        # tag_pk<int> -- TagName.id
        self.tags.add(tag_pk) # we add to many to many field
            # .add() method accepts object or its id
        # Note that add(), create(), remove(), clear(), and set() all apply database changes 
        # immediately for all types of related fields. In other words, 
        # there is no need to call save() on either end of the relationship

        tag = TagName.objects.get(id=tag_pk) # tag object we have
        tag.children += 1
        tag.save()

    def remove_tag(self, tag_pk):
        self.tags.remove(tag_pk)
        tag = TagName.objects.get(id=tag_pk) # tag object we have
        count = tag.children
        if count < 2:
            tag.delete()
        else:
            tag.children -= 1
            tag.save()
