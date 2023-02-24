from django.contrib import messages
from django.shortcuts import render,redirect,get_object_or_404
from .models import Userperson, Product, OrderedProduct, FinalOrder, NotifyParty, Company, Consignee
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
        
        if request.session.get('NAVIGATE') == "confirmorder" or request.session.get('NAVIGATE') == "confirmtrans":
            print('DELETED CACHE')
            request.session['Remarks'] = None
            request.session['productname'] = None
            request.session['OrderedPRem'] = None
            request.session['OrderPname'] = None
            request.session['manufacturer'] = None
            request.session['Order'] = None

        request.session['NAVIGATE'] = "home"
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
  
 
def AddProduct(request):
    condition = ""
    if request.user.is_authenticated:
        condition = True
        if request.method == "POST":
            imgfile = request.POST.get('Image')
            if imgfile == None:
                imgfile = "N/A"
            name = request.POST.get('Name')
            length = request.POST.get('Length')
            manufacturer = request.POST.get('Manufacturer')
            manuloc = request.POST.get('Location')
            color = request.POST.get('Color')
            cost = request.POST.get('Cost')
            stock = request.POST.get('Stock')
            desc = request.POST.get('Description')
            contact = request.POST.get('Contact')
            meas = request.POST.get('Measurement')
            weight = request.POST.get('Weight')
            Product.objects.create(
                Name = name,
                Image = imgfile,
                Manufacturer = manufacturer,
                ManuLoc = manuloc,
                Color = color,
                Length = length,
                Cost = cost,
                Stock = stock,
                Description = desc,
                Measurement = meas,
                GrossWeight = weight,
                Contact = contact,
            )
            New = get_object_or_404(Product, Name = name)
            New.MakeMark()


            return redirect ('Products')
        else:
            return render(
                request, 'Inventory/AddProd.html',{
                'C' : condition
                }
            )
        
    else:
        pass

def EditProduct(request,pk):
    condition = ""
    if request.user.is_authenticated:
        condition = True
        Existing = get_object_or_404(Product, pk=pk)

        if request.method == "POST":
            imgfile = request.POST.get('Image')
            if imgfile == None:
                imgfile = None
            name = request.POST.get('Name')
            length = request.POST.get('Length')
            manufacturer = request.POST.get('Manufacturer')
            manuloc = request.POST.get('Location')
            color = request.POST.get('Color')
            cost = request.POST.get('Cost')
            contact = request.POST.get('Contact')

            desc = request.POST.get('Description')
            meas = request.POST.get('Measurement')
            weight = request.POST.get('Weight')


            Existing.Name = name
            if imgfile == None:
                Existing.Image = imgfile

            Existing.Measurement = meas
            Existing.GrossWeight = weight
            Existing.Manufacturer = manufacturer
            Existing.ManuLoc = manuloc
            Existing.Color = color
            Existing.Length = length
            Existing.Cost = cost
            Existing.Description = desc
            Existing.Contact = contact
            print(Existing.Manufacturer)
            Existing.MakeMark()
            return redirect ('view',pk)
        
        else:
            return render(
                request, 'Inventory/edit.html',{
                'C' : condition,
                'Prod' : Existing
                }
            )
        
    else:
        pass

def Products(request):
    condition = ""
    User = Userperson.objects.all()
    P = Product.objects.filter(Stock__gte = 0).order_by('-Stock')
    if request.user.is_authenticated:
        condition = True
        if request.session.get('NAVIGATE') == "confirmorder" or request.session.get('NAVIGATE') == "confirmtrans":
            print('DELETED CACHE')
            request.session['Remarks'] = None
            request.session['productname'] = None
            request.session['OrderedPRem'] = None
            request.session['OrderPname'] = None
            request.session['manufacturer'] = None
            request.session['Order'] = None

        request.session['NAVIGATE'] = "products"
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

def Users(request):
    condition = ""
    if request.user.is_authenticated:
        condition = True
    
        if request.session.get('NAVIGATE') == "confirmorder" or request.session.get('NAVIGATE') == "confirmtrans":
            print('DELETED CACHE')
            request.session['Remarks'] = None
            request.session['productname'] = None
            request.session['OrderedPRem'] = None
            request.session['OrderPname'] = None
            request.session['manufacturer'] = None
            request.session['Order'] = None

        request.session['NAVIGATE'] = "users"

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
                if Allarray[i] == prod.OrderID.pk:
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

        if request.session.get('NAVIGATE') == "confirmorder" or request.session.get('NAVIGATE') == "confirmtrans":
            print('DELETED CACHE')
            request.session['Remarks'] = None
            request.session['productname'] = None
            request.session['OrderedPRem'] = None
            request.session['OrderPname'] = None
            request.session['manufacturer'] = None
            request.session['Order'] = None

        request.session['NAVIGATE'] = "info"
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

        if request.session.get('NAVIGATE') == "confirmorder" or request.session.get('NAVIGATE') == "confirmtrans":
            print('DELETED CACHE')
            request.session['Remarks'] = None
            request.session['productname'] = None
            request.session['OrderedPRem'] = None
            request.session['OrderPname'] = None
            request.session['manufacturer'] = None
            request.session['Order'] = None

        return render(request,'Inventory/edit.html',{
            'C' : condition
        })

def VerifID(request): #use for both FinalOrder and OrderedProduct
    ID = []
    for x in range(13):
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

def VerifBL(request): #use for both FinalOrder and OrderedProduct
    ID = []
    for x in range(20):
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

'''
At this point, Creating an order and an ordered product will cause the following:
'''

