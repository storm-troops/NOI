from django.db import models


class UserInfo(models.Model):
    """
    用户表
    """
    username = models.CharField(verbose_name='用户名', max_length=32, null=True, blank=True)
    password = models.CharField(verbose_name='密码', max_length=64, null=True, blank=True)
    email = models.CharField(verbose_name='邮箱', max_length=32, null=True, blank=True)
    roles = models.ManyToManyField(verbose_name='拥有的所有角色', to='Role', blank=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural = "01.用户表"


class Role(models.Model):
    """
    角色
    """
    title = models.CharField(verbose_name='角色名称', max_length=32,unique=True,blank=True,null=True)
    permissions = models.ManyToManyField(verbose_name='拥有的所有权限', to='Permission', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "02.角色表"


class Menu(models.Model):
    """
    菜单
    """
    title = models.CharField(verbose_name='菜单', max_length=32)
    icon = models.CharField(verbose_name='图标', max_length=32)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "03.菜单表"


class Permission(models.Model):
    """
    权限表
    """
    title = models.CharField(verbose_name='标题', max_length=32)
    url = models.CharField(verbose_name='含正则的URL', max_length=128, unique=True)

    name = models.CharField(verbose_name='代码', max_length=64, unique=True, null=False, blank=False)

    pid = models.ForeignKey(verbose_name='默认选中权限', to='Permission', related_name='ps', null=True, blank=True,
                            help_text="对于无法作为菜单的URL，可以为其选择一个可以作为菜单的权限，那么访问时，则默认选中此权限",
                            limit_choices_to={'menu__isnull': False}, on_delete=models.SET_NULL)

    menu = models.ForeignKey(verbose_name='菜单', to='Menu', null=True, blank=True, help_text='null表示非菜单',
                             on_delete=models.SET_NULL)

    class Meta:
        verbose_name_plural = "04.权限表"

    def __str__(self):
        return self.title


class Category(models.Model):
    """题目类别表"""
    title = models.CharField(verbose_name="类别", max_length=32, null=True, blank=True,unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "05.题目类别表"


class Tag(models.Model):
    title = models.CharField(verbose_name='标签名称', max_length=32,null=True, blank=True,unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "06.标签表"


class Examination_details(models.Model):
    """
        题目详情表
    """
    rubric_number = models.CharField(verbose_name="题目编号", max_length=32, null=True, blank=True,unique=True)
    rubric_name = models.CharField(verbose_name="题目名称", max_length=32, null=True, blank=True)
    rubric_describe = models.CharField(verbose_name="题目描述", max_length=128, null=True, blank=True)
    input_text = models.CharField(verbose_name="输入说明", max_length=64, null=True, blank=True)
    examination_status_choices = (
        (0, "未审核"),
        (1, "已审核")
    )
    examination_status = models.IntegerField(verbose_name="审核状态", choices=examination_status_choices, default=0)
    memory = models.CharField(verbose_name="内存", max_length=32, null=True, blank=True)
    time_bar = models.CharField(verbose_name="时间限制", max_length=32, null=True, blank=True)
    author = models.ForeignKey(verbose_name="出题人", to="UserInfo")
    sample_input = models.CharField(verbose_name="样例输入", max_length=336,null=True, blank=True)
    sample_out = models.CharField(verbose_name="样例输出", max_length=336,null=True, blank=True)
    review_code = models.CharField(verbose_name="评测源码", max_length=128,null=True, blank=True)
    rubric_type = models.ForeignKey(verbose_name="题目类型", to="Category")  # 外键题目类型
    difficulty_choices = (
        (0, "初级"),
        (1, "中级"),
        (2, "高级"),
    )
    difficulty = models.IntegerField(verbose_name="难度", choices=difficulty_choices, default=0)
    hint = models.CharField(verbose_name="题目提示", max_length=64)
    tag = models.ForeignKey(verbose_name="标签", to="Tag")  # 外键标签

    def __str__(self):
        return self.rubric_name

    class Meta:
        verbose_name_plural = "07.题目详情表"


class Answerrecord(models.Model):
    """
        答题记录表
    """
    question = models.ForeignKey(to='Examination_details', verbose_name="关联题目表", null=True, blank=True)
    user = models.ForeignKey(to='UserInfo', verbose_name="关联用户表", null=True, blank=True)
    answer_choices = (
        (0, "通过"),
        (1, "未通过"),
        (2, "超时"),
    )
    result = models.IntegerField(verbose_name="答题结果", choices=answer_choices, default=0)
    score = models.PositiveIntegerField(verbose_name="分数", null=True, blank=True)
    length = models.FloatField(verbose_name="代码长度", default=True, blank=True)
    language_choices = (
        (0, "C"),
        (1, "C++"),
        (2, "Java"),
        (3, "Python"),
        (4, "GO"),
        (5, "PHP"),
    )
    language = models.IntegerField(verbose_name="编程语言", choices=language_choices, default=0)
    submit_or_timeout_datetime = models.DateTimeField(verbose_name="时间", auto_now_add=True)

    def __str__(self):
        return self.user.username, self.question.rubric_name

    class Meta:
        verbose_name_plural = "08.答题记录表"


class Examination_Record(models.Model):
    """ 用户答题记录情况表"""
    user = models.ForeignKey(to='UserInfo', null=False, verbose_name='用户id')
    examination_count = models.IntegerField(verbose_name='答题总数量')
    pass_count = models.IntegerField(verbose_name='答题通过数量')

    class Meta:
        verbose_name_plural = "09.用户答题记录情况表"
