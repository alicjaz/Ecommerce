from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.db.models import Q

from .forms import SignUpForm
from .models import Category, Product


def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})


def about(request):
    return render(request, 'about.html', {})


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']  # Keep this as lowercase 'password'
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in!")
            return redirect('home')
        else:
            messages.error(request, "There was an error, please try again.")
            return redirect('login')
    else:
        return render(request, 'login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out... Thanks for stopping by")
    return redirect('home')


def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # log in user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You have registered successfully! Welcome")
        else:
            messages.success(request, "Whoops! There was a problem registering. Please, try again")
            return redirect('register')
    else:
        return render(request, 'register.html', {'form': form})


def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product': product})


def category(request, foo):
    foo = foo.replace('-', ' ')
    try:
        # Look Up The Category (Case-insensitive)
        category = Category.objects.filter(Q(name__iexact=foo)).first()

        if category is not None:
            products = Product.objects.filter(category=category)
            return render(request, 'category.html', {'products': products, 'category': category})
        else:
            raise Category.DoesNotExist

    except Category.DoesNotExist:
        messages.success(request, "That Category Doesn't Exist...")
        return redirect('home')
