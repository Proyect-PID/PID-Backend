from django.shortcuts import render, HttpResponse, redirect
from app_store.serializers import CategorySerializer, JoyasSerializer, CartItemSerializer, CartSerializer
from app_store.models import Category, Joyas, Cart, CartItems, Compra, ProductosCompra
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .forms import RegistroUsuarioForm

def test(request):
    print("hola mundo")
    return HttpResponse("Hola Mundo")

def registro_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()  
            return redirect('login') 
    else:
        form = RegistroUsuarioForm()
    return render(request, 'registro.html', {'form': form})

class CategoryListView(ListAPIView):
    queryset=Category.objects.all()
    serializer_class=CategorySerializer

class JoyasListView(ListAPIView):
    
    serializer_class=JoyasSerializer

    def get_queryset(self):
        category_name=self.kwargs['name']
        category=Category.objects.filter(name__iexact=category_name).first()
        queryset=Joyas.objects.filter(available=True,category=category).all()
        return queryset
    
class CartListView(ListAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=CartItemSerializer

    def get_queryset(self):
        cart, created=Cart.objects.get_or_create(user=self.request.user)
        queryset=CartItems.objects.filter(cart=cart).all()
        print(queryset)
        return queryset
    
class AddCartView(CreateAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=CartItemSerializer
    
    def create(self, request, *args, **kwargs):
        user=request.user
        product_id=kwargs.get("pk")
        try:
            product = Joyas.objects.get(id=product_id, available=True)
        except Joyas.DoesNotExist:
            return Response({'error':'No existe el producto'}, status=404)
        
        quantity=int(self.request.data.get('quantity', product.stock))
        if quantity<=0 or product.stock==0:
            return Response({'error':"La cantidad no es valida"}, status=400)

        if quantity>product.stock:
            quantity=product.stock
        
        cart, created=Cart.objects.get_or_create(user=user)

        cart_item, created= CartItems.objects.get_or_create(cart=cart, product=product)
        cart_item.quantity=quantity
        cart_item.save()

        return Response(CartItemSerializer(cart_item).data, status=201)
    
class DeleteCartView(DestroyAPIView):
    serializer_class=CartItemSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        user=self.request.user
        cart, created= Cart.objects.get_or_create(user=user)
        cart_items=CartItems.objects.filter(cart=cart).all()
        return cart_items
    
    def delete(self, request, *args, **kwargs):
        try:
            cart_item=CartItems.objects.get(id=kwargs['cart_item_id'])
            cart_item.delete()
            return Response({'status':'Producto eliminado'}, status=204)
        except CartItems.DoesNotExist:
            return Response({'error':'El producto no existe en el carrito'}, status=404)