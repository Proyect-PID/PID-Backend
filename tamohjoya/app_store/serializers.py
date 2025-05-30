from rest_framework import serializers
from app_store.models import Category, Joyas, Cart, CartItems

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=["name"]

class JoyasSerializer(serializers.ModelSerializer):
    class Meta:
        model=Joyas
        fields='__all__'

class CartItemSerializer(serializers.ModelSerializer):
    product=JoyasSerializer(read_only=True)
    class Meta:
        model=CartItems
        fields=['id',"product","quantity"]

class CartSerializer(serializers.ModelSerializer):
    products=JoyasSerializer(read_only=True)
    #products=CartItemSerializer(many=True, read_only=True)
    class Meta:
        model=Cart
        fields=['products']