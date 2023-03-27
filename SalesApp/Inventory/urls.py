from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns=[
path('home',views.home,name='home'),
path('Products',views.Products, name='Products'),
path('PendingOrders',views.ShowProds, name='Products2'),
path('ConfirmedOrders',views.ShowComplete, name='doneorders'),
path('Ordered Products/<int:pk>/',views.ProdsinOrder, name='Products3'),
path('ClerkPage',views.Clerk, name='clerk'),
path('AddProduct', views.AddProduct, name='addproduct'),
path('NotifyParties', views.showNotify, name='shownotify'),
path('AddNotifyParty', views.AddNotify, name='addnotify'),
path('EditNotifyParty/<int:pk>/', views.EditNotify, name='editnotify'),
path('edit/<int:pk>/', views.EditProduct, name='editproduct'),
path('delete/<int:pk>/', views.delProduct, name='deleteproduct'),
path('',views.home, name='home'),
path('Signup',views.Signup, name='Signup'),
path('Login', views.Login, name='Login'),
path('logout', views.logout, name='logout'),
path('CreateOrder', views.CreateOrder, name='createorder'),
path('CompleteOrder/<int:pk>/', views.CompleteOrder, name='completeorder'),
path('ConfirmCreateOrder/<int:pk>/', views.ConfirmOrder, name='confirmcreateorder'),
path('view/<int:pk>/', views.Info, name='view'),
path('edit/<int:pk>/', views.Edit, name='edit'),
path('UnfinishedTransactions/<int:pk>/', views.EditTrans, name='UnfTrans'),
path('DeleteTrans/<int:pk>/', views.DeleteTrans, name='deltrans'),
path('editorder/<int:pk>/', views.ChangeTrans, name='editorder'),
path('confirmorder/<int:pk>/', views.ConfirmTrans, name='confirmorder'),
path('UserAdded', views.AddOrder, name='OrderAdded'),
path('Developer', views.Developer, name='Developer')


] 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

