from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns=[
path('',views.home, name='home'),

#displaying
path('ClerkPage',views.Clerk, name='clerk'),
path('Products',views.Products, name='Products'),
path('NotifyParties', views.showNotify, name='shownotify'),
path('Developer', views.Developer, name='Developer'),

#Notify Party management
path('AddNotifyParty', views.AddNotify, name='addnotify'),
path('EditNotifyParty/<int:pk>/', views.EditNotify, name='editnotify'),

#Product management
path('AddProduct', views.AddProduct, name='addproduct'),
path('edit/<int:pk>/', views.EditProduct, name='editproduct'),
path('delete/<int:pk>/', views.delProduct, name='deleteproduct'),
path('view/<int:pk>/', views.Info, name='view'),

#authentication
path('Signup',views.Signup, name='Signup'),
path('Login', views.Login, name='Login'),
path('logout', views.logoutuser, name='logout'),

#Order and OrderedProduct management
path('PendingOrders',views.ShowProds, name='Products2'),
path('ConfirmedOrders',views.ShowComplete, name='doneorders'),

path('CreateOrder', views.CreateOrder, name='createorder'),
path('AddOrder/<int:pk>/', views.AddtoOrder, name='addtoorder'),
path('ConfirmCreateOrder/<int:pk>/', views.ConfirmOrder, name='confirmcreateorder'),
path('CompleteOrder/<int:pk>/', views.CompleteOrder, name='completeorder'),

path('Order/<int:pk>/', views.EditTrans, name='UnfTrans'),
path('editorder/<int:pk>/', views.ChangeTrans, name='editorder'),
path('confirmorder/<int:pk>/', views.ConfirmTrans, name='confirmorder'),
path('DeleteTrans/<int:pk>/', views.DeleteTrans, name='deltrans'),

#path('Ordered Products/<int:pk>/',views.ProdsinOrder, name='Products3'),
#path('UserAdded', views.AddOrder, name='OrderAdded'),



] 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

