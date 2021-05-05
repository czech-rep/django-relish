from django import forms
from .models import *

class ImageForm(forms.ModelForm):
    
    class Meta:
        model = Image
        fields = ['title', 'image']
 


# instance
# Creating a form to change an existing article.
# >>> article = Article.objects.get(pk=1)
# >>> form = ArticleForm(instance=article)