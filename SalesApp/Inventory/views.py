from django.contrib import messages
from django.shortcuts import render,redirect,get_object_or_404
from .models import Userperson, Product, OrderedProduct, FinalOrder, NotifyParty, Consignee
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.models import User, auth
from django.template import loader
from django.templatetags.static import static
from django.http import HttpResponse
from django.conf import settings
from django.utils import timezone
from decimal import Decimal
import random
import string


def home(request):
    condition = ''
    use = "home"
    
    #This state checks if there is a user logged in for the application
    if request.user.is_authenticated: 
        condition = True
        
        '''This is something will be seen in a lot of views functions
        This ensures that server data during the filling up of forms will be reset in case you navigate to another
        page'''
        if request.session.get('NAVIGATE') == "confirmorder" or request.session.get('NAVIGATE') == "confirmtrans":
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
        condition = False
        return render(
            request, 'Inventory/home.html', {
            'C' : condition,
            'use' : use
            })

def Clerk(request):
    if request.session.get('NAVIGATE') == "confirmorder" or request.session.get('NAVIGATE') == "confirmtrans":
        request.session['Remarks'] = None
        request.session['productname'] = None
        request.session['OrderedPRem'] = None
        request.session['OrderPname'] = None
        request.session['manufacturer'] = None
        request.session['Order'] = None
        request.session['addedproduct'] = None
    return render(
            request,'Inventory/clerk.html',{
                'C' : True,
                'username' : request.session['user'],
                'userid' : request.session['userid'],
                'password' : request.session['password'],
                'firstname' : request.session['firstname'],
                'lastname' : request.session['lastname'],
                'birthday' : request.session['birthday'],
                'sex' : request.session['sex'],
            }
        )

''' 
A very efficient way to check if a field is a Decimal or not
Decimal was used instead of float due to the precision of Decimal, providing precise and accurate values
in compensation for some performance 
'''
def isDigit(request,num):
    try:
        #type(result) == int or type(result) == Decimal 
        "-" not in num and (Decimal(num) or int(num))
        return True
    except:
        return False
    

#Notify Party section
    
def showNotify(request):
    parties = NotifyParty.objects.all()
    many = len(parties) > 0

    return render(request, 'Inventory/notifyparties.html',{
        'C' : True,
        'P' : parties,
        'many' : many
    })

def AddNotify(request):
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
                Name = name.strip(),
                Street = street.strip(),
                City = city.strip(),
                State = state.strip()
            )
            party.Ad() #model function to create a derived value
            return redirect('addnotify')
        else:
            party = NotifyParty.objects.create(
                Name = name.strip(),
                Street = street.strip(),
                City = city.strip(),
                State = state.strip()
            )
            party.Ad()
            return redirect('shownotify')
        
    else:
        return render(request, 'Inventory/addnotify.html',{
            'C' : True,
            'edit' : edit
        })

def EditNotify(request, pk):
    edit = True
    chosen = get_object_or_404(NotifyParty, pk=pk)
    if request.method == 'POST':
        name = request.POST.get('name').strip()
        street = request.POST.get('street').strip()
        city = request.POST.get('city').strip()
        state = request.POST.get('state').strip()
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
            'C' : True,
            'edit' : edit,
            'chosen' : chosen
        })
    

#Products Section    
 
