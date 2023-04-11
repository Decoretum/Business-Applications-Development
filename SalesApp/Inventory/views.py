from django.contrib import messages
from django.shortcuts import render,redirect,get_object_or_404
from .models import Userperson, Product, OrderedProduct, FinalOrder, NotifyParty, Consignee
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User, auth
from django.template import loader
from django.templatetags.static import static
from django.http import HttpResponse
from django.conf import settings
from django.utils import timezone
from decimal import Decimal
import random
import string
import zoneinfo

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
            request.session['addedproduct'] = None

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
            request.session['addedproduct'] = None
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
    
def showNotify(request):
    condition = True
    parties = NotifyParty.objects.all()
    many = len(parties) > 0

    return render(request, 'Inventory/notifyparties.html',{
        'C' : condition,
        'P' : parties,
        'many' : many
    })

def AddNotify(request):
    condition = True
    edit = False
    if request.method == 'POST':
        name = request.POST.get('name')
        street = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        if name.strip() == "" or street.strip() == "" or city.strip() == "" or state.strip() == "":
            messages.info(request, 'No fields must be left blank')
            return redirect('addnotify')
        if request.POST.get('More') == 'More':
            party = NotifyParty.objects.create(
                Name = name,
                Street = street,
                City = city,
                State = state
            )
            party.Ad()
            return redirect('addnotify')
        else:
            party = NotifyParty.objects.create(
                Name = name,
                Street = street,
                City = city,
                State = state
            )
            party.Ad()
            return redirect('shownotify')
        
    else:
        return render(request, 'Inventory/addnotify.html',{
            'C' : condition,
            'edit' : edit
        })

def EditNotify(request, pk):
    condition = True
    edit = True
    chosen = get_object_or_404(NotifyParty, pk=pk)
    if request.method == 'POST':
        name = request.POST.get('name')
        street = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        if name.strip() == "" or street.strip() == "" or city.strip() == "" or state.strip() == "":
            messages.info(request, 'No fields must be left blank')
            return redirect('shownotify', pk)
        else:
            chosen.Name = name
            chosen.Street = street
            chosen.City = city
            chosen.State = state
            chosen.Ad()
            return redirect('shownotify')
    else:
        return render(request, 'Inventory/addnotify.html',{
            'C' : condition,
            'edit' : edit,
            'chosen' : chosen
        })
 
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
            request.session['addedproduct'] = None

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
            request.session['addedproduct'] = None

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
            request.session['addedproduct'] = None

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
            request.session['addedproduct'] = None

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
    status = ""
    if request.user.is_authenticated:
        condition = True
        Orders = FinalOrder.objects.filter(Finished = False)
        Products = Product.objects.filter(Stock__gte = 1).filter(Status = True)
   
        if request.method == "POST":
            OrderNum = request.POST.get('Order')
            if request.POST.get('proddrop') == "":
                messages.info(request,"Choose a product!")
                return redirect('createorder')
            
            
            request.session['Order'] = OrderNum
            request.session['rem'] = request.POST.get('rem')
            request.session['productname'] = request.POST.get('proddrop')
            ChosenProduct = get_object_or_404(Product, Name = request.session['productname'])
            return redirect('confirmcreateorder', pk=ChosenProduct.pk)
            
            

        else:
            return render(request,'Inventory/MakeOrder.html',{ 
                'O' : Orders,
                'P' : Products,
                'C' : condition,
                'status' : status
            })
        
def AddtoOrder(request,pk):
    condition = True
    status = 'adding'
    Order = get_object_or_404(FinalOrder, pk=pk)
    Prods = Product.objects.filter(Stock__gte = 1).filter(Status = True)
    request.session['NAVIGATE'] = 'confirmorder'
    if request.method == 'POST':
        prod = request.POST.get('prod')
        rem = request.POST.get('rem')
        if str(prod).strip() == "" or str(prod).strip() == "Choose a product:":
            messages.warning(request,'You must choose a product')
            return redirect('addtoorder', pk)
        
        request.session['prod'] = prod
        request.session['rem'] = rem
        product = get_object_or_404(Product, Name = prod)
        request.session['addedproduct'] = 'addedproduct'
        request.session['pk'] = Order.pk
        return redirect('confirmcreateorder', pk=product.pk)
    
    else:
        return render(request,'Inventory/Makeorder.html',{
            'C' : condition,
            'status' : status,
            'prods' : Prods,
            'pk' : Order.pk
        })
    


