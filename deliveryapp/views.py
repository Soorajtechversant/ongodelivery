import json
import stripe
from .forms import  *
from .models import *
from cmd import IDENTCHARS
from requests import request  
from itertools import product
from django.conf import settings
from django.urls import reverse_lazy
from django.views.generic import View
from django.views import View , generic
from xmlrpc.client import FastMarshaller
from django.contrib import auth , messages
from django.http import HttpResponse, JsonResponse
from distutils.sysconfig import customize_compiler
from django.contrib.auth import authenticate, login 
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group , User, auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import ListView, CreateView, DetailView, TemplateView, DeleteView




class Registration(View):
    def get(self, request):
        return render(request,'products/registration/registration.html')
    def post(self, request):
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username is already exist')
                return redirect('products/registration/registration')
            else:
                user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
                user.save()
                messages.info(request, 'customer registered')
                return redirect("products/registration/login")
        else:
            messages.info(request,'password is not matching')
            return redirect('products/registration/registration')


class Customer_index(ListView):
    context_object_name  = 'textile'
    queryset = Ongo.objects.all()
    template_name  = "products/customer/customer_index.html"


class Login(View):
    def get(self, request):
        return render(request,'products/registration/login.html')
    def post(self, request):
        if request.method=='POST':
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if username == 'manager' and password == 'manager':
                auth.login(request, user)
                return redirect('products/productshop_owner/owner_index')
            elif user is not None:
                auth.login(request, user)
                return redirect("products/customer/customer_index")
            else:
                messages.info(request,'Invalid Credentials......')
                return redirect("products/registration/login")
        
# The logout class
class Logout(View):
    def get(self, request):
        auth.logout(request)
        return redirect('/')



@login_required
def settings(request):
    membership = False
    cancel_at_period_end = False
    if request.method == 'POST':
        subscription = stripe.Subscription.retrieve(request.user.customer.stripe_subscription_id)
        subscription.cancel_at_period_end = True
        request.user.customer.cancel_at_period_end = True
        cancel_at_period_end = True
        subscription.save()
        request.user.customer.save()
    else:
        try:
            if request.user.customer.membership:
                membership = True
            if request.user.customer.cancel_at_period_end:
                cancel_at_period_end = True
        except Customer.DoesNotExist:
            membership = False
    return render(request, 'settings.html', {'membership':membership,
    'cancel_at_period_end':cancel_at_period_end})



# This class will show the product details in admin index page
class Owner_index(ListView):
    context_object_name  = 'textile'
    queryset = Ongo.objects.all()
    template_name = "products/productshop_owner/owner_index.html"

# This class will add the product details
class Add_product(View):
    form_class = OngoForm
    def get(self, request):
        OngoForm = self.form_class()
        return render(request, "products/productshop_owner/add_product.html", {'form': OngoForm})
    def post(self, request):
        if request.method == 'POST':
            form = self.form_class(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('products/productshop_owner/owner_index')
            else:
                return redirect('products/productshop_owner/add_product')
      

# This class will delete the product details
class Delete_product(View):
    def get(self, request, id):
        textile = Ongo.objects.get(id=id)
        textile.delete()
        return redirect("products/productshop_owner/owner_index")


# This class will edit/update the product details
class Edit_product(View):
    def get(self, request, id):
        textile = Ongo.objects.get(id=id) 
        form = OngoForm(instance=textile)
        return render(request, 'products/productshop_owner/edit_product.html', {'form':form})
    def post(self, request, id):
        if request.method == 'POST':
            textile = Ongo.objects.get(id=id)
            form = OngoForm(request.POST,request.FILES, instance=textile)
            print(form)
            if form.is_valid():
                form.save()
                return redirect("products/productshop_owner/owner_index")



