from django.shortcuts import render, redirect
from . import models
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


from .models import Customer, Order, UserExtension
from .forms import CustomerForm, OrderForm, RegisterForm


@login_required()
def homepage(request):
    order = models.Order.objects.all()
    customer = models.Customer.objects.all()

    o_count = order.count()
    o_pending_count = order.filter(status='pending').count()
    o_out_delivery_count = order.filter(status='out of delivery').count()
    o_delivered_count = order.filter(status='delivered').count()

    c_count = models.Customer.objects.count()

    last_five = []
    i = 0
    for c in reversed(order):
        if i < 5:
            last_five.append(c)
            i = i + 1
        else:
            break

    # ajax 删除订单
    if request.is_ajax() and request.POST.get('order_id'):
        del_order_id = request.POST.get('order_id')
        del_order = Order.objects.get(id=del_order_id)
        del_order.delete()

    context = {
        'customer': customer,
        'o_count': o_count,
        'c_count': c_count,
        'o_pending_count': o_pending_count,
        'o_out_delivery_count': o_out_delivery_count,
        'o_delivered_count': o_delivered_count,
        'last_five': last_five,
    }
    return render(request, 'orderSystem/home.html', context)


def register(request):
    r_form = RegisterForm()

    message = ''

    # 非登录状态才能注册
    if request.session.get('id') is not None:
        return redirect('/') #登录中返回主页

    if request.method == 'POST':
        r_form = RegisterForm(request.POST)
        if r_form.is_valid():
            name_get = r_form.cleaned_data['username']
            password1_get = r_form.cleaned_data['password1']
            password2_get = r_form.cleaned_data['password2']
            phone_get = r_form.cleaned_data['phone']
            email_get = r_form.cleaned_data['email']
            # if RegisterForm.filter(name=name_get).exists():
            #     message = '该用户名已使用'

            try:
                if password1_get == password2_get:
                    new_user = User.objects.create_user(username=name_get, password=password1_get, email=email_get)
                    new_user.save()
                    UserExtension.objects.create(user=new_user, phone=phone_get).save()
                else:
                    message = '两次输入的密码不一致'
            except:
                message = '用户名和邮箱已被注册'


    context = {
        'r_form': r_form,
        'message': message
    }

    return render(request, 'orderSystem/register.html', context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('orderSystem:homepage')
    else:
        message = ''
        if request.method == 'POST':
            username_get = request.POST.get('username')
            password_get = request.POST.get('password')
            print(password_get)
            user = authenticate(request, username=username_get, password=password_get)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('orderSystem:homepage')
                else:
                    message = '账号已冻结'
            else:
                message = '用户名或密码错误'

    context = {
        'message': message
    }
    return render(request, 'orderSystem/loginpage.html', context)


def logout_view(request):
    logout(request)
    return redirect('orderSystem:login_page')


@login_required()
def modify_password(request):
    message = ''

    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        repeat_password = request.POST.get('repeat_password')

        print(old_password)
        print(new_password)
        print(repeat_password)

        user = authenticate(request, username=request.user.username, password=old_password)
        if user is not None:
            if user.is_active:
                if new_password == repeat_password:
                    user.set_password(new_password)
                    user.save()
                    return redirect('orderSystem:login_page')
                else:
                    message = '两次输入的密码不一致'
            else:
                message = '账号被冻结'
        else:
            message = '用户不存在'
    context = {
        'message': message
    }
    return render(request, 'orderSystem/modify_password.html', context)



@login_required()
def create(request):
    c_form = CustomerForm()
    o_form = OrderForm()

    if request.method == 'POST':
        if 'c_button' in request.POST:
            c_form = CustomerForm(request.POST)
            if c_form.is_valid():
                name_get = c_form.cleaned_data['name']
                phone_get = c_form.cleaned_data['phone']
                email_get = c_form.cleaned_data['email']
                customer = Customer.objects.create(name=name_get, phone=phone_get, email=email_get)
                customer.save()
                return redirect('orderSystem:homepage')

        if 'o_button' in request.POST:
            print(request.POST)
            o_form = OrderForm(request.POST)
            if o_form.is_valid():
                customer_get = o_form.cleaned_data['customer']
                product_get = o_form.cleaned_data['product']
                status_get = o_form.cleaned_data['status']
                order = Order.objects.create(customer=customer_get, product=product_get, status=status_get)
                order.save()
                return redirect('orderSystem:homepage')

    context = {
        'c_form': c_form,
        'o_form': o_form
    }

    return render(request, 'orderSystem/create.html', context)


@login_required()
def view_customer(request, customer_id):
    customer = Customer.objects.get(pk=customer_id)

    context = {
        'customer': customer
    }
    return render(request, 'orderSystem/viewcustomer.html', context)


@login_required()
def update_order(request, order_id):
    order = Order.objects.get(id=order_id)

    o_form = OrderForm(instance=order)

    if request.method == 'POST':
        o_form = OrderForm(request.POST)
        if o_form.is_valid():
            customer_get = o_form.cleaned_data['customer']
            product_get = o_form.cleaned_data['product']
            status_get = o_form.cleaned_data['status']
            order = Order.objects.filter(id=order_id)
            order.update(id=order_id, customer=customer_get, product=product_get, status=status_get)
            return redirect('orderSystem:homepage')

    context = {
        'o_form': o_form,
        'order': order
    }

    return render(request, 'orderSystem/updateoder.html', context)


@login_required()
def delete_order(request):
    # print(Order.objects.get(pk=order_id))
    context = {

    }
    return render(request, 'orderSystem/deleteorder.html', context)
