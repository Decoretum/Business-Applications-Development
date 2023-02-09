from django.contrib import messages
from django.shortcuts import render,redirect,get_object_or_404
from .models import Userperson, Product, OrderedProduct, FinalOrder
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User, auth
from django.template import loader
from django.http import HttpResponse
from django.core import serializers

# Create your views here.
def home(request):
    condition = ''
    if request.user.is_authenticated:
        condition = True
        return render(request, 'Inventory/home.html', {
        'C' : condition
        })
    else:
        print("no user")
        condition = False
        return render(
            request, 'Inventory/home.html', {
            'C' : condition
            })
    #Product.objects.create(Name = "NanoLaser",Brand = "NanoTechPH", Color = "Blue",Cost = "P5000")
 

def Products(request):
    condition = ""
    User = Userperson.objects.all()
    P = Product.objects.filter(Stock__gte = 0)
    if request.user.is_authenticated:
        condition = True
        return render(request, 'Inventory/products.html',{
            'C' : condition,
            'P':P, 
            'User':User,
            'username' : request.session['user']
            })
    else:
        condition = False
        return render(request, 'Inventory/products.html',{
            'C' : condition,
            'P':P, 
            'User':User
            })

def Signup(request):
    if request.method == 'POST':
        username = request.POST.get('usern')
        password = request.POST.get('passn')
        first_name = request.POST.get('firstn')
        last_name = request.POST.get('lastn')
        birthday = request.POST.get('birthday1')
        sex = request.POST.get('sexx')
        print(username)

        if User.objects.filter(username = username):
            messages.info(request,"Username is already taken")
            return redirect('Signup')
        else:
            if username == '' or password == '' or first_name == '' or last_name == '' or birthday == '' or sex == '':
                messages.info(request,"Missing Credentials!")
                return redirect('Signup')
                
            else:
                Userinst = User.objects.create_user(username=username, password=password, 
                first_name=first_name, last_name=last_name)

                Userinst.save()

                Userperson.objects.create(
                    username = username,
                    password = password,
                    first_name = first_name,
                    last_name = last_name,
                    birthday = birthday,
                    sex = sex
                )

                messages.info(request,'Account created successfully')
                return redirect('Login')

    else:
        return render(request,'Inventory/signup.html')

def Login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        checking = authenticate(request, username=username, password=password)
        if checking is not None:
            login(request, checking)
            userobj = get_object_or_404(Userperson, username=username, password=password )
            request.session['user'] = userobj.username
            request.session['userid'] = userobj.pk
            request.session['password'] = userobj.password
            request.session['firstname'] = userobj.first_name
            request.session['lastname'] = userobj.last_name
            request.session['birthday'] = str(userobj.birthday)
            request.session['sex'] = userobj.sex
            return redirect('home')
        else:
            messages.info(request,'Invalid Login Credentials')
            return redirect('Login')

    else:
        return render(request,'Inventory/Login.html')

''' Logic of Users, this will be primarly front-end, no editting of transaction, but you can create new order here 
    This will be where unfinished orders will be 
'''
def ShowOrders(request,Name,Cost,Length,Remark,Image,Manufacturer):
    #I will make a hashtable
    Order = {}
    Order["Name"] = Name
    Order["Cost"] = Cost
    Order["Length"] = Length
    Order["Remark"] = Remark
    Order["Image"] = Image
    Order["Manufac"] = Manufacturer
    return Order

def Users(request):
    condition = ""
    if request.user.is_authenticated:
        condition = True
        currentuser = get_object_or_404(Userperson, username = request.session['user'])
        OProducts = OrderedProduct.objects.filter(Client = currentuser)
        FinalOrders = FinalOrder.objects.all()
        ProductsinOrder = OrderedProduct.objects.all()
        Ordersarray=[]
        for x in FinalOrders:
            Ordersarray.append(x.pk)
        
        for x in ProductsinOrder:
            for y in FinalOrders:
                if x.Finalorder == y:
                    Ordersarray.append(ShowOrders(request,x.Order.Name,x.Order.Cost,x.Order.Length,x.remarks,x.Order.Image,x.Order.Manufacturer))
        print(Ordersarray)
        
    
        return render(request,'Inventory/users.html',
        {'username' : request.session['user'],
        'userid' : request.session['userid'],
        'password' : request.session['password'],
        'firstname' : request.session['firstname'],
        'lastname' : request.session['lastname'],
        'birthday' : request.session['birthday'],
        'sex' : request.session['sex'],
        'OProducts' : OProducts,
        'C' : condition,
        'Order' : FinalOrders,
        'Products' : ProductsinOrder
        })
    else:
        condition = False
        return render(request,'Inventory/users.html',
        {'username' : request.session['user'],
        'userid' : request.session['userid'],
        'password' : request.session['password'],
        'firstname' : request.session['firstname'],
        'lastname' : request.session['lastname'],
        'birthday' : request.session['birthday'],
        'sex' : request.session['sex'],
        'userobj' : currentuser,
        'OProducts' : OProducts,
        'C' : condition})

