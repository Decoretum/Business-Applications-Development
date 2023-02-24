from django.contrib import admin
from . models import Product, Userperson, OrderedProduct, FinalOrder, NotifyParty, Company, Consignee
# Register your models here.

admin.site.register(Product)
admin.site.register(Userperson)
admin.site.register(OrderedProduct)
admin.site.register(FinalOrder)
admin.site.register(NotifyParty)
admin.site.register(Company)
admin.site.register(Consignee)