from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
import json
from django.shortcuts import render, redirect,HttpResponse
from mycrm import handle_forms
import os,sys
from django.utils.timezone import datetime #取时区的时间，。然没弄出来，
from django import conf
from mycrm import app_steup
from mycrm.sites import site
from django.db.utils import IntegrityError

from django.views.decorators.csrf import csrf_exempt

from mycrm import models
from mycrm import form
from mycrm import permissions


app_steup.get_app_name()
# print(site)



@login_required    #检验未登录，跳转到登陆界面
def kingadmin(request):
    # kingadmin首页展示
    return render(request, 'kd/index.html')

def k_login(request):
    """登陆操作，登陆成功右上角显示用户名"""
    message = ''
    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username = username,password=password)    #验证用户名和密码
        if user:
            login(request,user)
            return redirect(request.GET.get('next', '/mycrm/'))
            #‘next’记录目标url，默认首页
        else:
            message = 'check out your username or password'#登陆页面打印错误信息
    return render(request,'kd/login.html',{'message':message})#get请求，返回登陆页面

def k_logout(request):
    """登出操作"""
    logout(request)
    return redirect('/mycrm/')#跳转到首页


@login_required
def app_index(request):
    return render(request,'kd/index.html',{'site':site})


@permissions.check_permission
@login_required
def table_obj_list(request,app_name,model_name):
    search_value = ''
    urls_name = [app_name,model_name]
    # """获取相应models中的数据返回给前端"""
    # print('ok',site.enable_dict[model_class][admin_class])
    admin_class = site.enable_dict[app_name][model_name]

    # print('333333',admin_class.model)
    if request.method == 'POST':
        print(request.POST)
        selected_action = request.POST.get('action')
        # selected_ids= json.loads(request.POST.get('selected_ids'))
        # print('sssssssss',selected_ids)
        # selected_objs = admin_class.model.objects.filter(id__in=selected_ids)
        # admin_action_func = getattr(admin_class,selected_action)
        # admin_action_func(request,selected_objs)

    querysets = admin_class.model.objects.all()#获取当前表中的所有数据
    querysets,filter_conditions = get_filter_result(request,querysets)#过滤之后的数据，
    admin_class.filter_conditions = filter_conditions#将url中取到的‘筛选的键值对’封装到对象中

    querysets,current_order_field = get_orderby_result(request,querysets,admin_class)
    #排序之后的数据

    querysets= get_search_result(request,querysets,admin_class)#搜索之后的数据
    admin_class.order_conditions = current_order_field#将？？封装到对象中
    admin_class.search_key = request.GET.get('_search','')#get请求时，取到url中的_search后的值

    # o = 1111111
    # for i in querysets:
    #     o+=11111111
    #     print('00000000000000'+str(o),type(i),i)
    # print(type(querysets))
    # return render(request,'kd/table_obj_list.html',{'querysets':querysets})
    querysets = paging(request,querysets)#分页后的数据
    all_filter,all_order = all_add(request,admin_class)


    return render(request,'kd/table_show.html',{'admin_class':admin_class,
                                                    'querysets':querysets,
                                                    'current_order_field':current_order_field,
                                                    'all_filter':all_filter,
                                                    'all_order':all_order,
                                                    'urls_name':urls_name})


@login_required
def get_search_result(request,querysets,admin_class):
    search_value = request.GET.get('_search')
    if search_value:
        con = Q()
        con.connector = 'OR'
        # print("22222222",search_value)
        for search_field in admin_class.search_fields:
            # print('33333333', search_field)
            con.children.append(('%s__contains'%search_field,search_value))
        return querysets.filter(con)
    return querysets


@login_required
def get_filter_result(request,querysets):
    filter_conditions = {}
    for key,val in request.GET.items():
        if key in ('_page','_o','_search','csrfmiddlewaretoken'):
            continue
        if val:
            filter_conditions[key] = val
    return querysets.filter(**filter_conditions),filter_conditions

@login_required
def paging(request,querysets):
    #分页
    p = Paginator(querysets,3)#实例化分页，每五个数据为一页

    page = request.GET.get('_page')#从url中获取分页的值  _page = 等号后面的值
    querysets = p.get_page(page)  #获取
    return querysets


