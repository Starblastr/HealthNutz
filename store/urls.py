from django.urls import path
from allauth.account.views import LoginView, LogoutView
from . import views
from . import product_views

urlpatterns = [
    path('', views.store, name='home'),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('accounts/signup/success', views.home, name='success'),
    path('blog/', views.blog, name='blog'),
    path('store/', views.store, name="store"),
    path('supplements/', product_views.supplements, name='supplements' ),

    path('cart/', views.cart, name="cart"),
    path('commment-pending/', views.comment_pending, name='comment_pending'),
    path('checkout/', views.checkout, name="checkout"),
    path('update_item/', views.updateItem, name='update_item'),
    path('process_order/', views.processOrder, name='process_order'),
    path('home/', views.home, name='homepage'),
    path('accounts/profile/', views.home, name='profile'),
    path('about/', views.about, name='about'),
    path('policy/', views.policy, name='policy'),
    path('contact/', views.contact, name='contact'),
path('<slug:slug>/c', product_views.SupplementDetail.as_view(), name='supplement_detail' ),
    path('<slug:slug>/a', views.post_detail, name='post_detail'),
    path('<slug:slug>/b', views.ItemDetail.as_view(), name='item_detail'),



]
