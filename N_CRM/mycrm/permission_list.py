#__autor__ = sunweiwei
#date = 2018/4/10



perm_dic = {

    # 'mycrm_table_index': ['table_indemycrm_table_addx', 'GET', [], {'source':'qq'}, ],  # 可以查看CRM APP里所有数据库表
    'mycrm_table_list': ['table_obj_list', 'GET', [], {}],  # 查看具体数据展示,，包括排序，搜索，过滤
    # 'mycrm_table_list_post': ['table_obj_list', 'POST', [], {}],  # 查看具体数据展示
    'mycrm_table_change_view': ['table_obj_change', 'GET', [], {}],  # 查看具体数据的修改页面
    'mycrm_table_change': ['table_obj_change', 'POST', [], {}],  # 查看具体数据的修改页面，并进行修改
    'mycrm_table_add': ['table_obj_add', 'POST', [], {}],  # 查看增加页面，并增加数据
    'mycrm_table_add_view': ['table_obj_add', 'GET', [], {}],  # 查看增加页面
    'mycrm_table_list_db': ['/mycrm/sale/', 'GET', [], {}],  # 可以查看表数据
    'mycrm_table_delete_view': ['table_obj_delete', 'GET', [], {}],  # 查看具体删除数据展示
    'mycrm_table_delete': ['table_obj_delete', 'POST', [], {}],  # 查看具体删除数据展示，并删除

    }