@login_required
def get_orderby_result(request,querysets,admin_class):
    fields_index = request.GET.get('_o')
    current_order_field = {}#获取到排序的url上的信息，分页和过滤都可以实现着个功能，而且挺好用，以后只要动态获取url上的信息时，就可以这样提取，urls.py上的信息用可以用正则匹配事的分组进行获取，
    if fields_index:
        # print('00000000000000000000',admin_class.list_filter)
        fields_name = admin_class.list_display[abs(int(fields_index))]
        current_order_field[fields_name] = fields_index#{fields_names（根据url值取得display的值）:url中获取的值}
        if fields_index.startswith('-'):#后端获取到为负号的数值，就进行反向排序，利用querysets.order_by(field_name)
            fields_name = '-'+fields_name
        return querysets.order_by(fields_name),current_order_field
    else:
        return querysets,current_order_field


@login_required
def all_add(request,admin_class):
    '''这个函数实现了将过滤的  &%s=%s  和 排序的 &_o=%s  给添加到分页上，和过滤排序互相添加'''
    all_add_urls_filter = ''
    all_add_urls_order = ''
    if admin_class.filter_conditions:
        for filter_key,filter_value in admin_class.filter_conditions.items():
        # filter_key = list(admin_class.filter_conditions.keys())[0]
        # filter_value = list(admin_class.filter_conditions.values())[0]
            filter_str = '&%s=%s'%(filter_key,filter_value)
            all_add_urls_filter += filter_str
    else:
        filter_str = ''
        all_add_urls_filter += filter_str#过滤


    if admin_class.order_conditions:
        for order_name,order_digiter in admin_class.order_conditions.items():
            # order_name = list(admin_class.order_conditions.keys())[0]
            # order_digiter = list(admin_class.order_conditions.values())[0]
            order_str = '&_o=%s'%(order_digiter,)
            all_add_urls_order += order_str
    else:
        order_str = ''
        all_add_urls_order += order_str#排序
    # print('all_add_urls_filter',all_add_urls_filter)
    return all_add_urls_filter,all_add_urls_order

@permissions.check_permission
@login_required
def table_obj_change(request,app_name,model_name,obj_id):

    # from kingadmin import handle_forms
    # forms_obj = handle_forms.creat_dynamic_modelform(admin_class)

    admin_class = site.enable_dict[app_name][model_name]
    model_form = handle_forms.creat_dynamic_modelform(admin_class)

    obj = admin_class.model.objects.get(id=obj_id)#获取到当前进入的一条数据行对象
    if request.method == 'GET':
        form_obj = model_form(instance=obj)
    elif request.method == 'POST':
        form_obj = model_form(instance=obj,data=request.POST)

        if form_obj.is_valid():
            form_obj.save()
            return redirect('/mycrm/%s/%s'%(app_name,model_name))

    return render(request,'kd/table_u.html',locals())

@permissions.check_permission
@login_required
def table_obj_add(request,app_name,model_name):
    admin_class = site.enable_dict[app_name][model_name]
    model_form = handle_forms.creat_dynamic_modelform(admin_class,form_add=True)
    if request.method == 'GET':
        form_obj = model_form()

    if request.method == 'POST':
        form_obj = model_form(data=request.POST)
        if form_obj.is_valid():
            form_obj.save()
            return redirect('/mycrm/%s/%s' % (app_name, model_name))
    # print('777777777777777777777')
    return render(request,'kd/table_c.html',locals())

@permissions.check_permission
@login_required
def table_obj_delete(request,app_name,model_name,obj_id):
    admin_class = site.enable_dict[app_name][model_name]
    obj = admin_class.model.objects.get(id=obj_id)
    print('okokokkkkkk',obj)
    if request.method == 'POST':
        obj.delete()
        # print('88888888888888888888')
        return redirect('/kingadmin/%s/%s/'%(app_name,model_name))
    return render(request,'kd/table_d.html',locals())

@permissions.check_permission
@login_required
def admin(request):
    return HttpResponse('admin')


@login_required
def student(request):
    return HttpResponse('student')

@login_required
def teacher(request):
    return HttpResponse('teacher')


@login_required
def dashboard(request,):

    return render(request,'kd/table_show.html')

# @permissions.check_permission
@login_required
def db_table_name(request):
    print(site.enable_dict)
    return render(request,'kd/db_table_name.html',{'site':site})


