from geetest import GeetestLib
from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.contrib import auth
from app01 import models, forms

pc_geetest_id = "b46d1900d0a894591916ea94ea91bd2c"
pc_geetest_key = "36fc3fe98530eea08dfc6ce76e3d24c4"


# Create your views here.
def chess(request):
    if not request.user.is_authenticated():
        return redirect('/login')
    return render(request, "index.html")


from django.db.models import F


def victory(request):
    if request.method == "POST":
        # print(request.path)
        depth = request.POST.get("depth")
        print(depth)
        user = request.user
        if int(depth) == 2:
            models.UserInfo.objects.filter(username=user).update(victory=F("victory") + 1, total=F("total") + 1,
                                                                 score=F("score") + 10)
        elif int(depth) == 3:
            models.UserInfo.objects.filter(username=user).update(victory=F("victory") + 1, total=F("total") + 1,
                                                                 score=F("score") + 20)
        else:
            models.UserInfo.objects.filter(username=user).update(victory=F("victory") + 1, total=F("total") + 1,
                                                                 score=F("score") + 30)
        return HttpResponse('OK')


def defeat(request):
    if request.method == "POST":
        # print(request.POST)
        depth = request.POST.get("depth")
        print(depth)
        user = request.user
        models.UserInfo.objects.filter(username=user).update(defeat=F("defeat") + 1)
        models.UserInfo.objects.filter(username=user).update(total=F("total") + 1)
        return HttpResponse('OK')


def rank(request):
    rank = models.UserInfo.objects.all().order_by('-score')
    a = []
    b = 0
    for i in rank:
        if b < 3:
            b = b + 1
            a.append(i)
    return render(request, 'rank.html', locals())


def personinfo(request, username):
    user = models.UserInfo.objects.filter(username=username).first()
    return render(request, 'personinfo.html', locals())


def login(request):
    if request.method == "POST":
        ret = {'status': 0, 'msg': ''}
        username = request.POST.get('username')
        password = request.POST.get('password')
        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        challenge = request.POST.get(gt.FN_CHALLENGE, '')
        validate = request.POST.get(gt.FN_VALIDATE, '')
        seccode = request.POST.get(gt.FN_SECCODE, '')
        status = request.session[gt.GT_STATUS_SESSION_KEY]
        user_id = request.session["user_id"]
        if status:
            result = gt.success_validate(challenge, validate, seccode, user_id)
        else:
            result = gt.failback_validate(challenge, validate, seccode)
        if result:
            # 验证码正确
            user = auth.authenticate(username=username, password=password)
            if user:
                # 用户名密码正确
                # 给用户做登录
                auth.login(request, user)
                ret["msg"] = '/chess/'
            else:
                ret['status'] = 1
                ret['msg'] = '用户名或验证码错误'
        else:
            ret['status'] = 1
            ret['msg'] = '验证码错误'
        return JsonResponse(ret)
    return render(request, 'login2.html')


def get_geetest(request):
    user_id = 'test'
    gt = GeetestLib(pc_geetest_id, pc_geetest_key)
    status = gt.pre_process(user_id)
    request.session[gt.GT_STATUS_SESSION_KEY] = status
    request.session["user_id"] = user_id
    response_str = gt.get_response_str()
    return HttpResponse(response_str)


def logout(request):
    auth.logout(request)
    return redirect("/chess/")


def check_username_exist(request):
    ret = {"status": 0, "msg": ""}
    username = request.GET.get("username")
    is_exist = models.UserInfo.objects.filter(username=username)
    if is_exist:
        # 存在
        ret['status'] = 1
        ret['msg'] = '用户名已被注册'
    return JsonResponse(ret)


def register(request):
    if request.method == "POST":
        ret = {"status": 0, "msg": ""}  # 设置状态信息
        form_obj = forms.RegForm(request.POST)
        if form_obj.is_valid():

            form_obj.cleaned_data.pop("re_password")  # 重复密码去掉
            avatar_img = request.FILES.get("avatar")
            models.UserInfo.objects.create_user(**form_obj.cleaned_data, avatar=avatar_img)
            ret["msg"] = "/chess/"
            return JsonResponse(ret)
        else:
            ret["status"] = 1
            ret["msg"] = form_obj.errors
            return JsonResponse(ret)
    form_obj = forms.RegForm()
    return render(request, 'register.html', {'form_obj': form_obj})
