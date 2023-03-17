from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json

from .models import *

def home(request):
    products = Product.objects.all()
    if request.user.is_authenticated:
        customer = request.user.customer
    else :
        customer = ""
    context = {'products': products,
                'customer': customer}
    
    return render(request, 'core/home.html', context)

def shopping_cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer)
        items = order.orderitem_set.all()
    else:
        customer = ""
        items = []
        order = {'get_cart_total': 0}

    context = {'items': items,
               'customer': customer,
               'order': order}
    return render(request, 'core/shopping_cart.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customerName = request.user.customer
    product = Product.objects.get(id=productId)

    order, created = Order.objects.get_or_create(customer=customerName)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)