@login_required
def enrollment(request):
    customers = models.CustomerInfo.objects.all()
    grades = models.ClassList.objects.all()

    if request.method =='POST':
        # print('8888888')#至此翻车了，select 是下拉框，name，option是下拉框中的内容，是value，例如：
        #<select name='sun'>   <option value='111'>  后端得到  {'sun':111}
        customer_id =request.POST.get('customer_id')
        class_grade_id =request.POST.get('grade_id')
        try:
            # print('2222222')
            enrollment_obj = models.StudentEnrollment.objects.create(
                customer_id = customer_id,
                class_grade_id = class_grade_id,
                consultant_id = request.user.userprofile.id
            )
        except IntegrityError as e:
            enrollment_obj = models.StudentEnrollment.objects.get(customer_id=customer_id,class_grade_id=class_grade_id)

            if enrollment_obj.contract_agreed:
                print('999999',customer_id,class_grade_id)
                return redirect("/mycrm/enrollment/%s/enrollment_contract/"%enrollment_obj.id)


        urls = 'http://localhost:8000/mycrm/enrollment/%s'%enrollment_obj.id

    return render(request,'kd/enrollment.html',locals())


@login_required
def enrollment_info(request,enrollment_id):
    enrollment_obj = models.StudentEnrollment.objects.get(id=enrollment_id)
    if request.method == 'POST':
        # print('666666666',request.POST)
        customer_form = form.CustomerInfoForm(instance=enrollment_obj.customer,data=request.POST)
        if customer_form.is_valid():
            # print('llllllllll')
            customer_form.save()
            enrollment_obj.contract_agreed = True
            #enrollment_obj.contract_approved_date = datetime.now()#应该取到该地区的时区时间
            enrollment_obj.save()
            return HttpResponse('<h1>您已经成功报名！，请等待审核</h1>')
    else:
        customer_form = form.CustomerInfoForm(instance=enrollment_obj.customer)
    """列出已上传文件"""
    upload_files = []
    enrollment_fileupload_dir = os.path.join(conf.settings.CRM_FILE_UPLOAD_DIR,enrollment_id)
    if os.path.isdir(enrollment_fileupload_dir):
        upload_files = os.listdir(enrollment_fileupload_dir)#这里os.listdir得到的值就是一个列表，
                                                # 别王列表里添加了，那样会生成一个列表套列表
    # print(upload_files)
    return render(request,'kd/customer_form.html',locals())


@login_required
@csrf_exempt
def enrollment_fileupload(request,enrollment_id):
    enrollment_updata_dir = os.path.join(conf.settings.CRM_FILE_UPLOAD_DIR,enrollment_id)
    if not os.path.isdir(enrollment_updata_dir):
        # print('qqqqqqqqqqqqq')
        os.mkdir(enrollment_updata_dir)
    else:
        if len(os.listdir(enrollment_updata_dir)) < 2:
            files_obj = request.FILES.get('file')
            # print(files_obj,'pppppppppppp')
            with open(os.path.join(enrollment_updata_dir,files_obj.name),'wb') as f:
                # print('oooooooo')
                for chunks in files_obj.chunks():
                    f.write(chunks)
                f.close()
        else:
            return HttpResponse(json.dumps({"status":False,"err_msg":"max upload limit is 2"}))

    # """
    #     1.在POST提交之后form表单数据验证并且保存
    #     2.将上传上来的图片进行写入文件，
    #         按照一个客户一个目录写入，文件名可以用在StudentEnrollment表创建的学生id
    #     3.feils写入时，按照路径的方式来写入
    # """

    # print('lllllllllll')
    # return render(request,'kd/customer_form.html',locals())
    return HttpResponse(json.dumps({"status":True,}))


@login_required
def enrollment_contract(request,enrollment_id):
    """报名后，销售审核页面"""
    enrollment_obj = models.StudentEnrollment.objects.get(id=enrollment_id)
    print('.......',enrollment_obj)
    if request.method =='POST':
        enrollment_form = form.StudentEnrollmentForm(instance=enrollment_obj,data=request.POST)
        if enrollment_form.is_valid():
            enrollment_form.save()
            stu_obj =  models.Student.objects.get_or_create(customer=enrollment_obj.customer)[0]
            stu_obj.class_grade.add(enrollment_obj.class_grade_id)
            stu_obj.save()
            enrollment_obj.customer.status = True
            print('pppppppppp')
            enrollment_obj.customer.save()
            return redirect('/mycrm/')
    else:
        customer_form = form.CustomerInfoForm(instance=enrollment_obj.customer)
        enrollment_form = form.StudentEnrollmentForm(instance=enrollment_obj)
    return render(request,'kd/enrollment_contract_form.html',locals())