def AddProduct(request):
    if request.method == "POST":
        imgfile = request.FILES.get('Image')         
        name = request.POST.get('Name').strip()
        length = request.POST.get('Length').strip()
        manufacturer = request.POST.get('Manufacturer').strip()
        manuloc = request.POST.get('Location').strip()
        color = request.POST.get('Color').strip()
        cost = request.POST.get('Cost')
        stock = request.POST.get('Stock')
        desc = request.POST.get('Description').strip()
        contact = request.POST.get('Contact').strip()
        meas = request.POST.get('Measurement').strip()
        weight = request.POST.get('Weight').strip()

        if name.strip() == "" or length.strip() == ""  or manufacturer.strip() == "" or manuloc.strip() == "" or color.strip() == "" or cost.strip() == "" or desc.strip() == "" or contact.strip() == "" or meas.strip() == "" or weight.strip() == "":
            messages.info(request, 'You must fill out all the fields')
            return redirect('addproduct')

        elif isDigit(request,num = str(cost)) == False:
            messages.warning(request,"Input cost was not a number")
            return redirect('addproduct')


        elif Decimal(cost) <= 0:
            messages.warning(request,"No negative costs or costs equal to 0")
            return redirect('addproduct')

        elif isDigit(request, num = str(stock)) == False:
            messages.error(request, "Stock cannot be text")
            return redirect('addproduct')
        
        elif stock == "" or stock == None or "." in stock or int(stock) <= 0:
            messages.error(request, 'Stock must not be blank, a decimal, or <= 0')
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

        '''If the image field wasn't filled up by the user, then there will be a default image field
         if it is filled up by the user, then file from HTML field will be image field  '''
        if imgfile != None:
            New.Image = imgfile

        New.MakeMark()
        return redirect ('Products')
    
    else:
        return render(
            request, 'Inventory/AddProd.html',{
            'C' : True
                }
            )

def EditProduct(request,pk):
    Existing = get_object_or_404(Product, pk=pk)
    if request.session.get('NAVIGATE') == "confirmorder" or request.session.get('NAVIGATE') == "confirmtrans":
        request.session['Remarks'] = None
        request.session['productname'] = None
        request.session['OrderedPRem'] = None
        request.session['OrderPname'] = None
        request.session['manufacturer'] = None
        request.session['Order'] = None
        request.session['addedproduct'] = None

    if request.method == "POST":
        imgfile = request.FILES.get('Image')
        name = request.POST.get('Name').strip()
        length = request.POST.get('Length').strip()
        manufacturer = request.POST.get('Manufacturer').strip()
        manuloc = request.POST.get('Location').strip()
        color = request.POST.get('Color')
        cost = request.POST.get('Cost')
        contact = request.POST.get('Contact').strip()

        desc = request.POST.get('Description').strip()
        meas = request.POST.get('Measurement').strip()
        weight = request.POST.get('Weight').strip()
        stock = request.POST.get('stock')

        if name.strip() == "" or length.strip() == ""  or manufacturer.strip() == "" or manuloc.strip() == "" or color.strip() == "" or cost.strip() == "" or desc.strip() == "" or contact.strip() == "" or meas.strip() == "" or weight.strip() == "":
            messages.info(request, 'You must fill out all the fields')
            return redirect('editproduct',pk)

        elif isDigit(request,num = str(cost)) == False:
            messages.error(request,"Input cost was not a valid number")
            return redirect('editproduct', pk)

        elif Decimal(cost) <= 0:
            messages.error(request,"No negative costs or costs equal to 0")
            return redirect('editproduct', pk)
        
        elif isDigit(request, num = str(stock)) == False:
            messages.warning(request, "Stock cannot be text")
            return redirect('editproduct', pk)
        
        elif stock == "" or stock == None or "." in stock or int(stock) < 0:
            messages.warning(request, 'Stock must not be blank, a decimal, or <= 0')
            return redirect('editproduct', pk)

        Existing.Name = name

        if imgfile != None:
            Existing.Image = imgfile
        
        Existing.Stock += int(stock)
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
            'C' : True,
            'Prod' : Existing
                }
            )

def delProduct(request,pk):
    Deleted = get_object_or_404(Product, pk=pk)
    if request.user.is_authenticated:
        Deleted.Status = False
        Deleted.save()
        return redirect('Products')


def Products(request):
    use = 'home'
    P = Product.objects.filter(Status = True).order_by('-Stock')
    length = len(P)
    if request.user.is_authenticated:
        condition = True
        if request.session.get('NAVIGATE') == "confirmorder" or request.session.get('NAVIGATE') == "confirmtrans":
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
            'username' : request.session['user'],
            'use' : use,
            'L' : length
            })
    else:
        condition = False   
        return render(request, 'Inventory/products.html',{
            'C' : condition,
            'P':P, 
            #'url':settings.MEDIA_URL,
            'use' : use,
            "L" : length
            })
    



#Authentication Section

