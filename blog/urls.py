from django.urls import path
from . import views
from django.http import HttpResponse

urlpatterns = [
    path('posts/', views.home, name='blog-home') # left for fun
    , path('name/', views.name, name='blog-name')
    , path('about/', views.about, name='blog-about')

    , path('', views.PostListView.as_view(), name='posts')
    , path('user/<str:username>', views.UserPostListView.as_view(), name='user-posts')
        # here we use class view, it needs method as_view()
        # he automaticly looks for template blog/post_list.html
        # means <app>/<model>_<viewtype>.html 
    , path('post/<int:pk>/', views.PostDetailView.as_view(), name='post-detail') # pk = primary key
    , path('post/new/', views.PostCreateView.as_view(), name='post-create')
    , path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post-update')
    , path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete')

    , path('user-information/', views.user_data, name='user-info')
    , path("latest_post_info/", views.last_posted)
    , path("post_nr/<int:post_id>", views.post_by_id)           # tak jakby rest api
    , path("post_post/", views.post_post)
    , path("add_post_ex/", views.add_post_ex)
    , path("post_stack/", views.posting_stack)


]