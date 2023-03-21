from django.contrib import messages
from django.shortcuts import render,redirect,get_object_or_404
from .models import Userperson, Product, OrderedProduct, FinalOrder, NotifyParty, Company, Consignee
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User, auth
from django.template import loader
from django.templatetags.static import static
from django.http import HttpResponse
from django.conf import settings
from decimal import Decimal
import random
import string


def home(request):
    condition = ''
    use = "home"
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
            'C' : condition,
            'use' : use
            })

def Clerk(request):
    condition = ""
    print(request.path)
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
        return render(
            request,'Inventory/clerk.html',{
                'C' : condition,
                'username' : request.session['user'],
                'userid' : request.session['userid'],
                'password' : request.session['password'],
                'firstname' : request.session['firstname'],
                'lastname' : request.session['lastname'],
                'birthday' : request.session['birthday'],
                'sex' : request.session['sex'],
            }
        )


def isDigit(request,num):
    try:
        Decimal(num)
        return True
    except ValueError:
        return False
 
def AddProduct(request):
    condition = ""
    if request.user.is_authenticated:
        condition = True
        if request.method == "POST":
            imgfile = request.FILES.get('Image')               
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

            if name.strip() == "" or length.strip() == ""  or manufacturer.strip() == "" or manuloc.strip() == "" or color.strip() == "" or cost.strip() == "" or desc.strip() == "" or contact.strip() == "" or meas.strip() == "" or weight.strip() == "":
                messages.info(request, 'You must fill out all the fields')
                return redirect('addproduct')

            elif isDigit(request,num = str(cost[0:])) == False:
                messages.warning(request,"Input cost was not a number")
                return redirect('addproduct')


            elif Decimal(cost[slice(0,len(cost))]) <= 0:
                messages.warning(request,"No negative costs or costs equal to 0")
                return redirect('addproduct')
 
            elif stock == "" or stock == None or "." in stock or int(stock) <= 0:
                messages.error(request, 'Stock must not be blank, a decimal, or less than 0')
                return redirect('addproduct')
            
            New = Product.objects.create(
                Name = name,
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

            if imgfile == None:
                New.MakeMark()
            else:
                New.Image = imgfile
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
            imgfile = request.FILES.get('Image')
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

            if name.strip() == "" or length.strip() == ""  or manufacturer.strip() == "" or manuloc.strip() == "" or color.strip() == "" or cost.strip() == "" or desc.strip() == "" or contact.strip() == "" or meas.strip() == "" or weight.strip() == "":
                messages.info(request, 'You must fill out all the fields')
                return redirect('editproduct',pk)

            elif isDigit(request,num = str(cost[0:])) == False:
                messages.warning(request,"Input cost was not a number")
                return redirect('editproduct', pk)

            elif Decimal(cost[slice(0,len(cost))]) <= 0:
                messages.warning(request,"No negative costs or costs equal to 0")
                return redirect('editproduct', pk)


            Existing.Name = name
            if imgfile == None:
                pass
            else:
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

def delProduct(request,pk):
    Deleted = get_object_or_404(Product, pk=pk)
    if request.user.is_authenticated:
        Deleted.Status = False
        Deleted.save()
        return redirect('Products')




def Products(request):
    use = 'home'
    condition = ""
    User = Userperson.objects.all()
    P = Product.objects.filter(Stock__gte = 1).filter(Status = True).order_by('-Stock')
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
            'username' : request.session['user'],
            'use' : use
            })
    else:
        condition = False   
        return render(request, 'Inventory/products.html',{
            'C' : condition,
            'P':P, 
            'User':User,
            'url':settings.MEDIA_URL,
            'use' : use
            })

def Signup(request):
    if request.method == 'POST':
        username = request.POST.get('usern')
        password = request.POST.get('passn')
        first_name = request.POST.get('firstn')
        last_name = request.POST.get('lastn')
        birthday = request.POST.get('birthday1')
        sex = request.POST.get('sexx')

        if User.objects.filter(username = username):
            messages.info(request,"Username is already taken")
            return redirect('Signup')
        else:
            if str(username).strip() == '' or str(password).strip() == '' or str(first_name).strip() == '' or str(last_name).strip() == '' or str(birthday).strip() == '' or str(sex).strip() == '':
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

def ShowProds(request):
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

        AllOrders = FinalOrder.objects.filter(Finished = False)

        return render(request, 'Inventory/users2.html',{
            'C' : condition,
            'Orders' : AllOrders,
        })

