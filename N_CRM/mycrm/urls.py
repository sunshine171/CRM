
from django.urls import path,re_path
from mycrm import views
from django.conf.urls import url

urlpatterns = [
    path('',views.kingadmin,name='/mycrm/'),
    path('login/',views.k_login),
    path('logout/',views.k_logout,name='k_logout'),
    path('app_index/',views.app_index,name='app_index'),#查看数据表名
    path('admin/',views.admin,name='/mycrm/admin/'),
    path('student/',views.student,name='/mycrm/student/'),
    path('teacher/',views.teacher,name='/mycrm/teacher/'),
    path('enrollment/',views.enrollment,name='/mycrm/enrollment/'),
    # click销售页面进入db_table_name展示页面
    # path('db_table_name/', views.db_table_name, name='/mycrm/sale/'),
    path('db_table_name/', views.db_table_name, name='/mycrm/sale/'),
    # re_path('change/',views.foo,name='table_obj_change'),


    url(r'^enrollment/(\d+)/$', views.enrollment_info, name='enrollment_info'),#这个原先放在delete下面执行的时候保错，错误在views.py中的admin_class那行代码，但是挪到现在的位置就不报错了，不清楚原因
    url(r'^enrollment/(\d+)/fileup/$', views.enrollment_fileupload, name='enrollment_fileupload'),

    url(r'^enrollment/(\d+)/enrollment_contract/$', views.enrollment_contract, name='enrollment_contract'),

    url(r'^(\w+)/(\w+)/(\d+)/change/$',views.table_obj_change,name='table_obj_change'),#修改数据页面
    url(r'^(\w+)/(\w+)/$', views.table_obj_list, name='table_obj_list'),#查看每条数据页面
    url(r'^(\w+)/(\w+)/add/$', views.table_obj_add, name='table_obj_add'),#增加数据
    url(r'^(\w+)/(\w+)/(\d+)/delete/$', views.table_obj_delete, name='table_obj_delete'),#删除数据




]