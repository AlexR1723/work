# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class About(models.Model):
    type = models.ForeignKey('AboutType', models.DO_NOTHING, blank=True, null=True)
    text = models.CharField(max_length=5000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'about'


class AboutType(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'about_type'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(unique=True, max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class BecomePerformer(models.Model):
    text = models.CharField(max_length=5000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'become_performer'


class BenefitsSafe(models.Model):
    header = models.CharField(max_length=200, blank=True, null=True)
    text = models.CharField(max_length=500, blank=True, null=True)
    image = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'benefits_safe'


class Category(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    image = models.CharField(max_length=500, blank=True, null=True)
    text = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'category'


class City(models.Model):
    region = models.ForeignKey('Region', models.DO_NOTHING, blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'city'


class Comments(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    text = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'comments'


class Contact(models.Model):
    type = models.ForeignKey('ContactType', models.DO_NOTHING, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contact'


class ContactType(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contact_type'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class FirstSlider(models.Model):
    image = models.CharField(max_length=500, blank=True, null=True)
    text = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'first_slider'


class Gender(models.Model):
    name = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gender'


class HelpCategory(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    image = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'help_category'


class HelpImages(models.Model):
    question = models.ForeignKey('HelpSubcategory', models.DO_NOTHING)
    image_path = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'help_images'


class HelpSubcategory(models.Model):
    text = models.CharField(max_length=500, blank=True, null=True)
    help_category = models.ForeignKey(HelpCategory, models.DO_NOTHING, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'help_subcategory'


class Link(models.Model):
    link = models.CharField(max_length=100, blank=True, null=True)
    icon = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'link'


class News(models.Model):
    type = models.ForeignKey('NewsType', models.DO_NOTHING, blank=True, null=True)
    text = models.CharField(max_length=500, blank=True, null=True)
    image = models.CharField(max_length=500, blank=True, null=True)
    description = models.CharField(max_length=5000, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    meta_title = models.CharField(max_length=500, blank=True, null=True)
    meta_description = models.CharField(max_length=500, blank=True, null=True)
    image_alt = models.CharField(max_length=500, blank=True, null=True)
    slug = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'news'


class NewsType(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'news_type'


class OrderService(models.Model):
    text = models.CharField(max_length=5000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'order_service'


class PrivacyRules(models.Model):
    header = models.CharField(max_length=500, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    number = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'privacy_rules'


class ProjectRules(models.Model):
    number = models.IntegerField()
    header = models.CharField(max_length=500, blank=True, null=True)
    text = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'project_rules'


class PublicOffer(models.Model):
    number = models.IntegerField()
    header = models.CharField(max_length=500, blank=True, null=True)
    text = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'public_offer'


class Region(models.Model):
    name = models.CharField(unique=True, max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'region'


class Services(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=1000, blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    image = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'services'


class SubCategory(models.Model):
    category = models.ForeignKey(Category, models.DO_NOTHING, blank=True, null=True)
    name = models.CharField(unique=True, max_length=100, blank=True, null=True)
    image = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sub_category'


class TaskPhoto(models.Model):
    task = models.ForeignKey('UserTask', models.DO_NOTHING, blank=True, null=True)
    photo = models.FileField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'task_photo'


class UserAdvert(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    subcategory = models.ForeignKey(SubCategory, models.DO_NOTHING, blank=True, null=True)
    title = models.CharField(max_length=200, blank=True, null=True)
    description = models.CharField(max_length=5000, blank=True, null=True)
    photo_main = models.CharField(max_length=500, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_advert'


class UserAdvertPhoto(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    advert = models.ForeignKey(UserAdvert, models.DO_NOTHING, blank=True, null=True)
    photo = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_advert_photo'


class UserCities(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    city = models.ForeignKey(City, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_cities'


class UserFavoritesExecutor(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    exec = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_favorites_executor'


class UserOffer(models.Model):
    user_id_customer = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='user_id_customer', blank=True, null=True)
    advert = models.ForeignKey(UserAdvert, models.DO_NOTHING, blank=True, null=True)
    is_accept = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_offer'


class UserPortfolio(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    photo = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_portfolio'


class UserSubcategories(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    subcategories = models.ForeignKey(SubCategory, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'user_subcategories'


class UserTask(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    subcategory = models.ForeignKey(SubCategory, models.DO_NOTHING, blank=True, null=True)
    title = models.CharField(max_length=500, blank=True, null=True)
    description = models.CharField(max_length=5000, blank=True, null=True)
    city = models.ForeignKey(City, models.DO_NOTHING, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    pay = models.TextField(blank=True, null=True)  # This field type is a guess.
    photo_main = models.CharField(max_length=500, blank=True, null=True)
    task_status = models.ForeignKey('UserTaskStatus', models.DO_NOTHING, db_column='task_status', blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    exec = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    date_add = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_task'


class UserTaskBet(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    task = models.ForeignKey(UserTask, models.DO_NOTHING, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_task_bet'


class UserTaskStatus(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_task_status'


class UserType(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_type'


class Users(models.Model):
    auth_user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    phone = models.CharField(max_length=13, blank=True, null=True)
    city = models.ForeignKey(City, models.DO_NOTHING, blank=True, null=True)
    type = models.ForeignKey(UserType, models.DO_NOTHING, blank=True, null=True)
    uuid = models.CharField(max_length=50, blank=True, null=True)
    gender = models.ForeignKey(Gender, models.DO_NOTHING, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    about_me = models.CharField(max_length=5000, blank=True, null=True)
    get_new_order = models.BooleanField(blank=True, null=True)
    get_notice_status = models.BooleanField(blank=True, null=True)
    photo = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'


class WhatSafe(models.Model):
    text = models.CharField(max_length=5000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'what_safe'


class WhyWe(models.Model):
    text = models.CharField(max_length=500, blank=True, null=True)
    image = models.CharField(max_length=500, blank=True, null=True)
    left = models.BooleanField(blank=True, null=True)
    header = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'why_we'
