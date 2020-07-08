from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect
import json
from django.views import generic
import datetime
from django.conf import settings
from .models import *
from .utils import cookieCart, cartData, guestOrder
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render
from .models import Image
from django import forms
from .forms import ImageUpload


def supplements(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    products = Supplement.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/supplements.html', context)


class SupplementDetail(generic.DetailView):
    model = Supplement
    template_name = 'store/supplement_detail.html'

    def get(self, request, slug):
        data = cartData(request)
        product = self.get_object(queryset=None)
        cartItems = data['cartItems']
        order = data['order']
        items = data['items']

        products = Supplement.objects.all()
        context = {'products': products, 'cartItems': cartItems, 'product': product}
        return render(request, 'store/supplement_detail.html', context)