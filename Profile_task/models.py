from django.db import models
from django.utils.translation import ugettext_lazy as _

class Link(models.Model):
    link = models.CharField(max_length=100, blank=True, null=True, verbose_name="Ссылка")
    icon = models.CharField(max_length=100, blank=True, null=True, verbose_name="Иконка")

    class Meta:
        managed = False
        db_table = 'link'
        verbose_name = _("Ссылка")
        verbose_name_plural = _("Ссылки")


class Contact(models.Model):
    type = models.ForeignKey('ContactType', models.DO_NOTHING, blank=True, null=True, verbose_name="Тип контакта")
    name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Текст")

    class Meta:
        managed = False
        db_table = 'contact'
        verbose_name = _("Контакт")
        verbose_name_plural = _("Контакты")


class ContactType(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True, verbose_name="Наименование")

    class Meta:
        managed = False
        db_table = 'contact_type'
        verbose_name = _("Тип контакта")
        verbose_name_plural = _("Типы контактов")

    def __str__(self):
        return self.name

class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class Gender(models.Model):
    name = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gender'


class Region(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True, verbose_name="Наименование")

    class Meta:
        managed = False
        db_table = 'region'
        verbose_name = _("Регион")
        verbose_name_plural = _("Регионы")

    # def cities(self):
    #     city=City.objects.filter(region=self)
    #     return city

    def first_reg(self):
        count=City.objects.filter(region=self).count()/2
        # print(count)
        reg=City.objects.filter(region=self).order_by('name')[:count]
        return reg

    def second_reg(self):
        count = City.objects.filter(region=self).count() / 2
        # print(count)
        reg = City.objects.filter(region=self).order_by('name')[count:]
        return reg



class City(models.Model):
    region = models.ForeignKey(Region, models.DO_NOTHING, blank=True, null=True, verbose_name="Регион")
    name = models.CharField(max_length=50, blank=True, null=True, verbose_name="Наименование")

    class Meta:
        managed = False
        db_table = 'city'
        verbose_name = _("Город")
        verbose_name_plural = _("Города")


