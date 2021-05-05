from django.contrib import admin

# Register your models here.
# okay: then:

from .models import Post

admin.site.register(Post) # << pass in the Post model