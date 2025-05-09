from django.urls import path
from petstoreapp import views
# import to display the images
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
   path('',views.index),
   path('login',views.userlogin),
   path('register',views.register),
   path('contactus',views.contactus),
   path('details/<petid>',views.getPetById),
   path('logout',views.userlogout),
   path('filter-by-cat/<catName>',views.filterByCategory),
   path('sort-by-price/<direction>',views.sortByPrice),
   path('filter-by-range',views.filterByRange),
   path('addtocart/<petid>',views.addToCart),
   path('mycart',views.showMyCart),
   path('removecart/<cartid>',views.removeCart),
   path('updatequantity/<cartid>/<operation>',views.updateQuantity),
   path('confirm_order',views.confirmOrder),
   path('makepayment',views.makepayment),
   path('placeorder',views.placeOrder),
   path('editprofile',views.edit_profile)
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)