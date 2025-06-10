from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.conf import settings
class UserManager(BaseUserManager):

    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('El usuario debe tener un correo electrónico')
        if not username:
            raise ValueError('El usuario debe tener un nombre de usuario')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('El superusuario debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('El superusuario debe tener is_superuser=True.')

        return self.create_user(email, username, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(verbose_name="Nombre de Usuario", max_length=25, unique=True)
    email = models.EmailField(verbose_name="Correo", max_length=255, unique=True)
    is_staff = models.BooleanField(verbose_name="staff", default=False)
    is_superuser = models.BooleanField(verbose_name="superuser", default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    objects = UserManager()

class Category(models.Model):
    name = models.CharField(verbose_name="Nombre", unique=True)

    def __str__(self):
        return self.name
    
    def clean(self):
        self.name = self.name.capitalize()
        return super().clean()
    
    def save(self, *args, **kwargs):
        self.name = self.name.capitalize()
        return super().save(*args, **kwargs)
    
class Joyas(models.Model):
    image = models.ImageField(verbose_name="Imagen", upload_to='joyas/')
    name = models.CharField(verbose_name="Nombre", max_length=50, unique=True)
    description = models.TextField(verbose_name="Descripcion")
    price = models.DecimalField(verbose_name="Precio", default=0, decimal_places=2, max_digits=10)
    available = models.BooleanField(verbose_name="Disponibilidad", default=False)
    stock = models.PositiveIntegerField(verbose_name='Cantidad', default=0)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Joyas, through="app_store.CartItems")

class CartItems(models.Model):
    product = models.ForeignKey(Joyas, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

class Compra(models.Model):
    user_email = models.EmailField(verbose_name="Correo", max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return f"Compra de {self.user_email}"

class ProductosCompra(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE, related_name='products')
    product = models.ForeignKey(Joyas, on_delete=models.CASCADE)
    product_price = models.DecimalField(verbose_name="Precio unitario", default=0, decimal_places=2, max_digits=10)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(verbose_name="Precio total", default=0, decimal_places=2, max_digits=12)

    def save(self, *args, **kwargs):
        self.total_price = self.product_price * self.quantity
        super().save(*args, **kwargs)

    @classmethod
    def create_or_update(cls, compra, product, quantity):
        obj, created = cls.objects.get_or_create(compra=compra, product=product,
                                                 defaults={
                                                     'product_price': product.price,
                                                     'quantity': quantity,
                                                 })
        if not created:
            obj.quantity += quantity
            obj.product_price = product.price  
        obj.save()
        return obj