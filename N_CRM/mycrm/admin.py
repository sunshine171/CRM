from django.contrib import admin
from mycrm import models



from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from mycrm.models import UserProfile


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = UserProfile
        fields = ('email', 'name')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])#把明文密码改成密文
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = UserProfile
        fields = ('email', 'password', 'name', 'is_active', 'is_superuser')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserProfileAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'name', 'is_superuser')
    list_filter = ('is_superuser',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name',)}),
        ('Permissions', {'fields': ('is_active','is_staff','is_superuser','role','user_permissions','groups')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('role','user_permissions','groups')

# Now register the new UserAdmin...
admin.site.register(UserProfile, UserProfileAdmin)
# # ... and, since we're not using Django's built-in permissions,
# # unregister the Group model from admin.
admin.site.unregister(Group)



# Register your models here.
class CustomerInfoAdmin(admin.ModelAdmin):
    list_display = ['name','source','contact_type','contact','consultant','status','date']
    list_filter = ['source','consultant','status','date']
    search_fields = ['contact','consultant__name','contact_type','name']
    readonly_fields = ['status','contact']
    filter_horizontal = ['consult_courses']
    actions =['change_status']
    def change_status(self,*args,**kwargs):
        print('change_status',self,*args,**kwargs)
    #分页
    # list_per_page = 2
# admin.site.register(models.UserProfile,UserProfileAdmin)#也可以用，把models去掉
admin.site.register(models.Student)
admin.site.register(models.Branch)
admin.site.register(models.ClassList)
admin.site.register(models.Course)
admin.site.register(models.CourseRecord)
admin.site.register(models.CustomerFollowUp)
admin.site.register(models.StudyRecord)
admin.site.register(models.CustomerInfo)
admin.site.register(models.Role)
admin.site.register(models.Menus)
admin.site.register(models.StudentEnrollment)
admin.site.register(models.ContractTemplate)





# class CustomerAdmin(admin.ModelAdmin):
#     list_display = ['name', 'source', 'contact_type', 'contact', 'consultant', 'consult_content', 'status', 'date']
#     list_filter = ['source', 'consultant', 'status', 'date']
#     search_filed = ['contact', 'consultant__name']
#     # 这个consultant是外键，搜索其字段需要双下划线'__name'；
#
#
# # 注册
# admin.site.register(models.CustomerInfo, CustomerAdmin)
