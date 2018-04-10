#__autor__ = sunweiwei
#date = 2018/3/4
from django.contrib import admin
from mycrm.sites import site
from mycrm import models
from mycrm.admin_base import BaseKingAdmin

class CustomerAdmin(BaseKingAdmin):
    list_display = ['name','source','contact_type','contact','consultant','status','date']
    list_filter = ['source','consultant','status','date']
    search_fields = ['contact','consultant__name','contact_type','name']
    readonly_fields = ['contact','status']
    filter_horizontal =['consult_courses']
    actions = ['change_status']
    def change_status(self,request,querysets):
        print('kingadmin action',self,request,querysets)
        querysets.update(status=0)


class CustomerFollowUpAdmin(BaseKingAdmin):
    list_display = ['user','status','date']
    list_filter = ['user','status','date']
    search_fields = ['contact','status','date']



class CourseAdmin(BaseKingAdmin):
    list_display = ['name','price','outline']
    list_filter = ['name','price','outline']
    search_fields = ['name','price','outline']
class ClassListAdmin(BaseKingAdmin):
    list_display = ['start_date','graduate_date']
    list_filter = ['start_date','graduate_date']
    search_fields = ['start_date','graduate_date']

site.register(models.CustomerInfo,CustomerAdmin)
site.register(models.CustomerFollowUp,CustomerFollowUpAdmin)
site.register(models.Course,CourseAdmin)
site.register(models.ClassList,ClassListAdmin)
site.register(models.UserProfile)
site.register(models.ContractTemplate)
