from django.contrib import admin
from petstoreapp.models import Pet, Cart,Order

# Register your models here.
class PetAdmin(admin.ModelAdmin):
    list_display = ['id','name','age','breed','type','price','gender','description','petimage']
    list_filter = ['type','price']

admin.site.register(Pet,PetAdmin)

class CartAdmin(admin.ModelAdmin):
    list_display = ['id','uid','petid','quantity']
    list_filter = ['uid']

admin.site.register(Cart, CartAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','orderid','userid','petid','quantity']
    list_filter = ['userid','petid']

admin.site.register(Order, OrderAdmin)