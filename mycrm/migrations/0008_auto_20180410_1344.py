# Generated by Django 2.0.4 on 2018-04-10 05:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mycrm', '0007_auto_20180410_1035'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userprofile',
            options={'permissions': (('mycrm_table_list', '查看具体数据展示'), ('mycrm_table_list_post', '查看具体数据展示,包括排序、搜索、过滤'), ('mycrm_table_change_view', '查看具体数据的修改页面'), ('mycrm_table_change', '查看具体数据的修改页面，并进行修改'), ('mycrm_table_add', '看增加页面，并增加数据'), ('mycrm_table_add_view', '查看增加页面'), ('mycrm_table_list_db', '可以查看表数据'), ('mycrm_table_delete_view', '查看具体删除数据展示'), ('mycrm_table_delete', '查看具体删除数据展示，并删除'))},
        ),
    ]
