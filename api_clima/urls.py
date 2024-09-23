"""
URL configuration for api_clima project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from api import views
from api.Views import cultivo, client, user_view
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/register/', user_view.UserRegistrationView.as_view(), name='user-registration'),
    path('api/auth/login/', user_view.UserLoginView.as_view(), name='user-login'),
    path('api/auth/logout/', user_view.UserLogoutView.as_view(), name='user-logout'),
    path('users/', views.user_list),
    path('users/<int:pk>/', views.user_detail),
    path('cultivos', cultivo.cultivo_list_by_client_id),
    path('cultivos/<int:pk>/', cultivo.cultivo_detail),
    path('client/cultivos/<int:pk>/', cultivo.cultivo_list_by_client_id),
    path('client', client.ClientList.as_view()),
    path('client/<int:pk>/', client.client_detail),

]
