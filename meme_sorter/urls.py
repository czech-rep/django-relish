from django.urls import path, include
from . import views

# app_name = 'meme_sorter'


urlpatterns = [
    path('', views.hello, name='hello')
    , path('index/', views.index, name='index')
    , path('tag/<str:tag_name>', views.tag, name='tag_name')

    , path('add_by_form/', views.post_image_form, name='post_image_form')
    , path('details/<int:img_id>', views.image_details, name='image_details')
    , path('resize/<int:img_id>', views.image_resize, name='image_resize')

    , path('add_chosen_tag/<int:img_id>/<int:tag_pk>/<str:action>', views.add_chosen_tag, name='add_chosen_tag')
    , path('delete/<int:img_id>', views.delete_image, name='delete_image')

    # nieużywane
    #niby rest:
    , path('count_memes/<str:tag_name>', views.count_memes, name='count_memes')
    #przegląd tagów
    # , path('tags', views.tags, name='tags')
]

