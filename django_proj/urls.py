"""django_proj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

from users import views as user_views # users app
from blog.views import error_page as error_page

urlpatterns = [
    path('meme/', include('meme_sorter.urls')), # included my new app

    path('admin/', admin.site.urls),
    path('register/', user_views.register, name='register'),

    path('', include('blog.urls')), # brings us to blog app / urls
    # path('blog/', include('blog.urls')),

 # REST FRAMEWORK :
    path('api/', include('api.urls')), # 


    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('profile/', user_views.profile, name='profile'),
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='users/password_reset.html'
        ), name='password_reset'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view()
        , name='password_reset_confirm'),
    path('password_reset/done', auth_views.PasswordResetDoneView.as_view(
            template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('password-reset_complete', auth_views.PasswordResetCompleteView.as_view()
        , name='password_reset_complete')


        
    # error page - for all apps
    , path("error/<str:err_msg>", error_page, name='error_page') # imported from users.views
]
#           url,        view function,                      name - to call by redirect

# this is about serving user media files during development
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # thats for files
