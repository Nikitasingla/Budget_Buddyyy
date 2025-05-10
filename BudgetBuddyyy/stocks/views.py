from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from mainpage.views import register_view,login_view,logout_view
import requests
from django.http import HttpResponse

# Create your views here.

def homed(request):
    return render(request,'home.html')

# views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Stock, CartItem

def stock_list(request):
    stocks = Stock.objects.all()
    return render(request, 'stock_list.html', {'stocks': stocks})

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from .models import Stock, CartItem

@login_required
def add_to_cart(request, stock_id):
    stock = get_object_or_404(Stock, id=stock_id)
    item, created = CartItem.objects.get_or_create(user=request.user, stock=stock)

    if not created:
        item.quantity += 1
        item.save()
    return redirect('cart_view')

@login_required
def cart_view(request):
    items = CartItem.objects.filter(user=request.user)
    grand_total = sum(item.get_total_price() for item in items)
    return render(request, 'cart.html', {'items': items, 'grand_total': grand_total})
@login_required
def delete_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()
    return redirect('cart_view')
@login_required
def search_stock_view(request):
    stock=None
    error=None
    data=[]

    try:
        response=requests.get('http://127.0.0.1:5000/api/stock/')
        if response.status_code==200:
            data=response.json()
    except Exception as e:
        error="Unable to fetch Stock list"
    if request.method=='POST':
        symbol=request.POST.get('symbol','').upper()
        if not symbol:
            error="Please enter a stock symbol"
        else:
            try:
              api_url=f'http://127.0.0.1:5000/api/stock/{symbol}'
              response=requests.get(api_url)

              if response.status_code==200:
                  stock=response.json()
              else:
                  error=response.json().get("error","Stock not found")
            except requests.exceptions.RequestException as e:
                error=f"Could not connect to stock API : {e}"
        
    return render(request,'stocked.html',{
        'stock':stock,'error':error,'all_stocks':data
    })
from .models import BoughtStocks
from django.views.decorators.csrf import csrf_exempt

@login_required
def buy_stock(request):
    if request.method=="POST":
        symbol=request.POST.get('symbol','').upper()
        try:
            response=requests.get(f'http://127.0.0.1:5000/api/stock/{symbol}')
            if response.status_code==200:
                stock_data=response.json()
                price=stock_data.get('price',0)
                BoughtStocks.objects.create(user=request.user,symbol=symbol,price=price)
                return redirect('bought_stocks')
            else:
                return render(request,'stocked.html',{'error':'Stock not found '})
        except Exception:
            return render(request,'stocked.html',{'error':'API error occured'})
    return render(request,'stocked.html')

@login_required
def bought_stocks_view(request):
    bought_entries=BoughtStocks.objects.filter(user=request.user)
    symbols=[b.symbol for b in bought_entries]

    bought_stocks=[]
    try:
        response=requests.get('http://127.0.0.1:5000/api/stock/')
        if response.status_code==200:
            all_stocks=response.json()
            bought_stocks=[s for s in all_stocks if s["symbol"] in symbols]
    except Exception:
        pass

    return render(request,'bought.html',{
        'bought_stocks':bought_stocks,'user_entries':bought_entries
    })

@login_required
def add_stock_view(request):
    if not request.user.is_staff:
        return HttpResponse("Unauthorized access-Admins only",status=403)
    
    if request.method=="POST":
        symbol=request.POST.get('symbol')
        price=request.POST.get('price')
        open_price=request.POST.get('open')
        high=request.POST.get('high')
        low=request.POST.get('low')
        image_url=request.POST.get('image_url')

        new_stock={
            "symbol":symbol,"price":price,"open":open_price,"high":high,"low":low,"image_url":image_url
        }
        try:
            response=requests.post(f'http://127.0.0.1:5000/api/stock/',json=new_stock)
            print(f'response code{response.status_code}')
        except Exception:
            return HttpResponse("Failed to connect to API",status=500)
        return redirect('search_stock')
    return render(request,'add_pro.html')

@login_required 
def update_stocks(request,symbol):
    if not request.user.is_staff:
        return HttpResponse("Unauthorized access-Admins only",status=403)
    if request.method=="POST":
        symbol=request.POST.get('symbol')
        price=request.POST.get('price')
        open_price=request.POST.get('open')
        high=request.POST.get('high')
        low=request.POST.get('low')
        image_url=request.POST.get('image_url')


        updated_stock={
            "symbol":symbol,
            "price":price,
            "open":open_price,
            "high":high,
            "low":low,
            "image_url":image_url
        }
        try:
            response=requests.put(f'http://127.0.0.1:5000/api/stock/{symbol}',json=updated_stock)
        except Exception:
            return HttpResponse("Failed to connect to Flask API",status=500)
        return redirect('search_stock')
    return render(request,'update.html')

@login_required
def delete_stock(request,symbol):
    if not request.user.is_staff:
        return HttpResponse("Unauthorised access-only for admins",status=403)
    try:
        response=requests.delete(f'http://127.0.0.1:5000/api/stock/{symbol}')
    except Exception:
        return HttpResponse("Failed to connect to API",status=500)
    return redirect('search_stock')
    