def ProdsinOrder(request, pk):
    condition = True
    Ordered = OrderedProduct.objects.filter(OrderID = pk)
    empty = len(Ordered) == 0
    return render(request, 'Inventory/ProductsinOrder.html',{
        'C' : condition,
        'Ordered' : Ordered,
        'e' : empty
    })




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

def VerifID(request): #use for both FinalOrder and OrderedProduct, tanggalin letters
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
        Orders = FinalOrder.objects.filter(Finished = False)
        Products = Product.objects.filter(Stock__gte = 1).filter(Status = True)
   
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
        #ChosenConsignee = get_object_or_404(Consignee, Name=ChosenOrder.BL.Name)
    else:
        ChosenOrder = ""

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

            if str(Person).strip() == '' or str(Port).strip() == '' or str(Person).strip() == "Type new Consignee Name" or str(Port).strip() == "Type new Port of Discharge":
                messages.info(request,"No proper fields for either Consignee or Port of Discharge")
                return redirect('confirmcreateorder', pk)

          
            Cost = Decimal(Cost)

            
            #Final Order Section
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
                    NumOfBL = 3,
                )

                NewOrder.TotalCost += Cost
                NewOrder.PD()
                ChosenOrder = NewOrder
            
            else:
                ChosenOrder.TotalCost += Cost
                ChosenOrder.save()

            
            #Ordered Product Section
            remarks = request.POST.get('Description')

            if str(remarks).strip() == "":
                remarks = "No remarks"

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
                'fetch' : fetch
            })
        

def CompleteOrder(request,pk):
    OrderDone = get_object_or_404(FinalOrder, pk=pk)
    OrderDone.Finished = True

    OrderedProds = OrderedProduct.objects.filter(OrderID = OrderDone)
    for item in OrderedProds:
        item.Marks.Stock -= item.quantity
        item.Marks.save()
        item.save()

    OrderDone.save()
    print(OrderDone.pk)
    return redirect('Products2')

def ShowComplete(request):
    condition = True
    use = 'complete'
    DoneOrders = FinalOrder.objects.filter(Finished = True)
    OrderedP = OrderedProduct.objects.all()
    if request.user.is_authenticated:
        pass
        return render(request, 'Inventory/products.html',{
            'use' : use,
            'C' : condition,
            'O' : DoneOrders,
            'Ord' : OrderedP
        })

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
    Order = get_object_or_404(FinalOrder, pk=TobeDel.OrderID.pk)
    Order.TotalCost -= TobeDel.totalcost
    Order.save()
    TobeDel.delete()
    return redirect('UnfTrans', pk=Order.pk)

def EditTrans(request, pk):
    condition = ""
    Order = get_object_or_404(FinalOrder, pk=pk)
    Products = OrderedProduct.objects.filter(OrderID = Order).order_by('-totalcost')
    if request.user.is_authenticated:
        condition = True
        empty = len(Products) == 0
        return render(request,'Inventory/cart.html',{ 
                    'C' : condition,
                    'Products' : Products,
                    'p' : pk,
                    'e' : empty
                })
   

#This will lead to the confirm order page, where quantity, product price, and others will be updated to confirm change in transaction
#Ito para sa akin yung pinakamahirap na ginawa ko so far for this project. I needed to simulate a UX case na walang pipiliing dropdown option ang user.
def ChangeTrans(request,pk):
    condition = ""
    ChosenTrans = get_object_or_404(OrderedProduct, pk=pk)
    quant = ChosenTrans.Marks.Stock
    prods = Product.objects.filter(Stock__gte = 1).filter(Status = True)
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


def ConfirmTrans(request,pk):
    state = request.session.get('state')
    ChosenTrans = get_object_or_404(OrderedProduct, pk=request.session.get('OrderedPRem')) #Orderedproduct
    orderprodname = request.session.get('OrderPname') #Orderedproductpk
    remarks = request.session.get('Remarks') #remarks
    Newproduct = get_object_or_404(Product, Name = orderprodname) #new product
    Order = get_object_or_404(FinalOrder,pk=ChosenTrans.OrderID.pk)

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
    
            Order.TotalCost -= ChosenTrans.totalcost
            ChosenTrans.totalcost = Decimal(cost[1:len(cost)])
            Order.TotalCost += ChosenTrans.totalcost
            Order.save()
            
            ChosenTrans.quantity = int(q)
            ChosenTrans.Marks = get_object_or_404(Product, Name=orderprodname)
            ChosenTrans.remarks = Newremarks
            ChosenTrans.save()
            return redirect('UnfTrans', pk=ChosenTrans.OrderID.pk)

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


    