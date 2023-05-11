from django.test import TestCase
from decimal import Decimal

# Create your tests here.
try:
    num = '85.00'
    print(type(num) == str)
    print(Decimal(num) or int(num))
except:
    print('error')