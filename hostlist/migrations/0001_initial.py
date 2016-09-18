# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Catagory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('catagoryen', models.CharField(max_length=30, verbose_name='\u7c7b\u522b\u7b80\u79f0', blank=True)),
                ('catagorycn', models.CharField(max_length=30, verbose_name='\u7c7b\u522b\u5168\u79f0', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='DataCenter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dcen', models.CharField(max_length=30, verbose_name='\u673a\u623f\u7b80\u79f0', blank=True)),
                ('dccn', models.CharField(max_length=30, verbose_name='\u673a\u623f\u5168\u79f0', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Dzhuser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=30, verbose_name='\u7528\u6237\u540d', blank=True)),
                ('engineer', models.CharField(max_length=30, verbose_name='\u7ef4\u62a4\u4eba\u5458', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='HostList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', models.CharField(max_length=60, verbose_name='UUID', blank=True)),
                ('ip', models.CharField(max_length=15, verbose_name='IP\u5730\u5740', blank=True)),
                ('hostname', models.CharField(max_length=30, verbose_name='\u4e3b\u673a\u540d')),
                ('minionid', models.CharField(max_length=60, verbose_name='MinionID')),
                ('nocn', models.CharField(max_length=30, verbose_name='\u8fd0\u8425\u5546\u5168\u79f0')),
                ('catagorycn', models.CharField(max_length=30, verbose_name='\u7c7b\u522b', blank=True)),
                ('pacn', models.CharField(max_length=30, verbose_name='\u5730\u533a\u5168\u79f0')),
                ('dccn', models.CharField(max_length=30, verbose_name='\u673a\u623f\u5168\u79f0', blank=True)),
                ('engineer', models.CharField(max_length=30, verbose_name='\u7ef4\u62a4\u4eba\u5458', blank=True)),
                ('macaddr', models.CharField(max_length=20, verbose_name='MAC\u5730\u5740', blank=True)),
                ('zsourceip', models.CharField(max_length=30, verbose_name='\u4e3b\u884c\u60c5\u6e90', blank=True)),
                ('bsourceip', models.CharField(max_length=30, verbose_name='\u5907\u884c\u60c5\u6e90', blank=True)),
                ('licdate', models.CharField(max_length=30, verbose_name='\u6388\u6743\u65e5\u671f', blank=True)),
                ('licstatus', models.CharField(max_length=30, verbose_name='\u6388\u6743\u72b6\u6001', blank=True)),
                ('idip', models.CharField(max_length=15, verbose_name='MinionID\u4e2d\u7684IP\u5730\u5740', blank=True)),
                ('ipsame', models.CharField(max_length=10, verbose_name='IP\u5730\u5740\u4e00\u81f4\u6027', blank=True)),
                ('remark', models.TextField(max_length=200, verbose_name='\u5907\u6ce8', blank=True)),
            ],
            options={
                'ordering': ['minionid'],
            },
        ),
        migrations.CreateModel(
            name='NetworkOperator',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('noen', models.CharField(max_length=30, verbose_name='\u8fd0\u8425\u5546\u7b80\u79f0', blank=True)),
                ('nocn', models.CharField(max_length=30, verbose_name='\u8fd0\u8425\u5546\u5168\u79f0', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProvinceArea',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('paen', models.CharField(max_length=30, verbose_name='\u7701\u4efd\u5730\u533a\u7b80\u79f0', blank=True)),
                ('pacn', models.CharField(max_length=30, verbose_name='\u7701\u4efd\u5730\u533a\u5168\u79f0', blank=True)),
            ],
        ),
    ]
