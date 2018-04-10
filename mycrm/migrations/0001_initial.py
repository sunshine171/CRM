# Generated by Django 2.0.4 on 2018-04-09 13:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True)),
                ('addr', models.CharField(blank=True, max_length=128, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ClassList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_type', models.SmallIntegerField(choices=[(0, '脱产'), (1, '周末'), (2, '网络班')], default=0)),
                ('semester', models.SmallIntegerField(verbose_name='学期')),
                ('start_date', models.DateField(verbose_name='开班日期')),
                ('graduate_date', models.DateField(blank=True, null=True, verbose_name='毕业日期')),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mycrm.Branch')),
            ],
        ),
        migrations.CreateModel(
            name='ContractTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('content', models.TextField()),
                ('date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='课程名')),
                ('price', models.PositiveSmallIntegerField()),
                ('outline', models.TextField(verbose_name='课程大纲')),
                ('period', models.PositiveSmallIntegerField(default=5, verbose_name='课程周期(月)')),
            ],
        ),
        migrations.CreateModel(
            name='CourseRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_num', models.PositiveSmallIntegerField(verbose_name='课程节次')),
                ('title', models.CharField(max_length=64, verbose_name='本节主题')),
                ('content', models.TextField(verbose_name='本节内容')),
                ('has_homework', models.BooleanField(default=True, verbose_name='本节有作业')),
                ('homework', models.TextField(blank=True, null=True, verbose_name='作业需求')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('class_grade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mycrm.ClassList', verbose_name='上课班级')),
            ],
        ),
        migrations.CreateModel(
            name='CustomerFollowUp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='跟踪内容')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('status', models.SmallIntegerField(choices=[(0, '近期无报名计划'), (1, '一个月内报名'), (2, '2周内报名'), (3, '已报名')], verbose_name='跟进状态')),
            ],
        ),
        migrations.CreateModel(
            name='CustomerInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=None, max_length=32)),
                ('source', models.SmallIntegerField(choices=[(0, 'QQ群'), (1, '51CTO'), (2, '百度推广'), (3, '知乎'), (4, '转介绍'), (5, '其它')])),
                ('contact_type', models.SmallIntegerField(choices=[(0, 'qq'), (1, '微信'), (2, '手机')])),
                ('contact', models.CharField(max_length=64, unique=True)),
                ('consult_content', models.TextField(verbose_name='咨询内容')),
                ('status', models.SmallIntegerField(choices=[(0, '未报名'), (1, '已报名'), (2, '已退学')])),
                ('date', models.DateField(auto_now_add=True)),
                ('consult_courses', models.ManyToManyField(to='mycrm.Course', verbose_name='咨询课程')),
            ],
        ),
        migrations.CreateModel(
            name='Menus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('url_type', models.SmallIntegerField(choices=[(0, 'absolute'), (1, 'dynamic')], default=0)),
                ('url_name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='PaymentRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_type', models.SmallIntegerField(choices=[(0, '报名费'), (1, '学费'), (2, '退费')], default=0)),
                ('amount', models.IntegerField(default=500, verbose_name='费用')),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True)),
                ('menus', models.ManyToManyField(blank=True, to='mycrm.Menus')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_grade', models.ManyToManyField(to='mycrm.ClassList')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mycrm.CustomerInfo')),
            ],
        ),
        migrations.CreateModel(
            name='StudentEnrollment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contract_agreed', models.BooleanField(default=False)),
                ('contract_signed_date', models.DateTimeField(blank=True, null=True)),
                ('contract_approved', models.BooleanField(default=False)),
                ('contract_approved_date', models.DateTimeField(blank=True, null=True)),
                ('class_grade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mycrm.ClassList')),
            ],
        ),
        migrations.CreateModel(
            name='StudyRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.SmallIntegerField(choices=[(100, 'A+'), (90, 'A'), (85, 'B+'), (80, 'B'), (75, 'B-'), (70, 'C+'), (60, 'C'), (40, 'C-'), (-50, 'D'), (0, 'N/A')])),
                ('show_status', models.SmallIntegerField(choices=[(0, '缺勤'), (1, '已签到'), (2, '迟到'), (3, '早退')], default=1)),
                ('note', models.TextField(blank=True, null=True, verbose_name='成绩备注')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('course_record', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mycrm.CourseRecord')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mycrm.Student')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='姓名')),
                ('role', models.ManyToManyField(blank=True, to='mycrm.Role')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='studentenrollment',
            name='consultant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mycrm.UserProfile'),
        ),
        migrations.AddField(
            model_name='studentenrollment',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mycrm.CustomerInfo'),
        ),
        migrations.AddField(
            model_name='paymentrecord',
            name='consultant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mycrm.UserProfile'),
        ),
        migrations.AddField(
            model_name='paymentrecord',
            name='enrollment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mycrm.StudentEnrollment'),
        ),
        migrations.AlterUniqueTogether(
            name='menus',
            unique_together={('name', 'url_name')},
        ),
        migrations.AddField(
            model_name='customerinfo',
            name='consultant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mycrm.UserProfile', verbose_name='课程顾问'),
        ),
        migrations.AddField(
            model_name='customerinfo',
            name='referral_from',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mycrm.CustomerInfo', verbose_name='转介绍'),
        ),
        migrations.AddField(
            model_name='customerfollowup',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mycrm.CustomerInfo'),
        ),
        migrations.AddField(
            model_name='customerfollowup',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mycrm.UserProfile', verbose_name='跟进人'),
        ),
        migrations.AddField(
            model_name='courserecord',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mycrm.UserProfile', verbose_name='本节讲师'),
        ),
        migrations.AddField(
            model_name='classlist',
            name='contract_template',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mycrm.ContractTemplate'),
        ),
        migrations.AddField(
            model_name='classlist',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mycrm.Course'),
        ),
        migrations.AddField(
            model_name='classlist',
            name='teachers',
            field=models.ManyToManyField(to='mycrm.UserProfile', verbose_name='讲师'),
        ),
        migrations.AlterUniqueTogether(
            name='studentenrollment',
            unique_together={('customer', 'class_grade')},
        ),
        migrations.AlterUniqueTogether(
            name='courserecord',
            unique_together={('class_grade', 'day_num')},
        ),
        migrations.AlterUniqueTogether(
            name='classlist',
            unique_together={('branch', 'course', 'semester')},
        ),
    ]