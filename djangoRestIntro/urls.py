"""
URL configuration for djangoRestIntro project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from .views import users_crude, users, get_or_replace_or_update_or_delete_user
from .views import UserListCreateAPIView, UserRetrieveUpdateDestroyAPIView
from .views import UserAPIView, UserGetReplaceUpdateDeleteAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    # function views: v1
    path('users/crude', users_crude),
    path('users', users),
    path('users/<int:id>', get_or_replace_or_update_or_delete_user),
    # class views: v2
    path('users/class', UserListCreateAPIView.as_view()),
    path('users/class/<int:id>', UserRetrieveUpdateDestroyAPIView.as_view()),
    # class views: v3
    path('users/api', UserAPIView.as_view()),
    path('users/api/<int:id>', UserGetReplaceUpdateDeleteAPIView.as_view()),

]
