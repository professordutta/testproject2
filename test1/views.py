from django.shortcuts import render, HttpResponse, redirect
from .models import Product, Contact_Query
from django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
# Create your views here.

def home(request):
    product_info = Product.objects.all()
    # print(product_info)
    return render(request,'test1/home.html', {'product_info':product_info})
    # return HttpResponse('<h1>Home Page</h1>')   

def findproduct(request):
    if request.method == 'POST':
        x = request.POST.get('prod_search')
        # print(x)
        mydata = Product.objects.filter(Q(product_name__icontains = x) | Q(product_category__icontains = x) | Q(product_id__icontains = x) )
        # print(mydata)
        if mydata:
            return render(request,'test1/home.html', {'product_info':mydata})
        else:
            return render(request,'test1/home.html', {'warning':'No Record Found'})
           

def contact(request):
    return HttpResponse('Contact Page')

@login_required(login_url="loginuser")
def products(request):
    myproducts = Product.objects.all()
    paginator = Paginator(myproducts, 3)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request,'test1/product.html', {"page_obj": page_obj})

def contact(request):
    if request.method == 'GET':
        return render(request,'test1/contact.html')
    else:
        a = request.POST.get('name')
        b = request.POST.get('email')
        c = request.POST.get('message')
        new_data = Contact_Query(name=a, email=b, message=c)
        new_data.save()
        return render(request,'test1/contact.html',{'x':'Message Sent Successfully'})

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'test1/loginuser.html', {'form':AuthenticationForm()})
    else:
        a = request.POST.get('username')
        b = request.POST.get('password')
        user = authenticate(request, username=a, password=b)
        if user is None:
            return render(request,'test1/loginuser.html', {'form':AuthenticationForm(), 'error':'Invalid Credentials'})
        else:
            login(request, user)
            return redirect('home')

def signupuser(request):
    if request.method == 'GET':
        return render(request, 'test1/signupuser.html', {'form':UserCreationForm()})   
    else:
        a = request.POST.get('username')
        b = request.POST.get('password1')
        c = request.POST.get('password2')
        if b==c:
                # check whether user name is unique
            if (User.objects.filter(username = a)):
                return render(request,'test1/signupuser.html', {'form':UserCreationForm(), 'error':'User Name Already exists Try again with different username'})
            else:
                user = User.objects.create_user(username = a, password=b)
                user.save()
                login(request,user)
                return redirect('home')
        else:
            # password 1 and 2 do not match
            return render(request,'test1/signupuser.html', {'form':UserCreationForm(), 'error':'Password Mismatch Try Again'})   

def logoutuser(request):
    if request.method == 'GET':
        logout(request)
        return redirect('home')



