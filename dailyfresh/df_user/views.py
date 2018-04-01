#coding=utf-8
from django.http import JsonResponse,HttpResponseRedirect
from django.shortcuts import render,redirect
from models import *
from hashlib import sha1
from . import user_decorator
from df_goods.models import *
from df_cart.models import *

def register(request):
    return render(request,'df_user/register.html')

def register_handle(request):
    post=request.POST
    uname=post.get('user_name')
    upwd=post.get('pwd')
    upwd2=post.get('cpwd')
    uemail=post.get('email')
    #判断两次密码
    if upwd != upwd2:
        return redirect('/user/register/')
    #密码加密
    s1=sha1()
    s1.update(upwd)
    upwd3=s1.hexdigest()
    #创建对象
    user=UserInfo()
    user.uname=uname
    user.upwd=upwd3
    user.uemail=uemail
    user.save()

    return redirect('/user/login/')

def register_exist(request):
    uname=request.GET.get('uname')
    count=UserInfo.objects.filter(uname=uname).count()
    return JsonResponse({'count':count})

def login(request):
    uname=request.COOKIES.get('uname','')
    context={'title':'用户登录','error_name':0,'error_pwd':0,'uname':uname}
    return render(request,'df_user/login.html',context)

def login_handle(request):
    #接受请求信息
    post=request.POST
    uname=post.get('username')
    upwd=post.get('pwd')
    jizhu=post.get('jizhu',0)
    #根据用户查询对象
    users=UserInfo.objects.filter(uname=uname)
    print uname
    #判断：如果未查到，则用户名错误；如果查到，则判断密码是否正确，正确则转到用户中心
    if len(users)==1:
        s1=sha1()
        s1.update(upwd)
        if s1.hexdigest()==users[0].upwd:
            url=request.COOKIES.get('url','/')
            red=HttpResponseRedirect(url)
            #记住用户名
            if jizhu!=0:
                red.set_cookie('uname',uname)
            else:
                red.set_cookie('uanme','',max_age=-1)
            request.session['user_id']=users[0].id
            request.session['user_name']=uname
            request.session['count']=CartInfo.objects.filter(user_id=users[0].id).count()
            return red
        else:
            context={'title':'用户登录','error_name':0,'error_pwd':1,'uname':uname,'upwd':upwd}
            return render(request,'df_user/login.html',context)
    else:
        context={'title':'用户登录','error_name':1,'error_pwd':0,'uname':uname,'upwd':upwd}
        return render(request,'df_user/login.html',context)

@user_decorator.login
def info(request,*args,**kwargs):
    user_email=UserInfo.objects.get(id=request.session['user_id']).uemail
    user_phone = UserInfo.objects.get(id=request.session['user_id']).uphone
    user_address = UserInfo.objects.get(id=request.session['user_id']).uaddress

    goods_ids=request.COOKIES.get('goods_ids','')
    goods_ids1=goods_ids.split(',')
    goods_list=[]
    if len(goods_ids):
        for goods_id in goods_ids1:
            goods_list.append(GoodsInfo.objects.get(id=int(goods_id)))
    uid = request.session['user_id']
    count = CartInfo.objects.filter(user_id=uid).count()

    context={
        'title':'用户中心',
        'user_email':user_email,
        'user_name':request.session['user_name'],
        'user_phone':user_phone,
        'user_address':user_address,
        'page_name':1,
        'goods_list':goods_list,
        'count':count,
    }
    return render(request,'df_user/user_center_info.html',context)

@user_decorator.login
def order(request):
    context={
        'title':'用户中心',
        'page_name': 1}
    return render(request,'df_user/user_center_order.html',context)

@user_decorator.login
def site(request):
    user=UserInfo.objects.get(id=request.session['user_id'])
    if request.method=='POST':
        post=request.POST
        user.ureceiver=post.get('ureceiver')
        user.uaddress=post.get('uaddress')
        user.uyoubian=post.get('uyoubian')
        user.uphone=post.get('uphone')
        user.save()

    context={
        'title':'用户中心',
        'user':user,
        'page_name': 1,
    }
    return render(request,'df_user/user_center_site.html',context)

def logout(request):
    request.session.flush()
    return  redirect('/')
