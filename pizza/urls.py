from django.urls import path

from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	
	path('home/', views.home, name="home"),
    
    path('home/contact', views.contact, name="contact"),
    path('home/cart/', views.cart, name="cart"),
    path('registration/', views.registration, name="registration"),
    path('', views.login, name="login"),
    path('checkout', views.checkout, name="checkout"),
    path('update_item/', views.updateItem, name="updateItem"),
    path('logout/',views.user_logout ,name = 'user_logout'),
    path('process_order/', views.processOrder, name="processOrder"),
    path('cust/',views.customize, name="customize"),
    path('custOrder/',views.addcustom,name="addcustom"),
    path('OrderDetails/',views.orderDetails,name="orderDetails"),
    
]
urlpatterns += static(settings.MEDIA_URL , document_root=settings.MEDIA_ROOT)