def logout(request):
    print('logout')
    auth.logout(request)
    return redirect('Login')

def Info(request,pk):
    condition = ""
    CurrentProd = get_object_or_404(Product, pk=pk)
    if request.user.is_authenticated:
        condition = True
        return render(request, 'Inventory/Info.html',{
            'C' : condition,
            'P' : CurrentProd

        })
    else:
        condition = False
        return render(request, 'Inventory/Info.html',{
            'C' : condition,
            'P' : CurrentProd

        })
def Edit(request,pk):
    condition = ""
    if request.user.is_authenticated:
        condition = True
        return render(request,'Inventory/edit.html',{
            'C' : condition
        })
    

def Order(request,pk):
    condition = ""
    if request.user.is_authenticated:
        condition = True
        CurrentProd = get_object_or_404(Product, pk=pk)
        print(type(CurrentProd.pk))
        Orders = FinalOrder.objects.all()
        CUser = get_object_or_404(Userperson, username = request.session['user'])
        if request.method == "POST":
            quantvalue = request.POST.get('drop')
            totalcost3 = request.POST.get('totalcost')
            remark = request.POST.get('remark')
            ordernumber = request.POST.get('ordername')
            ChosenOrder = get_object_or_404(FinalOrder, pk = ordernumber)
            OrderedProduct.objects.create(Client = CUser, Order = CurrentProd, 
            remarks = remark, quantity = quantvalue, totalcost = totalcost3, Finalorder = ChosenOrder)
            #Product.objects.filter(pk=pk).update(Stock -= quantvalue )
            CurrentProd.Stock -= int(quantvalue)
            CurrentProd.save()
            
            return redirect('Products')
        else:
            ordersarray = []
            array = []
            P = Product.objects.all()
            for x in range(CurrentProd.Stock):
                array.append(x+1)
            return render(request,'Inventory/order.html',{ 
                'O' : Orders,
                'P' : P,
                'Current' : CurrentProd,
                'A' : array,
                'C' : condition
            })
    else:
        condition = False
        print("No user, cant order!")
        return render(request,'Inventory/cantorder.html',{ 
                'C' : condition
            })

def Cart(request):
    condition = ""
    arraylist = []
    pricelist = 0
    Orders = FinalOrder.objects.all()
    Products = OrderedProduct.objects.all()
    if request.user.is_authenticated:
        Current = get_object_or_404(Userperson,username = request.session['user'])
        UserProducts = OrderedProduct.objects.all().filter(Client = Current)
        for userp in UserProducts:
            arraylist.append(userp.Client)
            pricelist += userp.totalcost
        condition = True
        if UserProducts != None:
            return render(request,'Inventory/cart.html',{ 
                    'C' : condition,
                    'User' : Current,
                    'list' : arraylist,
                    'CurrentProd' : Products,
                    'O' : Orders,
                    'price' : pricelist
                })
    else:
        condition = False
        return render(request,'Inventory/cart.html',{ 
                'C' : condition
            })

def AddOrder(request):
    if request.user.is_authenticated:
        currentuser = get_object_or_404(Userperson, username = request.session['user'])
        OProducts = OrderedProduct.objects.filter(Client = currentuser)
        array = []
        condition = True
        FinalOrder.objects.create()
        return redirect('User')
          

def ConfirmOrder(request):
    if request.user.is_authenticated:
        Current = get_object_or_404(Userperson,username = request.session['user'])
    else:
        pass
    
def Developer(request):
    condition = ''
    if request.user.is_authenticated:
        condition = True
        return render(request,'Inventory/programmer.html',{
            'C' : condition
        })
    else:
        condition = False
        return render(request,'Inventory/programmer.html',{
            'C' : condition
        })


    