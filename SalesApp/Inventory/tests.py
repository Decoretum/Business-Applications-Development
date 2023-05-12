from django.test import TestCase
from decimal import Decimal

# Create your tests here.
try:
    num = '85.00'
    print(type(num) == str)
    print(Decimal(num) or int(num))
except:
    print('error')


def hasnumber(request,string):
    return any(i.isdigit() for i in string)


print(hasnumber(request='you',string = "Mama123"))