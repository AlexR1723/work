# Generated by Django 2.2.7 on 2020-01-30 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AuthUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('is_superuser', models.BooleanField()),
                ('username', models.CharField(max_length=150, unique=True)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=150)),
                ('email', models.CharField(max_length=254)),
                ('is_staff', models.BooleanField()),
                ('is_active', models.BooleanField()),
                ('date_joined', models.DateTimeField()),
            ],
            options={
                'db_table': 'auth_user',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='BecomePerformer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(blank=True, max_length=5000, null=True, verbose_name='Текст')),
            ],
            options={
                'verbose_name': 'Текст',
                'verbose_name_plural': "Текст 'Как стать исполнителем'",
                'db_table': 'become_performer',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='BenefitsSafe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('header', models.CharField(blank=True, max_length=200, null=True, verbose_name='Заголовок')),
                ('text', models.TextField(blank=True, max_length=500, null=True, verbose_name='Текст')),
                ('image', models.ImageField(blank=True, null=True, upload_to='uploads/', verbose_name='Изображение')),
            ],
            options={
                'verbose_name': 'Преимущества безопасной сделки',
                'verbose_name_plural': 'Преимущество безопасной сделки',
                'db_table': 'benefits_safe',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Наименование категории')),
                ('image', models.ImageField(blank=True, null=True, upload_to='uploads/category/', verbose_name='Иконка')),
                ('text', models.TextField(blank=True, null=True, verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
                'db_table': 'category',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True, verbose_name='Наименование')),
            ],
            options={
                'verbose_name': 'Город',
                'verbose_name_plural': 'Города',
                'db_table': 'city',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(blank=True, null=True, verbose_name='Пользователь')),
                ('text', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Текст отзыва')),
            ],
            options={
                'verbose_name': 'Отзыв',
                'verbose_name_plural': 'Отзывы',
                'db_table': 'comments',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Текст')),
            ],
            options={
                'verbose_name': 'Контакт',
                'verbose_name_plural': 'Контакты',
                'db_table': 'contact',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ContactType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True, verbose_name='Наименование')),
            ],
            options={
                'verbose_name': 'Тип контакта',
                'verbose_name_plural': 'Типы контактов',
                'db_table': 'contact_type',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='FirstSlider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(blank=True, max_length=100, null=True, verbose_name='Заголовок')),
                ('description', models.CharField(blank=True, max_length=500, null=True, verbose_name='Описание')),
                ('image', models.ImageField(blank=True, null=True, upload_to='uploads/', verbose_name='Изображение')),
            ],
            options={
                'verbose_name': 'Слайд',
                'verbose_name_plural': 'Слайдер',
                'db_table': 'first_slider',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Gender',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=10, null=True)),
            ],
            options={
                'db_table': 'gender',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='HelpCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, null=True, verbose_name='Наименование')),
                ('image', models.ImageField(blank=True, null=True, upload_to='uploads/', verbose_name='Картинка')),
            ],
            options={
                'verbose_name': 'Категория вопроса',
                'verbose_name_plural': 'Категории вопросов',
                'db_table': 'help_category',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='HelpSubcategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(blank=True, max_length=500, null=True, verbose_name='Текст вопроса')),
            ],
            options={
                'verbose_name': 'Вопрос',
                'verbose_name_plural': 'Вопросы',
                'db_table': 'help_subcategory',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.CharField(blank=True, max_length=100, null=True, verbose_name='Ссылка')),
                ('icon', models.CharField(blank=True, max_length=100, null=True, verbose_name='Иконка')),
            ],
            options={
                'verbose_name': 'Ссылка',
                'verbose_name_plural': 'Ссылки',
                'db_table': 'link',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='OrderService',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, max_length=5000, null=True, verbose_name='Текст')),
            ],
            options={
                'verbose_name': 'Текст',
                'verbose_name_plural': "Текст 'Как заказать услугу'",
                'db_table': 'order_service',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PrivacyRules',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(verbose_name='Порядковый номер')),
                ('header', models.CharField(blank=True, max_length=500, null=True, verbose_name='Заголовок')),
                ('text', models.TextField(blank=True, help_text='Подпункты разделять двойным переносом строки', null=True, verbose_name='Текст')),
            ],
            options={
                'verbose_name': 'Правило конфиденциальности',
                'verbose_name_plural': 'Правила конфиденциальности',
                'db_table': 'privacy_rules',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ProjectRules',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(verbose_name='Порядковый номер')),
                ('header', models.CharField(blank=True, max_length=500, null=True, verbose_name='Заголовок')),
                ('text', models.TextField(blank=True, help_text='Подпункты разделять двойным переносом строки', null=True, verbose_name='Текст')),
            ],
            options={
                'verbose_name': 'Правило проекта',
                'verbose_name_plural': 'Правила проекта',
                'db_table': 'project_rules',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PublicOffer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(verbose_name='Порядковый номер')),
                ('header', models.CharField(blank=True, max_length=500, null=True, verbose_name='Заголовок')),
                ('text', models.TextField(blank=True, help_text='Подпункты разделять двойным переносом строки', null=True, verbose_name='Текст')),
            ],
            options={
                'verbose_name': 'Публичная оферта',
                'verbose_name_plural': 'Публичные оферта',
                'db_table': 'public_offer',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True, verbose_name='Наименование')),
            ],
            options={
                'verbose_name': 'Регион',
                'verbose_name_plural': 'Регионы',
                'db_table': 'region',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Наименование')),
                ('image', models.ImageField(blank=True, null=True, upload_to='uploads/subcategory/', verbose_name='Картинка')),
                ('price', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Подкатегория',
                'verbose_name_plural': 'Подкатегории',
                'db_table': 'sub_category',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UserAdvert',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=200, null=True)),
                ('description', models.CharField(blank=True, max_length=5000, null=True)),
                ('photo_main', models.ImageField(blank=True, max_length=500, null=True, upload_to='uploads/advert/')),
                ('date', models.DateField(blank=True, null=True)),
                ('price', models.IntegerField(blank=True, null=True)),
                ('count_offer', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'user_advert',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UserOffer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_accept', models.BooleanField(blank=True, null=True)),
                ('date', models.DateField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'user_offer',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(blank=True, max_length=13, null=True)),
                ('uuid', models.CharField(blank=True, max_length=50, null=True)),
                ('birthday', models.DateField(blank=True, null=True)),
                ('about_me', models.CharField(blank=True, default=' ', max_length=5000, null=True)),
                ('get_new_order', models.BooleanField(blank=True, null=True)),
                ('get_notice_status', models.BooleanField(blank=True, null=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='uploads/users/')),
                ('verify_phone', models.BooleanField(blank=True, null=True)),
                ('verify_passport', models.BooleanField(blank=True, null=True)),
                ('passport_photo', models.ImageField(blank=True, max_length=500, null=True, upload_to='uploads/users/')),
                ('verify_date', models.DateField(blank=True, null=True)),
                ('passport_num_ser', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'db_table': 'users',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UserTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=500, null=True)),
                ('description', models.CharField(blank=True, max_length=5000, null=True)),
                ('address', models.CharField(blank=True, max_length=100, null=True)),
                ('date', models.DateField(blank=True, null=True)),
                ('start_time', models.TimeField(blank=True, null=True)),
                ('end_time', models.TimeField(blank=True, null=True)),
                ('pay', models.TextField(blank=True, null=True)),
                ('photo_main', models.ImageField(blank=True, max_length=500, null=True, upload_to='uploads/task/')),
                ('price', models.IntegerField(blank=True, null=True)),
                ('date_add', models.DateField(blank=True, null=True)),
                ('rezult_text', models.CharField(blank=True, max_length=5000, null=True)),
                ('exec_finish', models.BooleanField(blank=True, null=True)),
            ],
            options={
                'db_table': 'user_task',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UserTaskStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'db_table': 'user_task_status',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UserType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'db_table': 'user_type',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='WhatSafe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, max_length=5000, null=True, verbose_name='Текст')),
            ],
            options={
                'verbose_name': 'Текст',
                'verbose_name_plural': "Текст 'Что такое безопасная сделка'",
                'db_table': 'what_safe',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='WhyWe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('header', models.CharField(blank=True, max_length=500, null=True, verbose_name='Заголовок')),
                ('text', models.CharField(blank=True, max_length=500, null=True, verbose_name='Текст')),
                ('image', models.ImageField(blank=True, null=True, upload_to='uploads/', verbose_name='Картинка')),
                ('left', models.BooleanField(blank=True, default=True, null=True, verbose_name='Картинка слева?')),
            ],
            options={
                'verbose_name': 'Текст',
                'verbose_name_plural': "Текст 'Почему мы'",
                'db_table': 'why_we',
                'managed': False,
            },
        ),
    ]