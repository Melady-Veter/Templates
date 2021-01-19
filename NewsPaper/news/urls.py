from django.contrib import admin
from django.urls import path, include
from .views import PostList, PostDetail


urlpatterns = [
    path('admin', admin.site.urls),
    path('pages', include('django.contrib.flatpages.urls')),
    path('',PostList.as_view()),
    path('<int:pk>', PostDetail.as_view()),
]