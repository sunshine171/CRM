from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser,PermissionsMixin
)


class UserProfileManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
        )
        # user.is_admin = True
        user.is_superuser = True#这里也改为is_superuser
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=32,verbose_name="姓名")  # 生日改成name
    is_active = models.BooleanField(default=True)
    # is_admin = models.BooleanField(default=False)#实现不了真正的权限，is_superuser
    is_staff = models.BooleanField(default=True)
    role = models.ManyToManyField("Role", blank=True)  # 双向一对多==多对多
    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email


    class Meta:
        permissions = (
            ('mycrm_table_list','查看具体数据展示,包括排序、搜索、过滤'),#过滤排序，。。都是GET方式，
            # ('mycrm_table_list_post','查看具体数据展示'),
            ('mycrm_table_change_view','查看具体数据的修改页面'),
            ('mycrm_table_change','查看具体数据的修改页面，并进行修改'),
            ('mycrm_table_add','看增加页面，并增加数据'),
            ('mycrm_table_add_view','查看增加页面'),
            ('mycrm_table_list_db','可以查看表名字数据'),
            ('mycrm_table_delete_view','查看具体删除数据展示'),
            ('mycrm_table_delete','查看具体删除数据展示，并删除'),
        )

#han_perm和has_module_perms实现了用户认证,只针对is_admin用户有效
    # def has_perm(self, perm, obj=None):
    #     "Does the user have a specific permission?"
    #     # Simplest possible answer: Yes, always
    #     return True
    #
    # def has_module_perms(self, app_label):
    #     "Does the user have permissions to view the app `app_label`?"
    #     # Simplest possible answer: Yes, always
    #     return True



    # # @property
    # # def is_staff(self):
    # #     "Is the user a member of staff?"
    # #     # Simplest possible answer: All admins are staff
    # #     return self.is_admin







# class UserProfile(models.Model):
#     """
#     用户信息表
#     """
#     user = models.OneToOneField(User,on_delete=models.CASCADE)  # 创建外键，关联django用户表
#     # 扩展用户字段
#     name = models.CharField(max_length=32, verbose_name="姓名")  # 生日改成name
#     role = models.ManyToManyField("Role", blank=True)  # 双向一对多==多对多
#
#     def __str__(self):
#         return self.name




class Role(models.Model):
    """
    角色表
    """
    name = models.CharField(max_length=32, unique=True)  # 角色名不可以重复
    menus = models.ManyToManyField("Menus", blank=True)

    def __str__(self):
        return self.name


class CustomerInfo(models.Model):
    """
    客户信息
    """
    name = models.CharField(max_length=32,default=None)  # 首次报名可能不知道名字
    source_choices = (
        (0, 'QQ群'),
        (1, '51CTO'),
        (2, '百度推广'),
        (3, '知乎'),
        (4, '转介绍'),
        (5, '其它')
    )
    source = models.SmallIntegerField(choices=source_choices)
    referral_from = models.ForeignKey("self", blank=True, null=True, verbose_name="转介绍",on_delete=models.CASCADE)  # 关联自己
    contact_type_choices = (
        (0, 'qq'),
        (1, '微信'),
        (2, '手机'),
    )
    contact_type = models.SmallIntegerField(choices=contact_type_choices)
    contact = models.CharField(max_length=64, unique=True)
    consult_courses = models.ManyToManyField("Course", verbose_name="咨询课程")
    consult_content = models.TextField(verbose_name="咨询内容")
    consultant = models.ForeignKey("UserProfile", verbose_name="课程顾问",on_delete=models.CASCADE)
    status_choices = (
        (0, '未报名'),
        (1, '已报名'),
        (2, '已退学'),
    )
    status = models.SmallIntegerField(choices=status_choices)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return "%s"%self.name

