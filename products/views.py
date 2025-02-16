from django.shortcuts import render
from .forms import ProductFormSet  # Ensure you are importing from forms.py
from django.shortcuts import render, redirect

def add_products(request):
    formset = ProductFormSet()
    if request.method == "POST":
        formset = ProductFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                if form.cleaned_data.get("price"):  # Ensure price is not empty
                    form.save()
            return redirect("success_page")  # Change to the actual success page name

    return render(request, "products/add_products2.html", {"formset": formset})

from django.shortcuts import render

def success_page(request):
    return render(request, 'success.html')  # Make sure 'success.html' exists in your templates




from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import SignUpForm, LoginForm
from .models import CustomUser

def sign_up(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["pin"])  # Encrypt PIN
            user.save()
            login(request, user)
            return redirect("home")  # Redirect to home page
    else:
        form = SignUpForm()
    return render(request, "auth/signup.html", {"form": form})


def log_in(request):
    errors = []
    phone_number = ""
    phone_number = request.POST.get("phone_number", "").strip()
    pin = request.POST.get("pin", "").strip()
    print(phone_number,pin)
    print(request.method)
    if request.method == "POST":
        phone_number = request.POST.get("phone_number", "").strip()
        pin = request.POST.get("pin", "").strip()
        print(phone_number,pin)
        # Basic validations
        if not phone_number:
            errors.append("Phone number is required.")

        if not pin:
            errors.append("PIN is required.")
        elif len(pin) != 4 or not pin.isdigit():
            errors.append("PIN must be a 4-digit number.")

        # If there are no errors, perform login logic
        if not errors:
            # Example authentication logic (replace with your own)
            user = authenticate(phone_number=phone_number, pin=pin)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                 errors.append("Invalid phone number or PIN.")
            #For now, we'll simply redirect if there are no errors:
            return redirect("product_list")

    context = {
        "errors": errors,
        "phone_number": phone_number,
    }
    return render(request, "products/login.html", context)
def log_out(request):
    logout(request)
    return redirect("login")












from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.urls import path
from .models import Product
import json

def product_list(request):
    products = Product.objects.all().order_by("id")
    paginator = Paginator(products, 10)
    first_page = paginator.get_page(1)
    form = SignUpForm()
    return render(request, "products/index.html", {"products": first_page, "total_pages": paginator.num_pages,"form":form})
"""
def product_list_ajax(request, page):
    products = Product.objects.all().order_by("id")
    paginator = Paginator(products, 10)
    if page <= paginator.num_pages:
        page_obj = paginator.get_page(page)
        data = list(page_obj.object_list.values("id", "name", "price", "is_new", "is_old","image1", ))
        return JsonResponse({"products": data, "has_next": page_obj.has_next()})
    return JsonResponse({"products": [], "has_next": False})"""
from django.conf import settings
from django.db.models import F, Value
from django.db.models.functions import Concat

def product_list_ajax(request, page):
    products = Product.objects.all().order_by("id")
    paginator = Paginator(products, 10)
    
    if page <= paginator.num_pages:
        page_obj = paginator.get_page(page)
        data = list(
            page_obj.object_list.values("id" ,"name", "price", "is_new", "is_old")
        )

        # Convert Cloudinary image field to URL
        for item in data:
            product = Product.objects.get(id=item["id"])
            item["image1"] = product.image1.url if product.image1 else None
            #user=Product.objects.get(id=item["id"])
            item["user"]=str(product.user)

        return JsonResponse({"products": data, "has_next": page_obj.has_next()})

    return JsonResponse({"products": [], "has_next": False})


def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        product.name = request.POST.get("name", product.name)
        product.price = request.POST.get("price", product.price)
        product.is_new = request.POST.get("is_new") == "on"
        product.is_old = request.POST.get("is_old") == "on"
        product.save()
        return redirect('home')
    return render(request, "products/edit_product.html", {"product": product})

@csrf_exempt
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return JsonResponse({"success": True})