def Signup(request):
    if request.method == 'POST':
        username = request.POST.get('usern').strip()
        password = request.POST.get('passn').strip()
        first_name = request.POST.get('firstn').strip()
        last_name = request.POST.get('lastn').strip()
        birthday = request.POST.get('birthday1')
        sex = request.POST.get('sexx').strip()

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
        username = request.POST.get('username').strip()
        password = request.POST.get('password').strip()
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
According to Django documentation:
When you call logout(), the session data for the current request is completely cleaned out. 
All existing data is removed. This is to prevent another person from using the same web browser to log in 
and have access to the previous user’s session data. 
If you want to put anything into the session that will be available 
to the user immediately after logging out, do that after calling django.contrib.auth.logout().
'''
def logoutuser(request):
    logout(request)
    return redirect('Login')
    


#Displaying Section

def ShowProds(request):
    if request.session.get('NAVIGATE') == "confirmorder" or request.session.get('NAVIGATE') == "confirmtrans":
        request.session['Remarks'] = None
        request.session['productname'] = None
        request.session['OrderedPRem'] = None
        request.session['OrderPname'] = None
        request.session['manufacturer'] = None
        request.session['Order'] = None
        request.session['addedproduct'] = None

    request.session['NAVIGATE'] = "users"
    errorproducts = set() #Set for no duplicates
    i = 0
    AllOrders = FinalOrder.objects.filter(Finished = False)

    #This is O(n)
    AllSubOrders = OrderedProduct.objects.all()
    while i < len(AllSubOrders):
        finalorder = AllSubOrders[i].OrderID 
        if finalorder.Finished == False:
            product = AllSubOrders[i].Marks
            if product.Status == False:
                errorproducts.add(finalorder.pk)
        i += 1

  
    length = len(AllOrders)
    pk = request.session.get('PK')
    if pk != None:
        return render(request, 'Inventory/users2.html',{
                'C' : True,
                'Orders' : AllOrders,
                'L' : length,
                'primary' : pk,
                'array' : errorproducts
            })
    else:
        return render(request, 'Inventory/users2.html',{
                'C' : True,
                'Orders' : AllOrders,
                'L' : length,
                'array' : errorproducts
            })

'''def ProdsinOrder(request, pk):
    Ordered = OrderedProduct.objects.filter(OrderID = pk)
    empty = len(Ordered) == 0
    return render(request, 'Inventory/ProductsinOrder.html',{
        'C' : True,
        'Ordered' : Ordered,
        'e' : empty
    })'''

def ShowComplete(request):
    condition = True
    use = 'complete'
    DoneOrders = FinalOrder.objects.filter(Finished = True).order_by('-pk')
    OrderedP = OrderedProduct.objects.all()
    length = len(DoneOrders)
    if request.user.is_authenticated:
        pass
        return render(request, 'Inventory/products.html',{
            'use' : use,
            'C' : condition,
            'O' : DoneOrders,
            'Ord' : OrderedP,
            'L' : length
        })


def Info(request,pk):
    condition = ""
    CurrentProd = get_object_or_404(Product, pk=pk)
    if request.user.is_authenticated:
        condition = True
        if request.session.get('NAVIGATE') == "confirmorder" or request.session.get('NAVIGATE') == "confirmtrans":
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
    

'''
Information about the App or related
'''
def Developer(request):
    condition = ''
    if request.user.is_authenticated:
        condition = True

        if request.session.get('NAVIGATE') == "confirmorder" or request.session.get('NAVIGATE') == "confirmtrans":
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
    

    
#Data Generation Section

#Creates a randomized ID with a length of 13 consisting of letters and integers
def VerifID(request): 
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

#Similar to VerifID, but the length is 20
def VerifBL(request): 
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



# Order Management Section
'''
First phase of Order creation
- This contains the user's input for Product and remarks that will be available so that the next
phase of order creation will display data based on the the first phase's input

