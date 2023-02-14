from django.contrib import messages
from django.shortcuts import render,redirect,get_object_or_404
from .models import Userperson, Product, OrderedProduct, FinalOrder
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User, auth
from django.template import loader
from django.http import HttpResponse
from django.core import serializers
import random
import string


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
            request.session['state'] = "create"
            return redirect('home')
        else:
            messages.info(request,'Invalid Login Credentials')
            return redirect('Login')

    else:
        return render(request,'Inventory/Login.html')

''' 

Logic of Users, this will be primarly front-end, with a button for editting of transaction, and you can create new order here 
This will be where unfinished orders will be 

architecture of code

1. array with order numbers
2. create an array per order number, each array will be filled with hashtables that are for multiple products 
all product queries

3. iterate through all product queries
if product final order == product final order:
then find keyvalue of ordernumber = final order number

'''
def Users(request):
    condition = ""
    if request.user.is_authenticated:
        condition = True
        currentuser = get_object_or_404(Userperson, username = request.session['user'])
        FinalOrders = FinalOrder.objects.all() #order numbers
        ProductsinOrder = OrderedProduct.objects.all()
        Ordersarray=[]
        Allarray = []
        
        for x in FinalOrders: #1 
            Allarray.append(x.pk)

        for x in range(0,len(FinalOrders)): #2
            Ordersarray.append([Allarray[x]])
         
        #3
        #Might need to use pointers
        #runtime of O(n^2), but speed not a priority in functional requirement
        i = 0 #pointer for reference array
        j = 0 #pointer for main array
        while i <= len(Allarray) - 1:
            for prod in ProductsinOrder:
                if Allarray[i] == prod.Finalorder.pk:
                    Ordersarray[j].append((prod))
                
            i += 1
            j += 1

        print(Allarray)
        print(Ordersarray)
        
    
        return render(request,'Inventory/users.html',
        {'username' : request.session['user'],
        'userid' : request.session['userid'],
        'password' : request.session['password'],
        'firstname' : request.session['firstname'],
        'lastname' : request.session['lastname'],
        'birthday' : request.session['birthday'],
        'sex' : request.session['sex'],
        'C' : condition,
        'Order' : FinalOrders,
        'Products' : ProductsinOrder,
        'OrdersAndProds' : Ordersarray
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

def VerifID(request):
    ID = []
    for x in range(12):
        chooser = random.randint(1,2)
        if chooser == 1:
            randomizerlet = random.choice(string.ascii_letters)
            x = randomizerlet 
            ID.append(str(x))
        elif chooser == 2:
            randomizernum = random.randint(1,9)
            x = randomizernum
            ID.append(str(x))  

    word = ''.join(ID)
    return word


def CreateOrder(request):
    condition = ""
    if request.user.is_authenticated:
        condition = True
        Orders = FinalOrder.objects.all()
        Products = Product.objects.all()
        if request.method == "POST":
            request.session['Remarks'] = request.POST.get('remark')
            request.session['productname'] = request.POST.get('proddrop')
            ChosenProduct = get_object_or_404(Product, Name = request.session['productname'])
            return redirect('confirmcreateorder', pk=ChosenProduct.pk)
        else:
            return render(request,'Inventory/MakeOrder.html',{ 
                'O' : Orders,
                'P' : Products,
                'C' : condition
            })

def ConfirmOrder(request,pk):
    ChosenProduct = get_object_or_404(Product, pk=pk) #product
    remarks = request.session.get('Remarks') #remarks

    stock = ChosenProduct.Stock
    stocka = []
    condition = ""
    for i in range(1,stock+1):
        stocka.append(i)
    if request.user.is_authenticated:
        condition = True
        if request.method == "POST":
            q = request.POST.get('drop')
            Cost = request.POST.get('totalcost')[1:len(request.POST.get('totalcost'))]

            if int(q) == 1:
                Cost = int(ChosenProduct.Cost)
            else:
                Cost = int(request.POST.get('totalcost')[1:len(request.POST.get('totalcost'))])
                
            remarks = remarks
            OrderID = AddOrder(request)
            NewOrderProduct = OrderedProduct.objects.create(Order = ChosenProduct, remarks = remarks, quantity = q, totalcost = Cost, Finalorder = OrderID)

            #ChosenTrans.Order.Stock -= int(q) no removing yet since order is not confirmed, just edited
            NewOrderProduct.save()
            if request.POST.get('More') == "More":
                print('MORE')
                return redirect('createorder')
            else:
                return redirect('Products')

        elif request.GET.get('Back') == "Back":
            print('GOT IT')
            request.session['productname'] = None
            return redirect('createorder')

        elif request.GET.get('More') == "More":
            q = request.POST.get('drop')
            print(q)
            print(request.POST.get('totalcost'))
            Cost = request.POST.get('totalcost')[1:len(str(request.POST.get('totalcost')))]

            if int(q) == 1:
                Cost = int(ChosenProduct.Cost)
            else:
                Cost = int(str(request.POST.get('totalcost')[1:len(str(request.POST.get('totalcost')))]))
            
            remarks = remarks
            OrderID = AddOrder(request)
            NewOrderProduct = OrderedProduct.objects.create(Order = ChosenProduct, remarks = remarks, quantity = q, totalcost = Cost, Finalorder = OrderID)

            #ChosenTrans.Order.Stock -= int(q) no removing yet since order is not confirmed, just edited
            NewOrderProduct.save()
            print('NEW PRODUCT')
            return redirect('createorder')

        else:
            return render(request,'Inventory/confirmcreateorder.html',{
                'OrderedP' : ChosenProduct,
                'C' : condition,
                'stocka' : stocka,
                'Rem' : remarks
            })
        
'''
AddOrder will be a component of another view functionality

'''
def AddOrder(request):
    if request.user.is_authenticated:
        Order = FinalOrder.objects.create(OrderID = VerifID(request))
        Order.save()
        return Order

def Order(request,pk):
    state = ""
    condition = ""
    if request.user.is_authenticated:
        condition = True
        CurrentProd = get_object_or_404(Product, pk=pk)
        print(type(CurrentProd.pk))
        Orders = FinalOrder.objects.all()
        if request.method == "POST":
            quantvalue = request.POST.get('drop')
            totalcost3 = request.POST.get('totalcost')
            remark = request.POST.get('remark')
            ordernumber = request.POST.get('ordername')
            ChosenOrder = get_object_or_404(FinalOrder, pk = ordernumber)
            OrderedProduct.objects.create(Order = CurrentProd, 
            remarks = remark, quantity = quantvalue, totalcost = totalcost3, Finalorder = ChosenOrder)
            #Product.objects.filter(pk=pk).update(Stock -= quantvalue )
            CurrentProd.save()
            
            return redirect('Products')
        else:
            array = []
            P = Product.objects.all()
            for x in range(CurrentProd.Stock):
                array.append(x+1)
            return render(request,'Inventory/order.html',{ 
                'state' : state,
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

def EditTrans(request):
    condition = ""
    pricelist = 0
    Orders = FinalOrder.objects.all()
    OrderedProducts = OrderedProduct.objects.all()
    if request.user.is_authenticated:
        condition = True
        return render(request,'Inventory/cart.html',{ 
                    'C' : condition,
                    'CurrentProd' : OrderedProducts,
                    'O' : Orders,
                    'price' : pricelist
                })
    else:
        condition = False
        return render(request,'Inventory/cart.html',{ 
                'C' : condition
            })

#This will lead to the confirm order page, where quantity, product price, and others will be updated to confirm change in transaction
#Ito para sa akin yung pinakamahirap na ginawa ko so far for this project. I needed to simulate a UX case na walang pipiliing dropdown option ang user.
def ChangeTrans(request,pk):
    condition = ""
    ChosenTrans = get_object_or_404(OrderedProduct, pk=pk)
    quant = ChosenTrans.Order.Stock
    prods = Product.objects.all()
    currentq = ChosenTrans.quantity
    currentprod = ChosenTrans.Order.Name
    stocky = []
    prody = []

    for x in range(1,quant+1):
        stocky.append(x)

    for x in prods:
        prody.append(x.Name)

    if request.method == 'POST':
        print('Authenticated!')
        print(ChosenTrans.pk)
        condition = True
        
        request.session['OrderedPRem'] = ChosenTrans.pk
        request.session['OrderPname'] = request.POST.get('proddrop')
        request.session['manufacturer'] = request.POST.get('Manufacturer')
        request.session['Remarks'] = request.POST.get('Description')
        if request.session['OrderPname'] == "":
            request.session['OrderPname'] = ChosenTrans.Order.Name
            
        return redirect('confirmorder', pk)

    else:
        condition = True
        return render(request,'Inventory/Editorder.html',{
                    'C' : condition,
                    'K' : ChosenTrans,
                    'Prod' : currentprod,
                    'A' : stocky,
                    'P' : prody,
                    'Q' : currentq
            })


#Confirmation, updated data should be presented from ChangeTrans
''' New updated fields for ordered product object would be : 
    Product
    Ordered prod remarks
    ordered prod quantity
    ordered prod totalcost
'''
def ConfirmTrans(request,pk):
    state = request.session.get('state')
    ChosenTrans = get_object_or_404(OrderedProduct, pk=request.session.get('OrderedPRem')) #Orderedproduct
    orderprodname = request.session.get('OrderPname') #Orderedproductpk
    remarks = request.session.get('Remarks') #remarks
    Newproduct = get_object_or_404(Product, Name = orderprodname) #new product

    stock = Newproduct.Stock
    stocka = []
    condition = ""
    for i in range(1,stock+1):
        stocka.append(i)
    if request.user.is_authenticated:
        condition = True
        if request.method == "POST":
            Newremarks = request.POST.get('Description')
            q = request.POST.get('drop')
            if int(q) == 1:
                print('q is 1')
                ChosenTrans.totalcost = Newproduct.Cost[1:len(Newproduct.Cost)]
            else:
                ChosenTrans.totalcost = request.POST.get('totalcost')
            
            ChosenTrans.quantity = int(q)
            ChosenTrans.Order = get_object_or_404(Product, Name=orderprodname)
            #ChosenTrans.Order.Stock -= int(q) no removing yet since order is not confirmed, just edited
            ChosenTrans.remarks = Newremarks
            ChosenTrans.save()
            return redirect('UnfTrans')

        elif request.GET.get('Next') == "Next":
            print('GOT IT')
            request.session['OrderPRem'] = None
            return redirect('editorder', pk)

        else:
            return render(request,'Inventory/confirmorder.html',{
                'OrderedP' : ChosenTrans,
                'C' : condition,
                'Prod' : Newproduct,
                'stock' : stocka,
                'Rem' : remarks,
            })
          
    
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


    