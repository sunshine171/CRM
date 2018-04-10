from django.template import Library
from django.utils.safestring import mark_safe
from datetime import datetime,timedelta


register = Library()

@register.simple_tag
def build_table_row(obj,admin_class):
    ele = ''
    if admin_class.list_display:
        for index,column_name in enumerate(admin_class.list_display):
            # print(index)
            column_obj = admin_class.model._meta.get_field(column_name)#当前整张表对象通过get_field(列名）获取字段对象
            # print('77777777777777777777',column_obj)
            if column_obj.choices:
                column_data = getattr(obj,'get_%s_display'%column_name)()
                # print('788888888888888888',obj)
            else:
                column_data = getattr(obj,column_name)
                # print("9999999999999",column_data)
            td_ele = '<td>%s</td>' % column_data
            if index == 0:
                td_ele = '<td><a href="%s/change">%s</a></td>'%(obj.id,column_data)#href 中的%s  是为取出的数据对象的id

            # td_ele = '%s'%column_data

            ele += td_ele
    else:
        td_ele = '<td><a href="%s/change">%s</a></td>' % (obj.id, obj)
        ele += td_ele
    return mark_safe(ele)


@register.simple_tag
def build_filter_ele(filter_column,admin_class):
    coulmn_obj = admin_class.model._meta.get_field(filter_column)
    try:
        filter_ele = '<select name="%s" class="form-control">' % filter_column#创建select标签 name = filtre_columu
        for choice in coulmn_obj.get_choices():#遍历choice字段对象
            selected = ''
            if filter_column in admin_class.filter_conditions:#判断filter存在与conditions中
                if str(choice[0]) == admin_class.filter_conditions.get(filter_column):#choice = url中的数字相等时
                    selected = "selected"#就是选中状态
            option = "<option value='%s' %s>%s</option>" % (choice[0], selected, choice[1])
            filter_ele += option
    except AttributeError as e:#遇到时间类型的数据报错时，except：
        filter_ele = '''<select name='%s__gte' class="form-control">''' % filter_column
        if coulmn_obj.get_internal_type() in ['DateTimeField','DateField']:#get_internal_type()应该时固定用法
            time_obj = datetime.now()#datetime.now()取到当前时间
            time_list = [
                ['',"------"],
                [time_obj - timedelta(weeks=1),'七天内'],#option一周内数据
                [time_obj.replace(month=1),'一月内'],#一月内数据
                [time_obj - timedelta(days=90),'三月内'],#三个月内数据
                [time_obj.replace(year=1),'YearToDay(YTD)'],#replace和timedelta区别？
                ['','ALL']
            ]
            for i in time_list:
                selected = ''
                time_to_str = '' if not i[0] else "%s-%s-%s"%(i[0].year,i[0].month,i[0].day)#三元运算
                if "%s__gte"%filter_column in admin_class.filter_conditions:
                    if time_to_str == admin_class.filter_conditions.get("%s__gte"%filter_column):#时间str__gte 取到？
                        selected = 'selected'
                option = "<option value='%s' %s>%s</option>" % (time_to_str,selected,i[1])
                filter_ele += option
    filter_ele += '</select>'
    return mark_safe(filter_ele)


@register.simple_tag
def build_model_name(admin_class):#生成大写的表名
    model_names = admin_class.model._meta.model_name
    ele = "<td>%s</td>"%model_names.upper()
    return mark_safe(ele)


@register.simple_tag
def build_paging(querysets,all_filter,all_order):
    ele = """ 
        <nav aria-label="Page navigation">
        <ul class="pagination">
            
        """
    for i in querysets.paginator.page_range:#querysets.paginator.page_range获取当前的page_range,就是页数范围
        if abs(querysets.number - i) < 2:#queryset.number为当前页数，要求显示当前页和前后两页，共三页内容，
            active = ''
            if querysets.number == i:#判断是否为当前页，true时，添加属性‘actie'
                active = 'active'
            td_ele = """<li class="%s"><a href="?_page=%s%s%s">%s</a></li>"""%(active,i,all_filter,all_order,i)#a标签href会在url后添加_page = num
            ele += td_ele
    ele += "</ul></nav>"
    """将标签链接mark_safe返回"""
    return mark_safe(ele)



@register.simple_tag
def get_order_factor(column,current_order_field,forloop,all_filter):
    if column in current_order_field:
        last_order_index = current_order_field[column]
        if last_order_index.startswith('-'):
            current_sort_index = last_order_index.strip('-')
            current_sort_index = '?_o=%s%s' % (current_sort_index, all_filter)
        else:
            current_sort_index = '?_o=-%s%s'%(last_order_index,all_filter)
        return current_sort_index
    else:
        return '?_o=%s%s'%(forloop,all_filter)


@register.simple_tag
def all(current_order_field):
    return list(current_order_field.values())[0] if current_order_field else ''

@register.simple_tag
def build_add_tags(urls_name):#将页面添加表数据的链接改掉，这个可以写在setting里面
    add_links = '/mycrm/'
    for i in urls_name:
        i += '/'
        add_links += i
    add_links += 'add'
    return add_links


@register.simple_tag
def get_field_value(form_obj,field):
    return getattr(form_obj.instance,field)

@register.simple_tag
def get_available_m2m_data(field_name,form_obj,admin_class):
    field_obj = admin_class.model._meta.get_field(field_name)
    obj_list = field_obj.related_model.objects.all()
    if not admin_class.form_add:
        obj_list = set(obj_list)
        selected_data = set(getattr(form_obj.instance,field_name).all())
        return obj_list - selected_data
    else:
        return obj_list


@register.simple_tag
def get_selected_m2m_data(field_name,form_obj,admin_class):
    selected_data = ''
    if not admin_class.form_add:
        selected_data = getattr(form_obj.instance,field_name).all()
    return selected_data


@register.simple_tag
def display_all_related_objs(obj):
    """显示要被删除的所有关联的对象"""
    ele = '<div class="col-lg-offset-2"><ul>'
    ele += '<li>%s</li>'%obj
    for reversed_fk_obj in obj._meta.related_objects:
        related_table_name = reversed_fk_obj.name
        related_lookup_key = '%s_set'%related_table_name
        related_objs = getattr(obj,related_lookup_key).all()
        ele += '<li>%s<ul>'%related_table_name
        for i in related_objs:
            ele += "<li>%s</li>"%i
            ele += display_all_related_objs(i)
        ele += '</ul></li>'
    ele += "</ul></div>"
    return ele

