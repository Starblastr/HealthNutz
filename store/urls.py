from django.urls import path
from allauth.account.views import LoginView, LogoutView
from . import views


urlpatterns = [
    path('', views.store, name='home'),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('accounts/signup/success', views.home, name='success'),
    path('store/', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('blog/', views.blog, name='blog'),
    path('checkout/', views.checkout, name="checkout"),
    path('update_item/', views.updateItem, name='update_item'),
    path('process_order/', views.processOrder, name='process_order'),
    path('home/', views.home, name='homepage'),
    path('accounts/profile/', views.home, name='profile'),
    path('about/', views.about, name='about'),
    path('policy/', views.policy, name='policy'),
    path('contact/', views.contact, name='contact'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
    path('<slug:slug>/', views.ItemDetail.as_view(), name='item_detail'),


]
