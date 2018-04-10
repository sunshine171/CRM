#__autor__ = sunweiwei
#date = 2018/3/5
from django.shortcuts import render

class BaseKingAdmin(object):
    def __init__(self):
        self.actions.extend(self.default_action)
    list_display = []
    filter_display = []
    search_fields =[]
    readonly_fields = []
    filter_horizontal = []
    default_action = ['delete_selected_objs']
    actions = ['delete']
    def delete_selected_objs(self,request,querysets):
        return render(request,'kd/table_obj_delete.html')