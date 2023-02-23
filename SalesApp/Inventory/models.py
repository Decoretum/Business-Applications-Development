from django.db import models

class Company(models.Model):
    ShipperName = models.CharField(max_length=30)
    OceanVessel = models.CharField(max_length=50)
    LocalVessel =  models.CharField(max_length=50)
    LocalVesselOrigin = models.CharField(max_length=50)
    objects = models.Manager()

class NotifyParty(models.Model):
    Name = models.CharField(max_length=50)
    Address = models.CharField(max_length=50)
    objects = models.Manager()

class Consignee(models.Model):
    BL = models.CharField(max_length=20, unique=True)
    Name = models.CharField(max_length=30,unique=True)
    PortDischarge = models.CharField(max_length=50)


class Product(models.Model): #Steels, not food 
    objects = models.Manager()
    Name = models.CharField(max_length=30, unique=True)
    Image = models.ImageField(null= True, blank=True, upload_to="images/") #not have image if we dont have one, uploaded to images folder automatically
    Manufacturer = models.CharField(max_length=30)
    Marks = models.CharField(max_length=50, unique=True) #manufacturer, location of manufacturer, color mark
    Length = models.CharField(max_length=20)
    Cost = models.CharField(max_length=10) #declared value USD
    Stock = models.BigIntegerField()
    Description = models.CharField(max_length=500)
    Contact = models.CharField(max_length=500)

#Products Composite Models

class Product_desc(models.Model):
    Description = models.CharField(max_length=500)
    Marks = models.ForeignKey(Product.Marks, on_delete=models.CASCADE)

class Product_Measurement(models.Model):
    Measurement = models.CharField(max_length=30)
    Marks = models.ForeignKey(Product.Marks, on_delete=models.CASCADE)

class Product_GrossWeight(models.Model):
    GrossWeight = models.CharField(max_length=40)
    Marks = models.ForeignKey(Product.Marks, on_delete=models.CASCADE)




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
    #New Fields
    Place = models.CharField(max_length=50)
    NumOfBL = models.IntegerField(default=3)
    PayAt = models.CharField(max_length=40)
    PlaceDate = models.CharField()

    def PD(self): #call this when confirming the order
        self.PlaceDate = self.Place + ", " + self.OrderDate
        super(FinalOrder,self).save()
    FreightsCharges = models.FloatField(default=None)
    Verification = models.CharField(max_length=13, null=True) #Orderid -> verification
    Shipper = models.ForeignKey(Company.ShipperName, on_delete=models.CASCADE)
    BL = models.ForeignKey(Consignee.BL, on_delete=models.CASCADE)
    NotifyName = models.ForeignKey(NotifyParty.Name, on_delete=models.CASCADE)
    Marks = models.ForeignKey(Product.Marks, on_delete=models.CASCADE) 
    objects = models.Manager()


class OrderedProduct(models.Model):
    Order = models.ForeignKey(Product, on_delete=models.CASCADE)
    remarks = models.CharField(max_length=200)
    quantity = models.IntegerField(default=0)
    totalcost = models.IntegerField(default=0)
    Finalorder = models.ForeignKey(FinalOrder, on_delete=models.CASCADE, default=None)
    #New Fields
    BL = models.CharField(max_length=20, unique=True)
    Verificaton = models.ForeignKey(FinalOrder.Verification, on_delete=models.CASCADE)
    Marks = models.ForeignKey(FinalOrder.Verification, on_delete=models.CASCADE)
    Voyage = models.IntegerField(default=0)

    objects = models.Manager()
    