def CreateOrder(request):
    condition = ""
    if request.user.is_authenticated:
        condition = True
        Orders = FinalOrder.objects.all()
        Products = Product.objects.all()
        if request.method == "POST":
            OrderNum = request.POST.get('Order')
            if request.POST.get('proddrop') == "":
                messages.info(request,"Choose a product!")
                return redirect('createorder')
            
            if OrderNum == "New Order":
                OrderNum = "New"
  
            if OrderNum == "":
                messages.info(request,"No Order Selected!")
                return redirect('createorder')
            
            
            request.session['Order'] = OrderNum
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
    remarks = request.session.get('Remarks') #remarks
    fetch = request.session.get('Order')
    ChosenProduct = get_object_or_404(Product, pk=pk) #product
    
    if fetch != "New":
        ChosenOrder = get_object_or_404(FinalOrder, pk=fetch)
        ChosenConsignee = get_object_or_404(Consignee, Name=ChosenOrder.BL.Name)

    else:
        ChosenOrder = ""
        ChosenConsignee = ""

    AllOrders = FinalOrder.objects.all() #all orders
    stock = ChosenProduct.Stock
    stocka = []
    condition = ""
    for i in range(1,stock+1):
        stocka.append(i)
    if request.user.is_authenticated:
        condition = True
        request.session['NAVIGATE'] = "confirmorder"
        if request.method == "POST":
            if request.POST.get('Back') == "Back":
                print('GOING BACK')
                request.session['Order'] = None
                request.session['productname'] = None
                return redirect('createorder')

            order = "" #placeholder
            q = request.POST.get('drop')
            Cost = request.POST.get('totalcost')[1:len(request.POST.get('totalcost'))]
            OrderNum = request.POST.get('Order')
            Person = request.POST.get('Person')
            Port = request.POST.get('Port')

            if Person == '' or Port == '':
                messages.info(request,"No fields for either Consignee or Port of Discharge")
                return redirect('confirmcreateorder', pk)

            if int(q) == 1:
                Cost = int(ChosenProduct.Cost[1:len(request.POST.get('totalcost'))])

            else:
                Cost = int(Cost)
                
            if fetch == "New":
            
                NewConsign = Consignee.objects.create(
                    BL = VerifBL(request),
                    Name = Person,
                    PortDischarge = Port
                )
                NewConsign.save()

                NewOrder = FinalOrder.objects.create(
                    Verification = VerifID(request),
                    BL = NewConsign,
                    NumOfBL = 3
                )
                NewOrder.PD()
                ChosenOrder = NewOrder


            
            remarks = request.POST.get('Description')
            NewOrderProduct = OrderedProduct.objects.create(
                OrderedProductID = VerifID(request),
                OrderID = ChosenOrder,
                Marks = ChosenProduct, 
                remarks = remarks, 
                quantity = q, 
                totalcost = Cost, 
                )
            
            #ChosenTrans.Order.Stock -= int(q) no removing yet since order is not confirmed, just edited
            NewOrderProduct.save()

            if request.POST.get('More') == "More":
                print('MORE')
                return redirect('createorder')
                
            else:
                return redirect('Products')

        
        else:
            return render(request,'Inventory/confirmcreateorder.html',{
                'OrderedP' : ChosenProduct,
                'Order' : ChosenOrder,
                'C' : condition,
                'stocka' : stocka,
                'Rem' : remarks,
                'Orders' : AllOrders
            })
        
'''
AddOrder will be a component of another view functionality

'''
def AddOrder(request):
    if request.user.is_authenticated:
        Order = FinalOrder.objects.create(
            Verification = VerifID(request),
            )
        Order.PlaceDate = str(Order.Place) + ", " + str(Order.OrderDate) 
        Order.save()
        return Order
    
def DeleteTrans(request,pk):
    TobeDel = get_object_or_404(OrderedProduct, pk=pk)
    TobeDel.delete()
    return redirect('UnfTrans')

def EditTrans(request):
    condition = ""
    pricelist = 0
    Orders = FinalOrder.objects.all()
    OrderedProducts = OrderedProduct.objects.all().order_by('OrderID')
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
    quant = ChosenTrans.Marks.Stock
    prods = Product.objects.all()
    currentq = ChosenTrans.quantity
    currentprod = ChosenTrans.Marks.Name
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
            request.session['OrderPname'] = ChosenTrans.Marks.Name
            
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

        request.session['NAVIGATE'] = "confirmtrans"

        if request.method == "POST":
            cost = request.POST.get('totalcost')
            Newremarks = request.POST.get('Description')
            q = request.POST.get('drop')
            if int(q) == 1:
                print('q is 1')
                ChosenTrans.totalcost = Newproduct.Cost[1:len(Newproduct.Cost)]
            else:
                ChosenTrans.totalcost = cost[1:len(cost)]
            
            ChosenTrans.quantity = int(q)
            ChosenTrans.Marks = get_object_or_404(Product, Name=orderprodname)
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

        if request.session.get('NAVIGATE') == "confirmorder" or request.session.get('NAVIGATE') == "confirmtrans":
            print('DELETED CACHE')
            request.session['Remarks'] = None
            request.session['productname'] = None
            request.session['OrderedPRem'] = None
            request.session['OrderPname'] = None
            request.session['manufacturer'] = None
            request.session['Order'] = None

        return render(request,'Inventory/programmer.html',{
            'C' : condition
        })
    else:
        condition = False
        return render(request,'Inventory/programmer.html',{
            'C' : condition
        })


    