def ConfirmOrder(request,pk):
    remarks = request.session.get('Remarks') #remarks
    ChosenProduct = get_object_or_404(Product, pk=pk) #product
    stock = ChosenProduct.Stock
    stocka = []
    condition = ""

    for i in range(1,stock+1):
        stocka.append(i)
    if request.user.is_authenticated:
        condition = True
        request.session['NAVIGATE'] = "confirmorder"

        #If coming from adding a product to an order
        if request.session.get('addedproduct') == 'addedproduct':
            status = 'adding'
            order = request.session.get('pk')
            ChosenOrder = get_object_or_404(FinalOrder, pk=order)
            if request.method == 'POST':
                if request.POST.get('Back') == "Back":
                    print('GOING BACK')
                    return redirect('addtoorder', pk=order)
                
                q = request.POST.get('drop')
                Cost = request.POST.get('totalcost')[1:len(request.POST.get('totalcost'))]
                Cost = Decimal(Cost)
                rem = request.POST.get('Description')

                if str(rem).strip() == "":
                    remarks = "No remarks"
                else:
                    remarks = rem

                NewOrderProduct = OrderedProduct.objects.create(
                    OrderedProductID = VerifID(request),
                    OrderID = ChosenOrder,
                    Marks = ChosenProduct, 
                    remarks = remarks, 
                    quantity = q, 
                    totalcost = Cost, 
                    )
                
                NewOrderProduct.save()

                ChosenOrder.TotalCost += Cost
                ChosenOrder.save()

                if request.POST.get('More') == "More":
                    print('MORE')
                    return redirect('addtoorder', pk=order)
                    
                else:
                    return redirect('UnfTrans', pk=order)



            else:
                return render(request, 'Inventory/confirmcreateorder.html',{
                    'C' : condition,
                    'status' : status,
                    'OrderedP' : ChosenProduct,
                    'stocka' : stocka,
                    'Order' : ChosenOrder,
                })
        
        #Coming from confirming a new order
        else:
            status = 'confirming'
            if request.method == "POST":
                if request.POST.get('Back') == "Back":
                    print('GOING BACK')
                    request.session['Order'] = None
                    request.session['productname'] = None
                    return redirect('createorder')

                q = request.POST.get('drop')
                Cost = request.POST.get('totalcost')[1:len(request.POST.get('totalcost'))]
                Person = request.POST.get('Person')

                if str(Person).strip() == '' or str(Person).strip() == "Type new Consignee Name":
                    messages.info(request,"No proper fields for Consignee")
                    return redirect('confirmcreateorder', pk)

            
                Cost = Decimal(Cost)
            
                #Final Order Section         
                NewConsign = Consignee.objects.create(
                        BL = VerifBL(request),
                        Name = Person,
                    )
                NewConsign.save()

                timezone.activate('Asia/Taipei')

                NewOrder = FinalOrder.objects.create(
                        Verification = VerifID(request),
                        BL = NewConsign,
                        NumOfBL = 3,
                        Time = timezone.localtime()
                    )

                NewOrder.TotalCost += Cost
                NewOrder.PD()
                ChosenOrder = NewOrder
                    
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
                
                NewOrderProduct.save()

                if request.POST.get('More') == "More":
                    print('MORE')
                    return redirect('createorder')
                    
                else:
                    return redirect('Products')

        
            else:
                return render(request,'Inventory/confirmcreateorder.html',{
                    'OrderedP' : ChosenProduct,
                    'C' : condition,
                    'stocka' : stocka,
                    'Rem' : remarks,
                    'status' : status
                    })
        

