from django.forms import ModelForm
from django import forms


def creat_dynamic_modelform(admin_class,form_add=False):
    #动态实现form表单，用于多个增删查改的页面
    """form_add=False:默认为修改True为添加"""
    class Meta:
        model = admin_class.model
        fields = "__all__"
        if not form_add: #修改
            exclude = admin_class.readonly_fields
            admin_class.form_add = False
        else: #添加
            admin_class.form_add = True

    def __new__(cls,*args,**kwargs):
        for field_name in cls.base_fields:
            field_obj = cls.base_fields[field_name]
            field_obj.widget.attrs.update({'class':'form-control'})


        return ModelForm.__new__(cls)

    dynamic_form = type('DynamicModelForm',(ModelForm,),{'Meta':Meta,'__new__':__new__})
    return dynamic_form