- Request data are initialized for the second phase to adapt to the request data
'''
def CreateOrder(request):
    status = ""
    condition = True
    Products = Product.objects.filter(Stock__gte = 1).filter(Status = True)

    if request.method == "POST":
        if request.POST.get('proddrop') == "":
            messages.info(request,"Choose a product!")
            return redirect('createorder')
        
        
        request.session['rem'] = request.POST.get('rem').strip()
        request.session['productname'] = request.POST.get('proddrop')
        ChosenProduct = get_object_or_404(Product, Name = request.session['productname'])
        return redirect('confirmcreateorder', pk=ChosenProduct.pk)
        
        

    else:
        return render(request,'Inventory/MakeOrder.html',{ 
            'P' : Products,
            'C' : condition,
            'status' : status
        })
    
'''
This is the alternative of the first phase of order creation
- This function will occur if you're adding a product to an existing order 
(Adding OrderedProduct object to FinalOrder object)
- Identical functionalities and fields as the CreateOrder() function
'''
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

'''
This is the second phase of Order Creation
- Data is queried based on the request data and primary key of the 1st order creation phase
- This is where the OrderedProduct and Final Order will be initialized
- 2 Scenarios:
    1. Confirming an Order creation from a brand new order (Final Order object)
    2. Adding an OrderedProduct to an already existing Final Order

- if scenario is 1, then:
    - HTML will automatically detect that the clerk is confirming a brand new order
    - You will see that the Chosen product and its price will appear
    - Quantity available to be chosen will be based on the database's query on available stock of the product
    - Fields for Consignee name, quantity to be ordered, and remarks will appear
    - Timezone will be set to Taipei/Asia so that the Final Order object's time will be based on that
    - You will have to fill up Consignee name since this is a brand new order

- if scenario is 2, then:
    - Data displayed will be the same as scenario 1, but you cannot edit Consignee name since the order
    has already been initialized
    - When submitting this, the ordered product will be created and will be added under the order that you're
    adding an ordered product with
