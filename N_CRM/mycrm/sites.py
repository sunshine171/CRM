#__autor__ = sunweiwei
#date = 2018/3/4

from mycrm.admin_base import BaseKingAdmin

class Adminsite(object):

    def __init__(self):
        self.enable_dict = {}

    def register(self,model_class,admin_class=None):#从register中取到数据库表和admin_class
        # print('.............',model_class,admin_class)
        app_name = model_class._meta.app_label  #_meta取到app的名字
        model_name = model_class._meta.model_name#取到对应的表名
        # admin_name = admin_class._meta.app_label
        if not admin_class:      #如果admin_class为空，执行默认的参数，有的换，执行填写的参数
            admin_class = BaseKingAdmin()
        else:
            admin_class = admin_class()

        admin_class.model = model_class#将model_class封装到admin_class中，后面用到
        # print("22222",admin_class.model)
        if app_name not in self.enable_dict:
            # {app_name:
            #   {  model_name :  admin_class }
            # } 格式
            self.enable_dict[app_name] = {}
        self.enable_dict[app_name][model_name] = admin_class

site = Adminsite()





