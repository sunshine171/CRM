# Generated by Django 2.0.4 on 2018-04-10 02:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mycrm', '0006_remove_userprofile_is_admin'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userprofile',
            options={'permissions': (('mycrm_table_list', '可以查看mycrm中每张表的数据'), ('mycrm_table_list_view', '可以查看mycrm中每条数据的修改页'), ('mycrm_table_list_change', '可以查看mycrm中每条数据进行修改'), ('mycrm_table_list_add', '可以查看mycrm中每条数据进行修改'), ('mycrm_table_list_add_views', '可以查看mycrm中每条数据进行修改'))},
        ),
    ]
