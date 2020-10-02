from django.shortcuts import render
from django.http import HttpResponse
from utils.stock_monitor import draw_company_stock_price, clear_graph, send_email
import io
import matplotlib.pyplot as plt
import urllib, base64
import matplotlib.pyplot as plt


def show_price(request):
    return render(request, 'stock_price/show_price.html')


def on_click(request):
    uri = None
    if (request.GET.get('confirm')):
        # plot stock price
        company_name = request.GET.get('company_name')
        duration = request.GET.get('duration')
        uri = draw_company_stock_price(company_name, duration)

        email_flag = request.GET.get('send_email')
        email_address = request.GET.get('email_address')
        if email_flag == 'on':
            send_email(email_address)

    if (request.GET.get('clear')):
        clear_graph()
        uri = None
        
    return render(request, 'stock_price/show_price.html', {'data' : uri})\


