from rest_framework import serializers
from app_store.models import Category, Joyas, CartItems, ProductosCompra, Compra
from django.contrib.auth import get_user_model

User = get_user_model()

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["name"]

class JoyasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Joyas
        fields = "__all__"

class CartItemSerializer(serializers.ModelSerializer):
    product = JoyasSerializer(read_only=True)

    class Meta:
        model = CartItems
        fields = ["id", "product", "quantity"]

class ProductosCompraSerializer(serializers.ModelSerializer):
    product = JoyasSerializer(read_only=True)
    product_price = serializers.DecimalField(read_only=True, max_digits=10, decimal_places=2)
    total_price = serializers.DecimalField(read_only=True, max_digits=12, decimal_places=2)

    class Meta:
        model = ProductosCompra
        fields = ["product", "product_price", "quantity", "total_price"]

class CompraSerializer(serializers.ModelSerializer):
    products = ProductosCompraSerializer(many=True, read_only=True)

    class Meta:
        model = Compra
        fields = ["id", "user_email", "products"]

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "username", "password"]

    def create(self, validated_data):
        user = User(
            email=validated_data["email"],
            username=validated_data["username"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user

        user = User.objects.create_user(
            email=validated_data["email"],
            username=validated_data["username"],
            password=validated_data["password"],
        )
        return user