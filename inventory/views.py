# -*- coding:utf-8 -*-
from django.shortcuts import render, redirect, HttpResponse
from django.http import HttpResponse
from rest_framework.views import APIView
from .models import Inventory,InventoryRecord
from merchandises.models import Merchandise
from .serializers import AddRecordSerializers
from rest_framework.response import Response
from rest_framework import status
from functools import wraps
from django.contrib import auth
from django import forms    #导入表单
from django.contrib.auth.models import User   #导入django自带的user表
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


# Create your views here.


class UserForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=100)
    password = forms.CharField(label='密_码', widget=forms.PasswordInput())



@login_required
def add_inventory(request):
    return render(request, 'add.html')

@csrf_exempt
def regist(request):
    if request.method == 'POST':
        uf = UserForm(request.POST)  # 包含用户名和密码
        if uf.is_valid():
            username = uf.cleaned_data['username']  # cleaned_data类型是字典，里面是提交成功后的信息
            password = uf.cleaned_data['password']
            try:
                registAdd = User.objects.create_user(username=username, password=password)
                return render(request, 'result.html', {'registAdd': registAdd})
            except:
                return render(request, 'result.html', {'registAdd': '', 'username': username})

    else:
        # 如果不是post提交数据，就不传参数创建对象，并将对象返回给前台，直接生成input标签，内容为空
        uf = UserForm()
    # return render_to_response('regist.html',{'uf':uf},context_instance = RequestContext(request))
    return render(request, 'register.html', {'uf': uf})


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        re = auth.authenticate(username=username,password=password)  #用户认证
        if re is not None:  #如果数据库里有记录（即与数据库里的数据相匹配或者对应或者符合）
            auth.login(request,re)   #登陆成功
            return redirect('/inventory/add/')    #跳转--redirect指从一个旧的url转到一个新的url
        else:  #数据库里不存在与之对应的数据
            return render(request, 'login.html', {'login_error':'用户名或密码错误'})  #注册失败
    return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return render(request, 'login.html')


class SubmitView(APIView):
    def post(self,request):
        merchandise = Merchandise.objects.get(barcode=request.data['barcode'])
        try:
            inventory = Inventory.objects.get(merchandiseID=merchandise.code)
        except:
            inventory = Inventory(merchandiseID=merchandise, stock=0, stockWithTag=0)
        inventory.stock += int(request.data['quantity'])
        inventory.save()
        inventory_record_data = {
            'merchandiseID': merchandise.code,
            'instockPrice': float(request.data['instockPrice']),
            'retailPrice': float(request.data['retailPrice']),
            'productionDate': request.data['productionDate'],
            'expiryDate': request.data['expiryDate'],
            'quantity': int(request.data['quantity']),
            'supplier': request.data['supplier'],
        }
        serializer = AddRecordSerializers(data=inventory_record_data)

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
