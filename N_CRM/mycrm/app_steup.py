#__autor__ = sunweiwei
#date = 2018/3/4

from django.conf import settings


def get_app_name():
    kingadmin_list ={}
    app_name_list = settings.INSTALLED_APPS
    for app_name in app_name_list:
        try:
            _models = __import__("%s.crm_admin"%app_name)#crm_admin = 原来的kingadmin.py文件
            # print(_models.kingadmin)
        except ImportError:
            pass
        # kingadmin_list.append(_models)
        # print(kingadmin_list)