'''
def ConfirmOrder(request,pk):
    remarks = request.session.get('rem') #remarks
    ChosenProduct = get_object_or_404(Product, pk=pk) #product
    stock = ChosenProduct.Stock
    stocka = []

    for i in range(1,stock+1):
        stocka.append(i)

    request.session['NAVIGATE'] = "confirmorder"

    #If coming from adding a product to an order, scenario 2
    if request.session.get('addedproduct') == 'addedproduct':
        status = 'adding'
        order = request.session.get('pk')
        ChosenOrder = get_object_or_404(FinalOrder, pk=order)
        if request.method == 'POST':
            if request.POST.get('Back') == "Back":
                return redirect('addtoorder', pk=order)
            
            q = request.POST.get('drop')
            Cost = request.POST.get('totalcost')[1:len(request.POST.get('totalcost'))]
            Cost = Decimal(Cost)
            rem = request.POST.get('Description').strip()

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
                return redirect('addtoorder', pk=order)
                
            else:
                return redirect('UnfTrans', pk=order)

        else:
            return render(request, 'Inventory/confirmcreateorder.html',{
                'C' : True,
                'status' : status,
                'OrderedP' : ChosenProduct,
                'stocka' : stocka,
                'Order' : ChosenOrder,
                'remarks' : remarks
            })
    
    #Coming from confirming a new order, or Scenario 1
    else:
        status = 'confirming'
        if request.method == "POST":
            if request.POST.get('Back') == "Back":
                request.session['Order'] = None
                request.session['productname'] = None
                request.session['Remarks'] = None
                return redirect('createorder')

            q = request.POST.get('drop')
            Cost = request.POST.get('totalcost')[1:len(request.POST.get('totalcost'))]
            Person = request.POST.get('Person').strip()

            if str(Person).strip() == '' or str(Person).strip() == "Type new Consignee Name":
                messages.info(request,"No proper fields for Consignee")
                return redirect('confirmcreateorder', pk)

        
            Cost = Decimal(Cost)
        
            #Final Order Section         
            human = "noone"
            people = Consignee.objects.all()
            i = 0

            while i < len(people):
                if people[i].Name == Person:
                    human = people[i]
                    break
                i += 1

            if human == "noone":
                NewConsign = Consignee.objects.create(
                    BL = VerifBL(request),
                    Name = Person,
                )
                NewConsign.save()
            else:
                NewConsign = human
    
            
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
            remarks = request.POST.get('Description').strip()

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
                return redirect('createorder')
                
            else:
                return redirect('Products')

    
        else:
            remarks = request.session.get('rem').strip()
            return render(request,'Inventory/confirmcreateorder.html',{
                'OrderedP' : ChosenProduct,
                'C' : True,
                'stocka' : stocka,
                'remarks' : remarks,
                'status' : status
                })
    
        
'''
Completing phase of an order
- This will confirm the order (FinalOrder object), including the OrderedProduct objects within the order
- certain fields can be null, but not all can be null
- If the OrderedProducts of a FinalOrder has a quantity sum greater than the available stock of a certain
product, then an error will pop up, and it will show in the view/edit section of an order in "Pending Orders"
'''
def CompleteOrder(request,pk):
    OrderDone = get_object_or_404(FinalOrder, pk=pk)
    Ordered = OrderedProduct.objects.filter(OrderID = OrderDone)

    #Algorithm for checking if a product is deleted or not
    for order in Ordered:
        if order.Marks.Status == False:
            return redirect('UnfTrans', pk=OrderDone.pk)
    

    '''
    O(n) algorithm as worst case 
    Hashmap will be used in order to store data for every specific product
    that OrderedProducts would contain, no matter how few or many OrderedProducts there is
    '''

    outcome = True
    OrderedProds = OrderedProduct.objects.filter(OrderID = OrderDone)
    i = 0
    hashmap = {}

    while i < len(OrderedProds):
        prod = OrderedProds[i]
        prodobj = prod.Marks
        if prodobj.Name in hashmap:
            ''' If the product name exists in the hashmap, then we will simply update their value,
            but we will retain the old value in order to update'''
            old = hashmap[prodobj.Name]
            hashmap.update({prodobj.Name: old - prod.quantity})
        else:
            ''' If product name doesn't exist yet in the hashmap, then we will
            create a new key-value for it '''
            hashmap.update({prodobj.Name: prodobj.Stock - prod.quantity })

        i = i + 1

    '''
    A negative value in a hashmap would mean that the total quantity sum of a product in
    the entirety of a FinalOrder is greater than number of Stock available for that product 
    ''' 

    #O(n) algorithm
    for val in hashmap.values():
        if val < 0:
            outcome = False


    if outcome == False:
        request.session['HM'] = hashmap #Hashmap Data
        request.session['PK'] = pk #Primary Key of Final Order
        return redirect('UnfTrans', pk)

    
    else:
        request.session['HM'] = None
        request.session['PK'] = None
        condition = True
        parties = NotifyParty.objects.all()
        num = pk

        if request.method == 'POST':
            shipper = request.POST.get('shipper').strip()
            ocean = request.POST.get('ocean').strip()

            notify = request.POST.get('notify').strip()
            portload = request.POST.get('portload').strip()
            portdis = request.POST.get('portdis').strip()
            transhto = request.POST.get('transhto').strip()
            finaldest = request.POST.get('finaldest').strip()
            voyage = request.POST.get('voyage').strip()

            prepcol = request.POST.get('fin')

            charges = request.POST.get('charges').strip()
            revtons = request.POST.get('revtons').strip()
            rate = request.POST.get('rate').strip()
            payat = request.POST.get('payat').strip()

            if (charges == ""):
                charges = 0
            if (rate == ""):
                rate = 0


            if notify == "Select a Notify Party":
                messages.info(request, 'Select a valid Notify Party')
                return redirect('completeorder', pk)
            
            elif portload.strip() == "" or portdis.strip() == "" or voyage.strip() == "" or shipper == "":
                messages.info(request, 'Shipper Company, Port of Loading, Port of Discharge, and Voyage cannot be left blank')
                return redirect('completeorder', pk)
            
            elif (prepcol == None):
                messages.warning(request, 'Both Prepaid and Collect cannot be null, one field must not be null')
                return redirect('completeorder',pk)

            elif isDigit(request,num = str(voyage)) == False:
                messages.warning(request,"Voyage was not a valid number")
                return redirect('completeorder', pk)
            
            elif voyage == "" or voyage == None or "." in voyage or int(voyage) < 0:
                messages.warning(request, 'Voyage must not be blank, a decimal, or <= 0')
                return redirect('completeorder', pk)
            
            elif isDigit(request,num = str(charges)) == False:
                messages.warning(request,"Charges was not a valid number")
                return redirect('completeorder', pk)
            
            elif charges == "" or charges == None or Decimal(charges) < 0:
                messages.warning(request, 'Charges cannot be less than 0')
                return redirect('completeorder', pk)
            
            elif isDigit(request,num = str(rate)) == False:
                messages.warning(request,"Rate was not a valid number")
                return redirect('completeorder', pk)
            
            elif rate == "" or rate == None or Decimal(rate) < 0:
                messages.warning(request, 'Rate cannot be less than 0')
                return redirect('completeorder', pk)

            #elif True != False:
            #    print('RESET')
            #    print(type(rate))
            #    print(Decimal(rate) + 10)
            #    print(Decimal(charges) + 10)
            #    print(type(charges))
            #    return redirect('completeorder', pk)



            else:
                notifobject = get_object_or_404(NotifyParty, Name = notify)

                #O(n) algorithm, very efficient
                for name in hashmap.keys():
                    product = get_object_or_404(Product, Name = name)
                    product.Stock = hashmap[name]
                    product.save()

                if prepcol == 'collect':
                    OrderDone.Collect = 'Yes'
                else:
                    OrderDone.Prepaid = 'Yes'

                OrderDone.Portdis = portdis
                OrderDone.Portload = portload
                OrderDone.ShipperName = shipper
                OrderDone.OceanVessel = ocean
                OrderDone.NotifyName = notifobject
                OrderDone.TranshTo = transhto
                OrderDone.FinalDest = finaldest
                OrderDone.Voyage = voyage

                OrderDone.Charges = charges
                OrderDone.RevTons = revtons
                OrderDone.Rate = rate
                OrderDone.PayAt = payat

                
                OrderDone.Finished = True

                OrderDone.save()
                return redirect('Products2')
                
        else:
            return render(request, 'Inventory/finalize.html',{
                'C' : condition,
                'parties' : parties,
                'n' : num
            })



#OrderedProduct Section
    
# Deleting of OrderedProduct obejct
def DeleteTrans(request,pk):
    TobeDel = get_object_or_404(OrderedProduct, pk=pk)
    Order = get_object_or_404(FinalOrder, pk=TobeDel.OrderID.pk)
    Order.TotalCost -= TobeDel.totalcost
    Order.save()
    TobeDel.delete()
    return redirect('UnfTrans', pk=Order.pk)

'''
Interface to show the OrderedProducts within a order (FinalOrder)
- if you came from confirming an order, but an error has been caused due to the the 
OrderedProducts having a higher total sum quantity than a product/s's available stock, then
you will see an error

