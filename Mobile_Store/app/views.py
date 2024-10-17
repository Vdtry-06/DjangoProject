from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from .models import *
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth import authenticate, login, logout 
from django.contrib import messages
from django.core.paginator import Paginator

import json

import numpy as np
import cv2
from ultralytics import YOLO
from sklearn.metrics.pairwise import cosine_similarity
from .forms import ImageSearchForm
# Create your views here.

def extract_features_from_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Chuyển đổi ảnh gốc sang màu xám
    sift = cv2.SIFT_create()  # Khởi tạo SIFT
    keypoints, descriptors = sift.detectAndCompute(gray, None)  # Phát hiện các đặc trưng và tính toán mô tả
    
    if descriptors is None:  # Kiểm tra nếu không phát hiện được đặc trưng
        return None
    if descriptors.shape[0] > 1:  # Đảm bảo rằng kích thước là (1, 128)
        descriptors = descriptors.mean(axis=0).reshape(1, -1)  # Nếu có nhiều đặc trưng, chỉ lấy trung bình
    return descriptors

def image_search(request):
    form = ImageSearchForm()
    keys = []
    searched = None
    if request.method == 'POST':
        form = ImageSearchForm(request.POST, request.FILES)
        if form.is_valid():
            image_file = form.cleaned_data['image']
            # Đọc ảnh tải lên vào mảng NumPy
            img = cv2.imdecode(np.frombuffer(image_file.read(), np.uint8), cv2.IMREAD_COLOR)
            if img is None:
                searched = "Định dạng ảnh không hợp lệ."
            else:
                check = False
                model = YOLO('yolov8n.pt')
                results = model(img)  # Truyền ảnh gốc vào mô hình
                for result in results:
                    result.show()
                    class_names = result.names
                    detected_objects = result.boxes.cls.tolist()
                    detected_names = [class_names[int(idx)] for idx in detected_objects]
                    # print("Tên các đối tượng phát hiện:", detected_names)
                    if "cell phone" in detected_names:
                        check = True
                        break

                if check:
                    query_features = extract_features_from_image(img)  # Chuyển đổi sang màu xám và trích xuất các đặc trưng
                    if query_features is None:
                        searched = "Không phát hiện được đặc trưng nào trong ảnh tải lên."  # Không trích xuất được đặc trưng
                    else:
                        products = Product.objects.all()
                        similarities = []

                        for product in products:
                            if product.image_features:
                                stored_features = np.frombuffer(product.image_features, dtype=np.float32).reshape(-1, 128)
                                if stored_features.shape[1] != 128:
                                    continue  # Bỏ qua sản phẩm nếu kích thước không hợp lệ

                                similarity = cosine_similarity(query_features, stored_features).mean()
                                print(similarity)
                                if similarity > 0.5:  # Chỉ xem xét các sản phẩm có độ tương đồng > 0.5         
                                    similarities.append((similarity, product))

                        similarities.sort(reverse=True, key=lambda x: x[0])  # Sắp xếp theo độ tương đồng giảm dần
                        keys = [product for _, product in similarities[:8]]  # Lấy 8 sản phẩm tương tự nhất

                        if not keys:  # Kiểm tra nếu không tìm thấy sản phẩm nào tương tự
                            searched = "không tìm thấy."
                        else:
                            searched = "Danh sách sản phẩm tương tự nhất đã được tìm thấy."
                else:
                    searched = "Không phát hiện được 'cellphone' trong ảnh tải lên."

    context = {
        'form': form,
        'keys': keys,
        'searched': searched,
    }
    return render(request, 'app/image_search.html', context)

def category(request):
    categories = Category.objects.filter(is_trademark = False)
    active_category = request.GET.get('category', '')
    trademark_name = request.GET.get('trademark', '')
    if active_category:
        products = Product.objects.filter(category__slug = active_category)
    else:
        products = Product.objects.all()
    context = {
        'categories': categories, 
        'products': products, 
        'active_category': active_category, 
        'trademark_name': trademark_name
    }
    return render(request, 'app/category.html', context)
    
def search(request):
    if request.method == "POST":
        searched = request.POST["searched"]
        keys = Product.objects.filter(name__contains = searched)
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {
            'get_cart_item': 0, 
            'get_cart_total': 0
        }
    categories = Category.objects.filter(is_trademark = False)
    products = Product.objects.all()
    return render(request, 'app/search.html', {
        "categories" : categories,
        "searched" : searched, 
        "keys" : keys, 
        "products": products
    })
    
def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'app/register.html', context)
    
def loginPage(request):
    if request.user.is_authenticated:
        return redirect("home")
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username = username, password = password)
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                messages.info(request, 'user or password not correct!')
    context = {}
    return render(request, 'app/login.html', context)

def logoutPage(request):
    logout(request)
    return redirect("home")

def home(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {
            'get_cart_item': 0, 
            'get_cart_total': 0
        }
    categories = Category.objects.filter(is_trademark = False)
    products = Product.objects.all().order_by('id')

    # Sử dụng Paginator để phân trang
    paginator = Paginator(products, 20)  # Mỗi tranga có 20 sản phẩm
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    context = {
        'categories': categories,
        'products': products,
        'items': items,
        'order': order,
    }
    return render(request, 'app/home.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {
            'get_cart_item': 0, 
            'get_cart_total': 0
        }
    categories = Category.objects.filter(is_trademark = False)
    context = {
        'categories': categories,
        'items': items, 
        'order': order
    }
    return render(request, 'app/cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {
            'get_cart_item': 0, 
            'get_cart_total': 0
        }
    categories = Category.objects.filter(is_trademark = False)
    context = {
        'categories': categories,
        'items': items, 
        'order': order
    }
    return render(request, 'app/checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customer = request.user
    product = Product.objects.get(id = productId)
    order, created = Order.objects.get_or_create(customer = customer, complete = False)
    orderItem, created = OrderItem.objects.get_or_create(order = order, product = product)
    
    if action == 'add':
        orderItem.quantity += 1
        
    elif action == 'remove':
        orderItem.quantity -= 1
        
    orderItem.save()
    
    if orderItem.quantity <= 0:
        orderItem.delete()
    
    return JsonResponse('added', safe = False)