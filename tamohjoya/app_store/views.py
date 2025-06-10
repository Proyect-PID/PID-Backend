<<<<<<< HEAD
from django.shortcuts import HttpResponse
from django.db.models import Sum, Value
from django.db.models.functions import Coalesce
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated 
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView
from rest_framework import status, serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from app_store.models import Category, Joyas, Cart, CartItems, Compra, ProductosCompra
from app_store.serializers import (
    CategorySerializer,
    JoyasSerializer,
    CartItemSerializer,
    ProductosCompraSerializer,
    CompraSerializer,
    UserRegisterSerializer,
)

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()
=======
from django.shortcuts import render, HttpResponse, redirect
from app_store.serializers import CategorySerializer, JoyasSerializer, CartItemSerializer, CartSerializer
from app_store.models import Category, Joyas, Cart, CartItems, Compra, ProductosCompra
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .forms import RegistroUsuarioForm
>>>>>>> f178f8fd08913765764eddce8da2d44fb90ae9b0

def test(request):
    print("hola mundo")
    return HttpResponse("Hola Mundo")

<<<<<<< HEAD
# JWT login personalizado que acepta username o email
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'username'  # campo para login, puede ser username o email

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError("Credenciales incorrectas")
        else:
            raise serializers.ValidationError("Se requieren username y password")

        data = super().validate(attrs)
        data['user'] = {
            "id": self.user.id,
            "username": self.user.username,
            "email": self.user.email,
        }
        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# Vistas públicas (sin autenticación)
=======
def registro_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()  
            return redirect('login') 
    else:
        form = RegistroUsuarioForm()
    return render(request, 'registro.html', {'form': form})

>>>>>>> f178f8fd08913765764eddce8da2d44fb90ae9b0
class CategoryListView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class JoyasListView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = JoyasSerializer

    def get_queryset(self):
        category_name = self.kwargs["name"]
        category = Category.objects.filter(name__iexact=category_name).first()
        queryset = Joyas.objects.filter(available=True, category=category).all()
        return queryset

# Vista para los 8 productos más vendidos con descripción
class TopProductosView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        joyas = Joyas.objects.annotate(
            total_vendido=Coalesce(
                Sum('productoscompra__quantity'),
                Value(0)
            )
        ).order_by('-total_vendido')[:8]

        resultado = []
        for joya in joyas:
            resultado.append({
                'id': joya.id,
                'name': joya.name,
                'description': joya.description,
                'image': joya.image.url if joya.image else '',
                'price': float(joya.price),
                'total_vendido': joya.total_vendido,
            })

        return Response(resultado)

# Vistas protegidas (requieren autenticación JWT)
class CartListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartItemSerializer

    def get_queryset(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        queryset = CartItems.objects.filter(cart=cart).all()
        return queryset

class AddCartView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartItemSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        product_id = kwargs.get("pk")

        try:
            product = Joyas.objects.get(id=product_id, available=True)
        except Joyas.DoesNotExist:
            return Response({"error": "No existe el producto"}, status=404)

        try:
            quantity = int(request.data.get("quantity", 1))
        except (TypeError, ValueError):
            return Response({"error": "Cantidad inválida"}, status=400)

        if quantity <= 0:
            return Response({"error": "La cantidad debe ser mayor que cero"}, status=400)

        if product.stock == 0:
            return Response({"error": "Producto sin stock disponible"}, status=400)

        cart, created = Cart.objects.get_or_create(user=user)
        cart_item, created = CartItems.objects.get_or_create(cart=cart, product=product)

        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity

        if cart_item.quantity > product.stock:
            cart_item.quantity = product.stock

        cart_item.save()

        return Response(CartItemSerializer(cart_item).data, status=201)

class DeleteCartView(DestroyAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        cart, created = Cart.objects.get_or_create(user=user)
        cart_items = CartItems.objects.filter(cart=cart).all()
        return cart_items

    def delete(self, request, *args, **kwargs):
        try:
            cart_item = CartItems.objects.get(
                id=kwargs["cart_item_id"], cart__user=request.user
            )
            cart_item.delete()
            return Response({"status": "Producto eliminado"}, status=204)
        except CartItems.DoesNotExist:
            return Response(
                {"error": "El producto no existe en el carrito"}, status=404
            )

class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        cart, created = Cart.objects.get_or_create(user=user)
        cart_items = CartItems.objects.filter(cart=cart)

        if not cart_items.exists():
            return Response(
                {"error": "El carrito está vacío"}, status=status.HTTP_400_BAD_REQUEST
            )

        errores = []
        for item in cart_items:
            if item.quantity > item.product.stock:
                errores.append({
                    "product": item.product.name,
                    "requested": item.quantity,
                    "available": item.product.stock,
                    "error": f"No hay suficiente stock de {item.product.name}. Solo quedan {item.product.stock}."
                })

        if errores:
            return Response(
                {"error": "Stock insuficiente para uno o más productos", "detalles": errores},
                status=status.HTTP_400_BAD_REQUEST
            )

        compra = Compra.objects.create(user_email=user.email, user=user)
        for item in cart_items:
            ProductosCompra.create_or_update(
                compra=compra,
                product=item.product,
                quantity=item.quantity,
            )
            item.product.stock -= item.quantity
            item.product.save()

        cart_items.delete()

        return Response(
            {"status": "Compra realizada con éxito"}, status=status.HTTP_201_CREATED
        )

class UserRegisterView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegisterSerializer

    permission_classes = [AllowAny]
    serializer_class = UserRegisterSerializer
    
    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Logout exitoso"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": "Token inválido o expirado"}, status=status.HTTP_400_BAD_REQUEST)    