class Users(models.Model):
    auth_user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    phone = models.CharField(max_length=13, blank=True, null=True)
    city = models.ForeignKey(City, models.DO_NOTHING, blank=True, null=True)
    type = models.ForeignKey('UserType', models.DO_NOTHING, blank=True, null=True)
    uuid = models.CharField(max_length=50, blank=True, null=True)
    gender = models.ForeignKey(Gender, models.DO_NOTHING, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    about_me = models.CharField(max_length=5000, blank=True, null=True)
    get_new_order = models.BooleanField(blank=True, null=True)
    get_notice_status = models.BooleanField(blank=True, null=True)
    photo = models.ImageField(upload_to='uploads/users/', max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'


class UserType(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_type'


class Category(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Наименование категории")
    image = models.ImageField(upload_to='uploads/category/', blank=True, null=True, verbose_name="Иконка")
    text = models.TextField(blank=True, null=True, verbose_name="Описание")

    class Meta:
        managed = False
        db_table = 'category'
        verbose_name = _("Категория")
        verbose_name_plural = _("Категории")

    def __str__(self):
        return self.name

    def first_sub(self):
        count=SubCategory.objects.filter(category=self).count()/2
        # print(count)
        sub=SubCategory.objects.filter(category=self).order_by('name')[:count]
        return sub

    def second_sub(self):
        count = SubCategory.objects.filter(category=self).count() / 2
        # print(count)
        sub = SubCategory.objects.filter(category=self).order_by('name')[count:]
        return sub


class SubCategory(models.Model):
    category = models.ForeignKey(Category, models.DO_NOTHING, blank=True, null=True, verbose_name="Категория")
    name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Наименование")
    image = models.ImageField(upload_to='uploads/subcategory/', blank=True, null=True, verbose_name="Картинка")

    class Meta:
        managed = False
        db_table = 'sub_category'
        verbose_name = _("Подкатегория")
        verbose_name_plural = _("Подкатегории")


class UserSubcategories(models.Model):
    user = models.ForeignKey('AuthUser', models.DO_NOTHING)
    subcategories = models.ForeignKey('SubCategory', models.DO_NOTHING)

    class Meta:
            managed = False
            db_table = 'user_subcategories'

    def count(self):
        count = UserAdvert.objects.filter(subcategory=self.subcategories).filter(user=self.user).count()
        return count


class UserCities(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    city = models.ForeignKey(City, models.DO_NOTHING, blank=True, null=True)
    # region = models.ForeignKey(Region, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_cities'

class UserAdvert(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    subcategory = models.ForeignKey(SubCategory, models.DO_NOTHING, blank=True, null=True)
    title = models.CharField(max_length=200, blank=True, null=True)
    description = models.CharField(max_length=5000, blank=True, null=True)
    photo_main = models.ImageField(upload_to='uploads/advert/',max_length=500, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_advert'

class UserAdvertPhoto(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    advert = models.ForeignKey(UserAdvert, models.DO_NOTHING, blank=True, null=True)
    photo = models.ImageField(upload_to='uploads/advert/',max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_advert_photo'

class UserPortfolio(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    photo = models.ImageField(upload_to='uploads/portfolio/',max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_portfolio'


class UserTaskStatus(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_task_status'



class UserTask(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True,related_name='user_id')
    subcategory = models.ForeignKey(SubCategory, models.DO_NOTHING, blank=True, null=True)
    title = models.CharField(max_length=500, blank=True, null=True)
    description = models.CharField(max_length=5000, blank=True, null=True)
    city = models.ForeignKey(City, models.DO_NOTHING, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    pay = models.TextField(blank=True, null=True)
    photo_main = models.ImageField(upload_to='uploads/task/',max_length=500, blank=True, null=True)
    task_status = models.ForeignKey('UserTaskStatus', models.DO_NOTHING, db_column='task_status', blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    exec = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True,related_name='exec_id')
    date_add = models.DateField(blank=True, null=True)
    rezult_text = models.CharField(max_length=5000, blank=True, null=True)
    exec_finish = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_task'

    def bet_count(self):
        count=UserTaskBet.objects.filter(task=self).count()
        return count

    def all_photo(self):
        photo=TaskPhoto.objects.filter(task=self)
        return photo

    def all_photo_rezult(self):
        photo=UserTaskRezultPhoto.objects.filter(task=self)
        return photo


class TaskPhoto(models.Model):
    task = models.ForeignKey('UserTask', models.DO_NOTHING, blank=True, null=True)
    photo = models.FileField(upload_to='uploads/task/',max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'task_photo'

    def get_type(self):
        file_types=['avi','css','dll','doc','docx','gif','html','jpeg','jpg','js','mov','mp3','pdf','php','png','ppt','psd','rar','sql','svg','tif','txt','xls','xml','zip']
        name=str(self.photo.url)
        name=name.split('.')
        count=len(name)-1
        try:
            if(file_types.index(name[count])):
                full_name='image/file_type/'+name[count]+'.png'
        except:
            full_name = 'image/file_type/txt.png'
        return full_name


class UserFavoritesExecutor(models.Model):
    user = models.ForeignKey('AuthUser', models.DO_NOTHING, blank=True, null=True)
    exec = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_favorites_executor'


class UserTaskBet(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    task = models.ForeignKey(UserTask, models.DO_NOTHING, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_task_bet'




class UserTaskRezultPhoto(models.Model):
    task = models.ForeignKey(UserTask, models.DO_NOTHING, blank=True, null=True)
    photo = models.FileField(upload_to='uploads/task_rezult/',max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_task_rezult_photo'

    def get_type(self):
        file_types=['avi','css','dll','doc','docx','gif','html','jpeg','jpg','js','mov','mp3','pdf','php','png','ppt','psd','rar','sql','svg','tif','txt','xls','xml','zip']
        name=str(self.photo.url)
        name=name.split('.')
        count=len(name)-1
        try:
            if(file_types.index(name[count])):
                full_name='image/file_type/'+name[count]+'.png'
        except:
            full_name = 'image/file_type/txt.png'
        return full_name