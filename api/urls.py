from django.urls import include, path
from rest_framework import routers
from . import views



router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

# wire up API using automatic URL routeing
urlpatterns = [
    path('', include(router.urls))
    , path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]


from django.urls import path

urlpatterns += [
    path('post_id/<id>/', views.api_detail_blog_view, name='detail')
]