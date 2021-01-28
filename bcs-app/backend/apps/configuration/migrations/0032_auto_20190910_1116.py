# -*- coding: utf-8 -*-
#
# Tencent is pleased to support the open source community by making 蓝鲸智云PaaS平台社区版 (BlueKing PaaS Community Edition) available.
# Copyright (C) 2017-2019 THL A29 Limited, a Tencent company. All rights reserved.
# Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://opensource.org/licenses/MIT
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.
#
# Generated by Django 1.11.23 on 2019-09-10 03:16
from __future__ import unicode_literals

from django.db import migrations, models

import backend.apps.configuration.models.mixins


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0031_auto_20190729_1609'),
    ]

    operations = [
        migrations.CreateModel(
            name='HPA',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creator', models.CharField(max_length=32, verbose_name='创建者')),
                ('updator', models.CharField(max_length=32, verbose_name='更新者')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_time', models.DateTimeField(blank=True, null=True)),
                ('config', models.TextField(verbose_name='配置信息')),
                ('name', models.CharField(default='', max_length=255, verbose_name='名称')),
            ],
            options={
                'ordering': ('created',),
                'abstract': False,
            },
            bases=(models.Model, backend.apps.configuration.models.mixins.MConfigMapAndSecretMixin),
        )
    ]
