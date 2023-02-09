from django.db import models

# Create your models here.
class Product(models.Model): #Steels, not food 
    objects = models.Manager()
    Name = models.CharField(max_length=30, unique=True)
    Image = models.ImageField(null= True, blank=True, upload_to="images/") #not have image if we dont have one, uploaded to images folder automatically
    Manufacturer = models.CharField(max_length=30)
    Length = models.CharField(max_length=20)
    Cost = models.CharField(max_length=10)
    Stock = models.BigIntegerField()
    Description = models.CharField(null=True, max_length=500)
    Contact = models.CharField(null= True, max_length=500)


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
    TotalCost = models.CharField(max_length=20)
    ProductInfo = models.CharField(max_length=400)
    Finished = models.IntegerField(default=0) #0 is for not yet finished
    objects = models.Manager()


class OrderedProduct(models.Model):
    Client = models.ForeignKey(Userperson, on_delete=models.CASCADE)
    Order = models.ForeignKey(Product, on_delete=models.CASCADE)
    remarks = models.CharField(max_length=200)
    quantity = models.IntegerField(default=0)
    totalcost = models.IntegerField(default=0)
    Finalorder = models.ForeignKey(FinalOrder, on_delete=models.PROTECT, default=None)
    objects = models.Manager()
    

