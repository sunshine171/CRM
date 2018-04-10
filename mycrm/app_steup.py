from django.conf import settings


def get_app_name():
    kingadmin_list ={}
    app_name_list = settings.INSTALLED_APPS
    for app_name in app_name_list:
        try:
            _models = __import__("%s.crm_admin"%app_name)#crm_admin = 原来的kingadmin.py文件
        except ImportError:
            pass

