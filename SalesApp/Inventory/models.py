from django.db import models
from django.core.validators import MinValueValidator, DecimalValidator
from PIL import Image
from django.conf.urls.static import static
from decimal import Decimal
from django.utils import timezone


class NotifyParty(models.Model):
    Name = models.CharField(max_length=100, unique=True)
    Street = models.CharField(max_length=100)
    City = models.CharField(max_length=100)
    State = models.CharField(max_length=100)
    Address = models.CharField(max_length=300)

    def Ad(self):
        self.Address = self.State + ", " + self.City + ", " + self.Street
        super(NotifyParty,self).save()

    objects = models.Manager()

class Consignee(models.Model):
    BL = models.CharField(max_length=20, default='', unique=True)
    Name = models.CharField(max_length=100)


class Product(models.Model): #Steels, not food 
    objects = models.Manager()
    Name = models.CharField(max_length=200, unique=True)
    Image = models.ImageField(default= "images/defproduct.jpg", blank=True, upload_to="images/") #not have image if we dont have one, uploaded to images folder automatically
    Manufacturer = models.CharField(default=None, max_length=100)
    ManuLoc = models.CharField(default=None,max_length=255)
    Status = models.BooleanField(default=True) #Records incase of removed

    Measurement = models.CharField(default=None, max_length=100)
    Description = models.CharField(default=None, max_length=1000)
    GrossWeight = models.CharField(default=None, max_length=100)

    Available = models.BooleanField(default=True)

    Marks = models.CharField(default=None, null=True, max_length=300) 
    def MakeMark(self):
        self.Marks = str(self.Manufacturer) + ", " + str(self.ManuLoc)
        super(Product,self).save() 
    
    Length = models.CharField(max_length=20)
    Cost = models.DecimalField(default=0, validators=[DecimalValidator(7,2)], decimal_places=2, max_digits=7) #declared value USD
    Stock = models.BigIntegerField(default=0)
    Contact = models.CharField(max_length=500)

    def Reduce(self,number):
        self.Stock = self.Stock - number
        super(Product, self).save()
    
    def WhatStatus(self):
        self.Status = self.Stock > 0
        super(Product,self).save()
        return self.Status


class Userperson(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birthday = models.DateField()
    sex = models.CharField(max_length=50)
    objects = models.Manager()
   

    def getUsername(self):
        return self.username

    def getPassword(self):
        return self.password
    
    def getFirstName(self):
        return self.first_name
    
    def getLastName(self):
        return self.last_name

    def getBirthday(self):
        return self.birthday

    def getSex(self):
        return self.sex

    def __str__(self):
        return 'pk' + ':' + ' ' + 'User ' + str(self.pk) + ':' + ' ' + str(self.username) + ',' + ' ' + str(self.first_name) + ' ' + str(self.last_name) + ',' + ' ' + str(self.birthday) + ',' + ' ' + str(self.sex)


#Create a model that is created upon "Add to Cart" button press designated for a user
#Null = True
#Shipper, NotifyName, PayAt, Charges, RevTons, Rate, Prepaid, Collect
#portload, portdis, transhto, FinalDest, Voyage
class FinalOrder(models.Model):
    ShipperName = models.CharField(max_length=100, default='', blank=True)
    OceanVessel = models.CharField(max_length=100, null=True, default='')

    TotalCost = models.DecimalField(default=0, validators=[DecimalValidator(10,2)], decimal_places=2, max_digits=10) 
    Finished = models.BooleanField(default=False) #confirmed or not
    OrderDate = models.DateField(auto_now_add=True)#auto_now_add=True)
    Time = models.TimeField(default=timezone.now()) 

    Verification = models.CharField(default='',unique=True, max_length=13, blank=True) #Orderid -> verification
    BL = models.ForeignKey(Consignee, null=False, blank=True, on_delete=models.CASCADE)

    NotifyName = models.ForeignKey(NotifyParty, default=None, on_delete=models.CASCADE, null=True, blank=True)
    NumOfBL = models.IntegerField(default=3, null=True, blank=True)
    PayAt = models.CharField(default='', max_length=255, null=True, blank=True)
    Place = models.CharField(default="Kaohsiung, Taiwan", max_length=255, null=False)
    PlaceDate = models.CharField(default='', max_length=100, blank=True)

    Charges = models.DecimalField(default=0.0, validators=[MinValueValidator(Decimal('0.01'))], null=True, blank=True, decimal_places=2, max_digits=8)
    RevTons = models.CharField(max_length=1000, default='', null=True, blank=True)
    Rate = models.DecimalField(default=0.0, null=True, blank=True, validators=[MinValueValidator(Decimal('0.01'))], decimal_places=2, max_digits=8)
    Prepaid = models.CharField(max_length=20, default='', blank=True)
    Collect = models.CharField(max_length=20, default='', blank=True)
    
    Portload = models.CharField(max_length=255, default='', blank=True)
    Portdis = models.CharField(max_length=255, default='', blank=True)
    TranshTo = models.CharField(max_length=255, default='', null=True, blank=True)
    FinalDest = models.CharField(max_length=255, default='', null=True, blank=True)
    Voyage = models.CharField(max_length=255, default='')

    def PD(self): #call this when confirming the order
        self.PlaceDate = str(self.Place) + ", " + str(self.OrderDate)
        super(FinalOrder,self).save()

    objects = models.Manager()


class OrderedProduct(models.Model):
    remarks = models.CharField(max_length=500, default='', null=True, blank=True)
    quantity = models.IntegerField(default=0)
    totalcost = models.DecimalField(default=0, validators=[DecimalValidator(10,2)], decimal_places=2, max_digits=10)

    #New Fields
    OrderedProductID = models.CharField(default=None, unique=True, max_length=13)
    OrderID = models.ForeignKey(FinalOrder, default=None, on_delete=models.CASCADE)
    Marks = models.ForeignKey(Product, on_delete=models.CASCADE)

    def getProduct(self):
        return self.Marks
    
    def getOrder(self):
        return self.OrderID

    objects = models.Manager()
    

