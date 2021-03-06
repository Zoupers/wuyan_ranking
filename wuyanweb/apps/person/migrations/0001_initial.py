# Generated by Django 2.1.4 on 2019-03-06 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=50, verbose_name='姓名')),
                ('sex', models.CharField(blank=True, max_length=6, null=True, verbose_name='性别')),
                ('constellation', models.CharField(blank=True, max_length=10, null=True, verbose_name='星座')),
                ('birthday', models.CharField(blank=True, max_length=30, null=True, verbose_name='生辰')),
                ('birthplace', models.CharField(blank=True, max_length=100, null=True, verbose_name='出生地')),
                ('profession', models.CharField(blank=True, max_length=60, null=True, verbose_name='职业')),
                ('imdb', models.CharField(blank=True, max_length=15, null=True, verbose_name='IMDB编号')),
                ('introduce', models.TextField(blank=True, null=True, verbose_name='简介')),
                ('poster', models.CharField(blank=True, max_length=60, null=True, verbose_name='人物海报')),
                ('image', models.TextField(blank=True, null=True, verbose_name='人物照片')),
            ],
            options={
                'verbose_name': '人物',
                'verbose_name_plural': '人物',
            },
        ),
    ]
