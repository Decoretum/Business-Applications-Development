from django.db import models
from django.core.validators import MinValueValidator

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
    BL = models.CharField(max_length=20, unique=True)
    Name = models.CharField(max_length=100,unique=True)
    PortDischarge = models.CharField(max_length=100)


class Product(models.Model): #Steels, not food 
    objects = models.Manager()
    Name = models.CharField(max_length=200, unique=True)
    Image = models.ImageField(default="N/A", null= True, blank=True, upload_to="images/") #not have image if we dont have one, uploaded to images folder automatically
    
    Manufacturer = models.CharField(default=None, max_length=100)
    ManuLoc = models.CharField(default=None,max_length=255)
    Color = models.CharField(default=None, max_length=20)

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
    ProductInfo = models.CharField(max_length=400)
    Finished = models.IntegerField(default=0) #0 is for not yet finished
    OrderDate = models.DateField(auto_now_add=True)#auto_now_add=True)

    Verification = models.CharField(default=None,unique=True, max_length=13) #Orderid -> verification
    
    Shipper = models.ForeignKey(Company, on_delete=models.CASCADE, default=None)
    NotifyName = models.ForeignKey(NotifyParty, default=None, on_delete=models.CASCADE)
    BL = models.CharField(max_length=20, unique=True)
    NumOfBL = models.IntegerField(default=3, null=True)
    PayAt = models.CharField(default=None, max_length=70, null=True)
    Place = models.CharField(default=None, max_length=70)
    PlaceDate = models.CharField(default=None, max_length=100)

    Charges = models.FloatField(default=None, max_length=11, validators=[MinValueValidator(float('0.01'))], null=True)
    RevTons = models.CharField(max_length=1000, default=None, null=True)
    Rate = models.FloatField(default=None, null=True, validators=[MinValueValidator(float('0.01'))])
    Prepaid = models.CharField(max_length=20, default=None)
    Collect = models.CharField(max_length=20, default=None)
    
    Portload = models.CharField(max_length=255, default=None)
    Portdis = models.CharField(max_length=255, default=None)
    TranshTo = models.CharField(max_length=50, default=None, null=True)
    FinalDest = models.CharField(max_length=255, default=None, null=True)
    Voyage = models.SmallIntegerField(default=0)

    def PD(self): #call this when confirming the order
        self.PlaceDate = self.Place + ", " + self.OrderDate
        super(FinalOrder,self).save()

    FreightsCharges = models.FloatField(default=None, null=True)
    Collect = models.CharField(max_length=70, default=None)

    objects = models.Manager()


class OrderedProduct(models.Model):
    remarks = models.CharField(max_length=200)
    quantity = models.IntegerField(default=0)
    totalcost = models.IntegerField(default=0)

    #New Fields
    OrderedProductID = models.CharField(default=None, unique=True, max_length=13)
    Verificaton = models.ForeignKey(FinalOrder, default=None, on_delete=models.CASCADE)
    Marks = models.ForeignKey(Product, on_delete=models.CASCADE)


    objects = models.Manager()
    

