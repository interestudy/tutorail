from django.forms import ModelForm, Form
from django import forms

from .models import Customer, Order

#create your code here


class RegisterForm(Form):
    username = forms.CharField(
        label= '用户名',
        max_length= 128,
        widget= forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'username'
        })
    )

    password1 = forms.CharField(
        label= '密码',
        max_length= 30,
        widget= forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'password'
        })
    )

    password2 = forms.CharField(
        label= '确认密码',
        max_length= 30,
        widget= forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'password'
        })
    )

    email = forms.EmailField(
        label= '邮箱',
        widget= forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'email address'
        })
    )

    phone = forms.CharField(
        label= '手机',
        max_length= 128,
        widget= forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'tel'
        })
    )


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['time_created']
        labels = {
            'name': '名字',
            'phone': '电话',
            'email': '邮箱'
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入名字'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入电话'
            }),
            'email': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入邮箱'
            })
        }


class OrderForm(ModelForm):
    class Meta():
        model = Order
        fields = '__all__'
        exclude = ['time_created']
        labels = {
            'customer': '顾客',
            'product': '商品',
            'status': '订单状态'
        }
        widgets = {
            'customer': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': '请输入顾客'
            }),
            'product': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': '请输入商品'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': '请输入订单状态'
            })
        }