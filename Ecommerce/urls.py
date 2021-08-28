"""Ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path,include
from Ecom import views
from django.views.static import serve
from django.conf.urls import url
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home, name="home"),
    path('about/', views.about,name="about"),
    path('search', views.search_view, name='search'),
    path('add-to-cart/<int:pk>', views.add_to_cart_view, name='add-to-cart'),
    path('cart/',views.cart_view, name="cart"),
    path('remove-from-cart/<int:pk>', views.remove_from_cart_view, name='remove-from-cart'),
    path('contact/',views.contact,name="contact"),
    path("productview/<int:myid>", views.productview , name="productview"),
    path('customeraddress/', views.customer_address_view, name='customeraddress'),
    path('myorder/',views.my_order_view,name="myorder"),
    path('myprofile/', views.my_profile_view, name='myprofile'),
    path('signup',views.handleSignup,name='handleSignup'),
    path('login',views.handleLogin,name='handleLogin'),
    path('logout',views.handleLogout,name='handleLogout'),

    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),

]
