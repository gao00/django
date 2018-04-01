#coding=utf-8
from django.shortcuts import render, redirect
from df_user.models import *
from .models import *
from django.http import JsonResponse
from df_user.user_decorator import login

@login
def cart(request):
    uid=request.session['user_id']
    carts=CartInfo.objects.filter(user_id=uid)

    context={
        'title':'购物车',
        'page_name':1,
        'carts':carts,
    }
    return render(request,'df_cart/cart.html',context)

@login
def add_cart(request,gid,num):
    uid=int(request.session['user_id'])
    gid=int(gid)
    num=int(num)
    carts=CartInfo.objects.filter(user_id=uid,goods_id=gid)
    if len(carts)>=1:
        cart=carts[0]
        cart.count=cart.count+num
    else:
        cart=CartInfo()
        cart.user_id=uid
        cart.goods_id=gid
        cart.count=num
    cart.save()
    count_s=CartInfo.objects.filter(user_id=uid).count()
    request.session['count']=count_s
    if request.is_ajax():
        # count=CartInfo.objects.filter(user_id=request.session['user_id']).count()

        print '*' * 10
        print 'ajax'
        # --------------未使用
        return JsonResponse({'count': count_s})
    else:
        return redirect('/cart/')

@login
def edit(request,cart_id,count):
    try:
        cart=CartInfo.objects.get(pk=int(cart_id))
        count1=cart.count=int(count)
        cart.save()
        data={'ok':0}
    except Exception as e:
        data={'ok':count1}
    return  JsonResponse(data)

@login
def delete(requet,cart_id):
    try:
        cart=CartInfo.objects.get(pk=int(cart_id))
        cart.delete()
        data = {'ok': 1}
    except Exception as e:
        data={'ok':0}
    return JsonResponse(data)



