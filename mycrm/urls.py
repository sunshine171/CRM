
from django.urls import path,re_path
from mycrm import views
from django.conf.urls import url

urlpatterns = [
    path('',views.kingadmin,name='/mycrm/'),
    path('login/',views.k_login),#登陆
    path('logout/',views.k_logout,name='k_logout'),#登出
    path('app_index/',views.app_index,name='app_index'),#查看数据表名
    path('admin/',views.admin,name='/mycrm/admin/'),#管理员页面
    path('student/',views.student,name='/mycrm/student/'),#学生页面
    path('teacher/',views.teacher,name='/mycrm/teacher/'),#老师页面
    path('enrollment/',views.enrollment,name='/mycrm/enrollment/'),#报名页面
    # click销售页面进入db_table_name展示页面
    # path('db_table_name/', views.db_table_name, name='/mycrm/sale/'),
    path('db_table_name/', views.db_table_name, name='/mycrm/sale/'),
    # re_path('change/',views.foo,name='table_obj_change'),


    url(r'^enrollment/(\d+)/$', views.enrollment_info, name='enrollment_info'),
    url(r'^enrollment/(\d+)/fileup/$', views.enrollment_fileupload, name='enrollment_fileupload'),#报名文件上传

    url(r'^enrollment/(\d+)/enrollment_contract/$', views.enrollment_contract, name='enrollment_contract'),#报名审核

    url(r'^(\w+)/(\w+)/(\d+)/change/$',views.table_obj_change,name='table_obj_change'),#修改数据页面
    url(r'^(\w+)/(\w+)/$', views.table_obj_list, name='table_obj_list'),#查看每条数据页面
    url(r'^(\w+)/(\w+)/add/$', views.table_obj_add, name='table_obj_add'),#增加数据
    url(r'^(\w+)/(\w+)/(\d+)/delete/$', views.table_obj_delete, name='table_obj_delete'),#删除数据




]