from django.db import models
from django.core.validators import MinValueValidator
from PIL import Image

'''
Models that are active for confirmation of order:
    Company, Notify Party, Consignee

    Ordered Product will update its voyage number

'''
class Company(models.Model):
    ShipperName = models.CharField(max_length=30)
    OceanVessel = models.CharField(max_length=50)
    LocalVessel =  models.CharField(max_length=50, null=True)
    LocalVesselOrigin = models.CharField(max_length=50, null=True)
    objects = models.Manager()

class NotifyParty(models.Model):
    Name = models.CharField(max_length=50, unique=True)
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
    PortDischarge = models.CharField(max_length=100, default='', blank=True)


class Product(models.Model): #Steels, not food 
    objects = models.Manager()
    Name = models.CharField(max_length=200, unique=True)
    Image = models.ImageField(default=None, null= True, blank=True, upload_to="images/") #not have image if we dont have one, uploaded to images folder automatically
    Manufacturer = models.CharField(default=None, max_length=100)
    ManuLoc = models.CharField(default=None,max_length=255)
    Color = models.CharField(default=None, max_length=20)
    Status = models.BooleanField(default=True) #Records incase of removed

    Measurement = models.CharField(default=None, max_length=30)
    Description = models.CharField(default=None, max_length=500)
    GrossWeight = models.CharField(default=None, max_length=40)

    Marks = models.CharField(default=None, null=True, max_length=300) 
    def MakeMark(self):
        self.Marks = str(self.Manufacturer) + ", " + str(self.ManuLoc) + ", " + str(self.Color)
        super(Product,self).save() 
    
    Length = models.CharField(max_length=20)
    Cost = models.CharField(max_length=10) #declared value USD
    Stock = models.BigIntegerField(default=0)
    Contact = models.CharField(max_length=500)
    
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
class FinalOrder(models.Model):
    TotalCost = models.IntegerField(default=0) 
    ProductInfo = models.CharField(max_length=400, blank=True,default=None)
    Finished = models.BooleanField(default=False) #confirmed or not
    OrderDate = models.DateField(auto_now_add=True)#auto_now_add=True)

    Verification = models.CharField(default=None,unique=True, max_length=13, null=True, blank=True) #Orderid -> verification
    BL = models.ForeignKey(Consignee, null=False, blank=True, on_delete=models.CASCADE)

    Shipper = models.ForeignKey(Company, on_delete=models.CASCADE, default=None, null=True, blank=True)
    NotifyName = models.ForeignKey(NotifyParty, default=None, on_delete=models.CASCADE, null=True, blank=True)
    NumOfBL = models.IntegerField(default=3, null=True, blank=True)
    PayAt = models.CharField(default='', max_length=70, null=True, blank=True)
    Place = models.CharField(default="Kaohsiung, Taiwan", max_length=70, null=False)
    PlaceDate = models.CharField(default='', max_length=100, blank=True)

    Charges = models.FloatField(default=None, max_length=11, validators=[MinValueValidator(float('0.01'))], null=True, blank=True)
    RevTons = models.CharField(max_length=1000, default=None, null=True, blank=True)
    Rate = models.FloatField(default=None, null=True, blank=True, validators=[MinValueValidator(float('0.01'))])
    Prepaid = models.CharField(max_length=20, default='', blank=True)
    Collect = models.CharField(max_length=20, default='', blank=True)
    
    Portload = models.CharField(max_length=255, default='', blank=True)
    Portdis = models.CharField(max_length=255, default='', blank=True)
    TranshTo = models.CharField(max_length=50, default='', null=True, blank=True)
    FinalDest = models.CharField(max_length=255, default='', null=True, blank=True)
    Voyage = models.SmallIntegerField(default=0, null=False, blank=True)

    def PD(self): #call this when confirming the order
        self.PlaceDate = str(self.Place) + ", " + str(self.OrderDate)
        super(FinalOrder,self).save()

    objects = models.Manager()


class OrderedProduct(models.Model):
    remarks = models.CharField(max_length=200)
    quantity = models.IntegerField(default=0)
    totalcost = models.IntegerField(default=0)

    #New Fields
    OrderedProductID = models.CharField(default=None, unique=True, max_length=13)
    OrderID = models.ForeignKey(FinalOrder, default=None, on_delete=models.CASCADE)
    Marks = models.ForeignKey(Product, on_delete=models.CASCADE)


    objects = models.Manager()
    

