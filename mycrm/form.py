from django.forms import ModelForm,forms
from mycrm import models


class StudentEnrollmentForm(ModelForm):

    class Meta:
        model = models.StudentEnrollment
        fields = "__all__"
        readonly_fields = ['contract_agreed']


    def __new__(cls, *args, **kwargs):
        #重写new方法，给页面添加属性
            for field_name in cls.base_fields:
                field_obj = cls.base_fields[field_name]
                field_obj.widget.attrs.update({'class': 'form-control'})
                if field_name in cls.Meta.readonly_fields:
                    field_obj.widget.attrs.update({'disabled': 'true'})#添加disable属性

            return ModelForm.__new__(cls)
    def clean(self):
        print("cleaned_daat:",self.cleaned_data)
        if self.errors:
            raise forms.ValidationError(("Please fix errors before re-submit."))
        if self.instance.id is not None:
            for field in self.Meta.readonly_fields:
                old_field_val=getattr(self.instance,field)#数据库里的数据
                form_val = self.cleaned_data.get(field)
                print("filed differ compare:",old_field_val,form_val)
                if old_field_val != form_val:
                    self.add_error(field,"Readonly Field: field sheould be '{value}',not '{new_value}'".\
                                   format(**{'value':old_field_val,'new_value':form_val}))


class CustomerInfoForm(ModelForm):
    class Meta:
        model = models.CustomerInfo
        fields = "__all__"

        exclude = ['consult_content','status','consult_courses']
        readonly_fields = ['contact_type','contact','consultant','referral_from','source']


    def __new__(cls, *args, **kwargs):
            for field_name in cls.base_fields:
                # print('77777777777', cls.base_fields)
                field_obj = cls.base_fields[field_name]
                # print('66666', field_name)
                field_obj.widget.attrs.update({'class': 'form-control'})
                if field_name in cls.Meta.readonly_fields:
                    field_obj.widget.attrs.update({'disabled': 'true'})

            return ModelForm.__new__(cls)
    def clean(self):
        print("cleaned_daat:",self.cleaned_data)
        if self.errors:
            raise forms.ValidationError(("Please fix errors before re-submit."))
        if self.instance.id is not None:
            for field in self.Meta.readonly_fields:
                old_field_val=getattr(self.instance,field)#数据库里的数据
                form_val = self.cleaned_data.get(field)
                print("filed differ compare:",old_field_val,form_val)
                if old_field_val != form_val:
                    self.add_error(field,"Readonly Field: field sheould be '{value}',not '{new_value}'".\
                                   format(**{'value':old_field_val,'new_value':form_val}))