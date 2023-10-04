from django.shortcuts import render, redirect
from django.urls import reverse
import yfinance as yf
import datetime

from django.contrib import messages
from django.http import JsonResponse


from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.decorators import login_required
from .forms import UserForm
from .decorators import unauthenticated_user


import random


# from bokeh.plotting import figure , output_file, show

# from bokeh.embed import components
# import pandas as pd
# from math import pi


# from .utils import get_data, convert_to_df


tickers = ['AAPL','AMZN','MSFT','GOOGL','AMD','META','NFLX','IBM','NVDA','INTC']


@login_required(login_url='login')
def index(request):
    return redirect(reverse("stock",kwargs={'pk':random.choice(tickers)}))


@login_required(login_url='login')
def stock(request,pk):
    stock = yf.Ticker(pk)
    close = "{:.2f}".format(stock.history(period='1d').Close.values.tolist()[0])   

    today = datetime.date.today().strftime('%m-%d-%Y')
    year_ago = (datetime.date.today() - datetime.timedelta(days=365)).strftime('%m-%d-%Y')

    context = { 'ticker': pk,'today': today, 'year_ago': year_ago, 'stock':stock.info, 'close':close}
    return render(request,'stock.html',context) 


@login_required(login_url='login')
def search(request):
    query = request.GET.get("query")
    return redirect(reverse("stock", kwargs= {'pk':str(query)}))


@login_required(login_url='login')
def loadstock(request):
    #function to handle ajax request for the plot of price history
    pk = request.GET.get("ticker", None)
    start = datetime.datetime.strptime(request.GET.get("start", None), '%m-%d-%Y')
    finish = datetime.datetime.strptime(request.GET.get("finish", None), '%m-%d-%Y')
    if(start > finish):
        return JsonResponse({'error':'Finish date is sooner than start date'},status=400) 
    stock = yf.Ticker(pk)
    if stock is None:
        return JsonResponse({'error':'Ticker not found'},status=404)
    data = stock.history(start = start.strftime('%Y-%m-%d'), end = finish.strftime('%Y-%m-%d'))
    index = list(data.index.strftime('%Y-%m-%d %H'))
    print(index)
    close = data.Close.values.tolist()
    print(close)
    open = data.Open.values.tolist()
    high = data.High.values.tolist()
    low = data.Low.values.tolist()
    return JsonResponse( {pk :{'index': index, 'close': close, 'open': open,'high': high, 'low': low}}, status = 200)


@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username  = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password= password)

        if user == None:
             messages.error(request, 'Login information incorrect')
             return redirect('login')
        login(request,user)
        return redirect('index')
    context = {}
    return render(request, 'login.html', context)


@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('login')


@unauthenticated_user
def registerPage(request):
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Your account was created')
            return redirect('login')
        messages.error(request, 'Your password or user is invalid')
        return redirect('register')
    context = {'form' : form}
    return render(request, 'register.html', context)