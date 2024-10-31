from django.contrib import admin
from .models import *
from django.contrib.auth.models import Group
admin.site.unregister(Group)
# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(Feedback)