def CompleteOrder(request,pk):
    condition = True
    parties = NotifyParty.objects.all()
    num = pk
    OrderDone = get_object_or_404(FinalOrder, pk=pk)
    if request.method == 'POST':
        shipper = request.POST.get('shipper')
        ocean = request.POST.get('ocean')
        local = request.POST.get('local')
        localorigin = request.POST.get('localorigin')

        notify = request.POST.get('notify')
        portload = request.POST.get('portload')
        portdis = request.POST.get('portdis')
        transhto = request.POST.get('transhto')
        finaldest = request.POST.get('finaldest')
        voyage = request.POST.get('voyage')

        prepaid = request.POST.get('prepaid')
        collect = request.POST.get('collect')
        charges = request.POST.get('charges')
        revtons = request.POST.get('revtons')
        rate = request.POST.get('rate')
        payat = request.POST.get('payat')

        if (charges == ""):
            charges = 0
        if (rate == ""):
            rate = 0

        if notify == "Select a Notify Party":
            messages.info(request, 'Select a valid Notify Party')
            return redirect('completeorder', pk)
        elif portload.strip() == "" or portdis.strip() == "" or voyage.strip() == "":
            messages.info(request, 'Port of Loading, Port of Discharge, or Voyage cannot be left blank')
            return redirect('completeorder', pk)
        elif (prepaid.strip() != "Yes" and collect.strip() != "Yes"):
            messages.warning(request, 'Both Prepaid and Collect cannot be null, one field must not be null')
            return redirect('completeorder',pk)

        else:
            outcome = True
            OrderedProds = OrderedProduct.objects.filter(OrderID = OrderDone)
            i = 0
            sum = 0
            hashmap = {}

            # O(n) algorithm as worst case 

            while i < len(OrderedProds):
                prod = OrderedProds[i]
                if prod.Marks.Name in hashmap:
                    ''' If the product name exists in the hashmap, then we will simply update their value,
                    but we will retain the old value in order to update'''
                    old = hashmap[prod.Marks.Name]
                    hashmap.update({prod.Marks.Name: old - prod.quantity})
                else:
                    ''' If product name doesn't exist yet in the hashmap, then we will
                    create a new key-value for it '''
                    hashmap.update({prod.Marks.Name: prod.Marks.Stock - prod.quantity })

                i = i + 1

            for val in hashmap.values():
                if val < 0:
                    outcome = False

            if outcome == False:
                print(hashmap)
                request.session['HM'] = hashmap #Hashmap Data
                request.session['PK'] = pk #Primary Key of Final Order
                return redirect('UnfTrans', pk)
        
         
            else:
                #O(n) algorithm
                for item in OrderedProds:
                    item.Marks.Stock -= item.quantity
                    item.Marks.save()
                    item.save()

            notifobject = get_object_or_404(NotifyParty, Name = notify)
            OrderDone.Portdis = portdis
            OrderDone.Portload = portload
            OrderDone.ShipperName = shipper
            OrderDone.OceanVessel = ocean
            OrderDone.LocalVessel = local
            OrderDone.LocalVesselOrigin = localorigin
            OrderDone.NotifyName = notifobject
            OrderDone.TranshTo = transhto
            OrderDone.FinalDest = finaldest
            OrderDone.Voyage = voyage

            OrderDone.Prepaid = prepaid
            OrderDone.Collect = collect
            OrderDone.Charges = charges
            OrderDone.RevTons = revtons
            OrderDone.Rate = rate
            OrderDone.PayAt = payat

            
            OrderDone.Finished = True

            OrderDone.save()
            print(OrderDone.pk)
            return redirect('Products2')
    else:
        return render(request, 'Inventory/finalize.html',{
            'C' : condition,
            'parties' : parties,
            'n' : num
        })

def ShowComplete(request):
    condition = True
    use = 'complete'
    DoneOrders = FinalOrder.objects.filter(Finished = True).order_by('-pk')
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
        error = request.session.get('HM')
        finalorderkey = request.session.get('PK')

        condition = True
        empty = len(Products) == 0

        if error != None:
            array = []
            #O(n)
            for item in error.keys():
                if error[item] < 0:
                    array.append((item, error[item]))
                    
            return render(request,'Inventory/cart.html',{ 
                    'C' : condition,
                    'Products' : Products,
                    'p' : pk,
                    'e' : empty,
                    'array' : array,
                    'orderkey' : finalorderkey

                })
        else:
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
            request.session['addedproduct'] = None

        return render(request,'Inventory/programmer.html',{
            'C' : condition
        })
    else:
        condition = False
        return render(request,'Inventory/programmer.html',{
            'C' : condition
        })


    