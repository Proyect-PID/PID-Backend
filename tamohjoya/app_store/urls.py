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