- Array was used to store data for a product and an integer that represents its error on quantity 
'''
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
   

'''
First phase of editing an OrderedProduct
- Similar to first phase of Order creation, fields for this phase will be used to get user data
that will determine what data will be displayed on the second phase
- The OrderedProduct to be edited is already determined
- We get the data for Product name and remarks
'''
def ChangeTrans(request,pk):
    condition = ""
    ChosenTrans = get_object_or_404(OrderedProduct, pk=pk)
    Ordernum = ChosenTrans.OrderID.pk
    if ChosenTrans.Marks.Status == False:
        return redirect('UnfTrans', pk=Ordernum)
    
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
        condition = True
        
        request.session['OrderedPRem'] = ChosenTrans.pk
        request.session['OrderPname'] = request.POST.get('proddrop')
        request.session['manufacturer'] = request.POST.get('Manufacturer')
        request.session['Remarks'] = request.POST.get('Description').strip()
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


'''
Second phase of editing an OrderedProduct
- Similar to how orders are confirmed, the data from the first phase of editing an orderedproduct
will be fetched from the database to be displayed on this second phase

'''
def ConfirmTrans(request,pk):
    ChosenTrans = get_object_or_404(OrderedProduct, pk=request.session.get('OrderedPRem')) #Orderedproduct
    orderprodname = request.session.get('OrderPname') #Orderedproductpk
    remarks = request.session.get('Remarks').strip() #remarks
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
            if Newproduct.Status == False:
                messages.info(request,'You cant confirm transaction with a deleted product')
                return redirect('confirmorder', pk=Order.pk)
            cost = request.POST.get('totalcost')
            Newremarks = request.POST.get('Description').strip()
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
          




    