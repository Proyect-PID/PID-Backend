<<<<<<< HEAD
from django.urls import path
from app_store.views import (
    CategoryListView,
    test,
    JoyasListView,
    CartListView,
    AddCartView,
    DeleteCartView,
    CheckoutView,
    UserRegisterView,
    TopProductosView,
    CustomTokenObtainPairView,
    
)
from rest_framework_simplejwt.views import TokenRefreshView
from app_store.views import LogoutView

urlpatterns = [
    path("test/", test, name="test"),
    path("category/", CategoryListView.as_view(), name="category"),
    path("joyas/<str:name>/", JoyasListView.as_view(), name="joyas"),
    path("top-productos/", TopProductosView.as_view(), name="top-productos"),
    path("cart/", CartListView.as_view(), name="cart"),
    path("cart/<int:pk>/add/", AddCartView.as_view(), name="add-cart"),
    path("cart/<int:cart_item_id>/delete/", DeleteCartView.as_view(), name="delete-cart"),
    path("login/", CustomTokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("register/", UserRegisterView.as_view(), name="register"),
    path('logout/', LogoutView.as_view(), name='logout'),
]
=======
from django.urls import path 
from app_store.views import CategoryListView, test, JoyasListView, CartListView, AddCartView, DeleteCartView,registro_usuario
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns=[
    path('test/',test, name="test"),
    path('registro/', registro_usuario, name='registro_usuario'),
    path('category/',CategoryListView.as_view(), name= "category"),
    path('joyas/<str:name>/',JoyasListView.as_view(), name= "joyas"),
    path('cart/',CartListView.as_view(), name='cart'),
    path('cart/<int:pk>/add/',AddCartView.as_view(), name='add-cart'),
    path('cart/<int:cart_item_id>/delete/',DeleteCartView.as_view(), name='delete-cart'),
    path('login/', TokenObtainPairView.as_view(),name='login'),
    path('token/refresh/', TokenRefreshView.as_view(),name='token-refresh'),
    ]
>>>>>>> f178f8fd08913765764eddce8da2d44fb90ae9b0
