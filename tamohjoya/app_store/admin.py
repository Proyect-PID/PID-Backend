from django.contrib import admin
from app_store.models import Category, Joyas,Compra,ProductosCompra

admin.site.register(Category)
admin.site.register(Joyas)
admin.site.register(Compra)




@admin.register(ProductosCompra)
class ProductosCompraAdmin(admin.ModelAdmin):
    readonly_fields = ('product_price', 'total_price')
    list_display = ('get_user_email', 'product', 'quantity')
    
    def get_user_email(self, obj):
        return obj.compra.user_email
    get_user_email.short_description = 'Usuario (Email)'   
    
    
    
     
    
   