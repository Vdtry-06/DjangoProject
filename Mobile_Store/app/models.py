from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm 

import numpy as np
import cv2

class Category(models.Model):
    trademark = models.ForeignKey('self', on_delete = models.CASCADE, related_name = 'trademarks', null = True, blank = True)
    is_trademark = models.BooleanField(default = False)
    name = models.CharField(max_length = 200, null = True)
    slug = models.SlugField(max_length = 200, unique = True)
    def __str__(self):
        return self.name
    
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
   
class Product(models.Model):
    category = models.ManyToManyField(Category, related_name = 'product')
    name = models.CharField(max_length = 200, null = True)
    price = models.FloatField()
    image = models.ImageField(null = True, blank = True)
    image_features = models.BinaryField(null=True, blank=True)
    operating_system = models.CharField(max_length=50, blank=True, null=True)
    graphics_chip = models.CharField(max_length=50, blank=True, null=True)
    cpu_speed = models.CharField(max_length=100, blank=True, null=True)
    ram = models.CharField(max_length=10, blank=True, null=True)
    color = models.CharField(max_length=20, blank=True, null=True)
    MEMORY_CHOICES = [
        ('32GB', '32 GB'),
        ('64GB', '64 GB'),
        ('128GB', '128 GB'),
        ('256GB', '256 GB'),
        ('512GB', '512 GB'),
        ('1TB', '1 TB'),
    ]
    memory = models.CharField(max_length = 5, choices = MEMORY_CHOICES, default = '64GB')
    
    def __str__(self):
        return self.name
    @property
    def ImageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    
    def extract_features(self):
        if self.image:
            try:
                image_data = self.image.read()
                if image_data:
                    img = cv2.imdecode(np.frombuffer(image_data, np.uint8), cv2.IMREAD_COLOR)
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    sift = cv2.SIFT_create()
                    keypoints, descriptors = sift.detectAndCompute(gray, None)
                    if descriptors is not None:
                        self.image_features = descriptors.tobytes()
            except Exception as e:
                print(f"Error processing image for product {self.name}: {e}")
    
    def save(self, *args, **kwargs): # nhận các tham số không xác định
        if self.image:
            self.extract_features() # trích xuất hình ảnh được tải lên
        super().save(*args, **kwargs) # lưu đối tượng vào cơ sở dữ liệu
    
class Order(models.Model):
    customer = models.ForeignKey(User, on_delete = models.SET_NULL, null = True, blank = True)
    date_ordered = models.DateTimeField(auto_now_add = True)
    complete = models.BooleanField(default = False, null = True, blank = False)
    transaction_id = models.CharField(max_length = 200, null = True)

    def __str__(self):
        return f'Order #{self.id} by {self.customer.username if self.customer else "Guest"}'
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total   
    
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete = models.SET_NULL, null = True, blank = True)
    order = models.ForeignKey(Order, on_delete = models.SET_NULL, null = True, blank = True)
    quantity = models.IntegerField(default = 0, null = True, blank = True)
    date_added = models.DateTimeField(auto_now_add = True)
    
    @property
    def get_total(self):
        if self.product is not None:
            total = self.product.price * self.quantity
        else:
            total = 0
        return total
    
class ShippingAddress(models.Model):
    customer = models.ForeignKey(User, on_delete = models.SET_NULL, null = True, blank = True)
    order = models.ForeignKey(Order, on_delete = models.SET_NULL, null = True, blank = True)
    address = models.CharField(max_length = 200, null = True)
    Country = models.CharField(max_length = 200, null = True)
    State = models.CharField(max_length = 200, null = True)
    Mobile = models.CharField(max_length = 10, null = True)
    added_date = models.DateTimeField(auto_now_add = True)
    
    def __str__(self):
        return self.address if self.address else 'No address provided'

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    feedback_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Feedback from {self.user.username}'