class CustomerFollowUp(models.Model):
    """
    客户跟踪记录表
    """
    customer = models.ForeignKey('CustomerInfo',on_delete=models.CASCADE)
    content = models.TextField(verbose_name="跟踪内容")
    user = models.ForeignKey('UserProfile', verbose_name="跟进人",on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    status_choices = (
        (0, '近期无报名计划'),
        (1, '一个月内报名'),
        (2, '2周内报名'),
        (3, '已报名'),
    )
    status = models.SmallIntegerField(choices=status_choices, verbose_name="跟进状态")

    def __str__(self):
        return self.content


class Course(models.Model):
    """
    课程
    """
    name = models.CharField(verbose_name="课程名", unique=True, max_length=64)
    price = models.PositiveSmallIntegerField()
    outline = models.TextField(verbose_name="课程大纲")
    period = models.PositiveSmallIntegerField(verbose_name="课程周期(月)", default=5)

    def __str__(self):
        return self.name


class ClassList(models.Model):
    """
    班级列表
    """
    branch = models.ForeignKey('Branch',on_delete=models.CASCADE)  # 关联校区
    course = models.ForeignKey("Course",on_delete=models.CASCADE)
    class_type_choices = ((0, '脱产'), (1, '周末'), (2, '网络班'))
    class_type = models.SmallIntegerField(choices=class_type_choices, default=0)
    semester = models.SmallIntegerField(verbose_name="学期")
    contract_template = models.ForeignKey('ContractTemplate',blank=True,null=True,on_delete=models.CASCADE)
    teachers = models.ManyToManyField('UserProfile', verbose_name="讲师")
    start_date = models.DateField(verbose_name="开班日期")
    graduate_date = models.DateField("毕业日期", blank=True, null=True)

    def __str__(self):
        return "{0}({1})期".format(self.course.name, self.semester)

    class Meta:
        """联合唯一"""
        unique_together = ('branch', 'course', 'semester')


class CourseRecord(models.Model):
    """
    上课记录
    """
    class_grade = models.ForeignKey("ClassList", verbose_name="上课班级",on_delete=models.CASCADE)
    day_num = models.PositiveSmallIntegerField(verbose_name="课程节次")
    teacher = models.ForeignKey("UserProfile", verbose_name="本节讲师",on_delete=models.CASCADE)
    title = models.CharField("本节主题", max_length=64)
    content = models.TextField("本节内容")
    has_homework = models.BooleanField("本节有作业", default=True)
    homework = models.TextField("作业需求", blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{0}第{1}节".format(self.class_grade, self.day_num)

    class Meta:
        unique_together = ('class_grade', 'day_num')


class StudyRecord(models.Model):
    """
    学习记录
    """
    course_record = models.ForeignKey(CourseRecord,on_delete=models.CASCADE)
    student = models.ForeignKey("Student",on_delete=models.CASCADE)
    score_choices = (
        (100, "A+"),
        (90, "A"),
        (85, "B+"),
        (80, "B"),
        (75, "B-"),
        (70, "C+"),
        (60, "C"),
        (40, "C-"),
        (-50, "D"),
        (0, "N/A"),
    )
    score = models.SmallIntegerField(choices=score_choices)
    show_choices = (
        (0, "缺勤"),
        (1, "已签到"),
        (2, "迟到"),
        (3, "早退"),
    )
    show_status = models.SmallIntegerField(choices=show_choices, default=1)
    note = models.TextField("成绩备注", blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{0} {1} {2}".format(self.course_record, self.student, self.score)


class Student(models.Model):
    """
    学员表
    """
    customer = models.ForeignKey("CustomerInfo",on_delete=models.CASCADE)
    class_grade = models.ManyToManyField("ClassList")

    def __str__(self):
        return self.customer


class Branch(models.Model):
    """
    校区
    """
    name = models.CharField(max_length=32, unique=True)
    addr = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return self.name


class Menus(models.Model):
    """动态菜单"""
    name = models.CharField(max_length=64)
    url_type_choices = (
        (0, 'absolute'),
        (1, 'dynamic')
    )
    url_type = models.SmallIntegerField(choices=url_type_choices, default=0)
    url_name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('name', 'url_name')


class PaymentRecord(models.Model):
    """报名缴费记录"""
    enrollment = models.ForeignKey('StudentEnrollment',on_delete=models.CASCADE)
    payment_type_choices = ((0,'报名费'),(1,'学费'),(2,'退费'))
    payment_type = models.SmallIntegerField(choices=payment_type_choices,default=0)
    amount = models.IntegerField('费用',default=500)
    consultant = models.ForeignKey('UserProfile',on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return '%s'%self.enrollment

class StudentEnrollment(models.Model):
    """学生报名表"""
    customer = models.ForeignKey('CustomerInfo',on_delete=models.CASCADE)
    consultant = models.ForeignKey('UserProfile',on_delete=models.CASCADE)
    class_grade = models.ForeignKey('ClassList',on_delete=models.CASCADE)
    contract_agreed = models.BooleanField(default=False)
    contract_signed_date = models.DateTimeField(blank=True,null=True)
    contract_approved = models.BooleanField(default=False)
    contract_approved_date = models.DateTimeField(blank=True,null=True)

    class Meta:
        unique_together = ('customer','class_grade')

    def __str__(self):
        return '%s'%self.customer




class ContractTemplate(models.Model):
    """合同模板表"""
    name = models.CharField(max_length=64)
    content = models.TextField()

    date = models.DateField(auto_now_add=True)
