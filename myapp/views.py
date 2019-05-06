from django.shortcuts import render,redirect
from django.http import  HttpRequest
from django.http import HttpResponse
from myapp import models
from myapp.forms import UserForm
from myapp.forms import RegisterForm
import hashlib
# Create your views here.
def hello(request):
    #return HttpResponse("Hello world ! ")
    context = {}
    context['hello']="Hello World!"
    return render(request,'hello.html',context)

def index(request):
    return render(request,"login/index.html")

def login(request):
    #检查登录会话，防止重复登录
    if request.session.get('is_login',None):
        return redirect('/index')

    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = models.User.objects.get(name=username)
                if user.password == hash_code(password):
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    return redirect("/index")
                    # return render(request, 'login/index.html', locals())
                else:
                    message = "密码有误！"
            except:
                message = '用户不存在! '
        return render(request,'login/login.html',locals())
    login_form = UserForm()
    return render(request, 'login/login.html', locals())
    # if request.method == "POST":
    #     username = request.POST.get('username',None)
    #     password = request.POST.get('password',None)
    #     message = "所有字段都必须填写！"
    #     if username and password:# 确保用户名和密码都不为空
    #         username = username.strip()
    #         try:
    #             user = models.User.objects.get(name=username)
    #             if user.password == password:
    #                 return redirect('/index/')
    #             else:
    #                 message = "用户名或密码有误!"
    #         except:
    #             message = "用户名不存在！"
    #     return render(request,'login/login.html',{"message":message})
    # return render(request,'login/login.html')

def register(request):
    if request.session.get('is_login', None):
        # 登录状态不允许注册。你可以修改这条原则！
        return redirect("/index")
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            phone = register_form.cleaned_data['phone']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']
            if password1 !=password2:
                message = "两次密码不一至"
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:
                    message = "用户名已存在,请重新选择用户名"
                    return render(request,'login/register.html',locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:  # 邮箱地址唯一
                    message = '该邮箱地址已被注册，请使用别的邮箱！'
                    return render(request, 'login/register.html', locals())
                same_phone_user = models.User.objects.filter(phone=phone)
                if same_phone_user:  # 邮箱地址唯一
                    message = '该邮手机号已被注册'
                    return render(request, 'login/register.html', locals())

                # 当一切都OK的情况下，创建新用户
                new_user = models.User.objects.create()
                new_user.name = username
                new_user.password = hash_code(password1)
                new_user.phone = phone
                new_user.email = email
                new_user.sex = sex
                new_user.save()
                return redirect('/login')  # 自动跳转到登录页面

    register_form = RegisterForm()
    return render(request,'login/register.html',locals())

def logout(request):
    if not request.session.get('is_login',None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/index")
    request.session.flush()
    # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect('/index')

def hash_code(s,salt='shencai123'):
    h = hashlib.sha3_256() # type: hashlib.sha256
    s += salt
    h.update(s.encode()) # update方法只接收bytes类型
    return h.hexdigest()