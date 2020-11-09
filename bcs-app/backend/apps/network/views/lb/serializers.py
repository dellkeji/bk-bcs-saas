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
import json

from rest_framework import serializers

from backend.apps.network.models import MesosLoadBlance as MesosLoadBalancer


class MesosLBSLZ(serializers.ModelSerializer):
    cluster_id = serializers.CharField()
    cluster_name = serializers.SerializerMethodField()
    data = serializers.SerializerMethodField()

    def get_data(self, obj):
        return json.loads(obj.data_dict)

    class Meta:
        model = MesosLoadBalancer
        fields = [
            "id",
            "name",
            "cluster_name",
            "cluster_id",
            "namespace",
            "ip_list"
            "status",
            "data"
        ]
