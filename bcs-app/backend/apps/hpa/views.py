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
import logging

from django.utils import timezone
from rest_framework import views, viewsets
from rest_framework.renderers import BrowsableAPIRenderer
from rest_framework.response import Response

from backend.accounts import bcs_perm
from backend.apps.application import constants as application_constants
from backend.apps.application.base_views import BaseAPI
from backend.apps.constants import ALL_LIMIT, ProjectKind
from backend.apps.hpa import constants, utils
from backend.apps.instance import constants as instance_constants
from backend.apps.network.serializers import BatchResourceSLZ
from backend.apps.resource.views import ResourceOperate
from backend.components import paas_cc
from backend.utils.error_codes import error_codes
from backend.utils.renderers import BKAPIRenderer
from backend.utils.response import BKAPIResponse
from backend.apps.configuration.constants import K8sResourceName

logger = logging.getLogger(__name__)

class HPA(viewsets.ViewSet, BaseAPI, ResourceOperate):
    renderer_classes = (BKAPIRenderer, BrowsableAPIRenderer)
    category = K8sResourceName.K8sHPA.value

    def list(self, request, project_id):
        """获取所有HPA数据
        """
        access_token = request.user.token.access_token
        cluster_dicts = self.get_project_cluster_info(request, project_id)
        cluster_data = cluster_dicts.get('results', {}) or {}
        k8s_hpa_list = []

        namespace_res = paas_cc.get_namespace_list(access_token, project_id, limit=ALL_LIMIT)
        namespace_data = namespace_res.get('data', {}).get('results') or []
        namespace_dict = {i['name']: i['id'] for i in namespace_data}

        for cluster_info in cluster_data:
            cluster_id = cluster_info['cluster_id']
            cluster_env = cluster_info.get('environment')
            cluster_name = cluster_info['name']
            hpa_list = utils.get_cluster_hpa_list(request, project_id, cluster_id, cluster_env, cluster_name)
            k8s_hpa_list.extend(hpa_list)

        for p in k8s_hpa_list:
            p['namespace_id'] = namespace_dict.get(p['namespace'])

        perm = bcs_perm.Namespace(request, project_id, bcs_perm.NO_RES)
        k8s_hpa_list = perm.hook_perms(k8s_hpa_list, ns_id_flag='namespace_id')

        return Response(k8s_hpa_list)

    def delete(self, request, project_id, cluster_id, ns_name, name):
        # 检查用户是否有命名空间的使用权限
        if request.project.kind != ProjectKind.K8S.value:
            raise error_codes.NotOpen("HPA暂时只支持K8S集群")

        username = request.user.username
        namespace_dict = self.check_namespace_use_perm(request, project_id, [ns_name])
        namespace_id = namespace_dict.get(ns_name)

        result, message = utils.delete_hpa(request, project_id, cluster_id, ns_name, namespace_id, name)
        if result is False:
            message = f'删除HPA:{name}失败[命名空间:{ns_name}], {message}'
            utils.activity_log(project_id, username, name, message, result)
            raise error_codes.APIError(message)

        message = f'删除HPA:{name}成功[命名空间:{ns_name}]'
        utils.activity_log(project_id, username, name, message, result)

        return Response({})

    def batch_delete(self, request, project_id):
        """批量删除资源
        """
        username = request.user.username
        if request.project.kind != ProjectKind.K8S.value:
            raise error_codes.NotOpen("HPA暂时只支持K8S集群")

        slz = BatchResourceSLZ(data=request.data)
        slz.is_valid(raise_exception=True)
        data = slz.data['data']
        # 检查用户是否有命名空间的使用权限
        namespace_list = set([_d.get('namespace') for _d in data])
        namespace_dict = self.check_namespace_use_perm(request, project_id, namespace_list)
        success_list = []
        failed_list = []
        for _d in data:
            cluster_id = _d.get('cluster_id')
            name = _d.get('name')
            ns_name = _d.get('namespace')
            ns_id = namespace_dict.get(ns_name)
            # 删除 hpa
            result, message = utils.delete_hpa(request, project_id, cluster_id, ns_name, ns_id, name)
            if result is False:
                failed_list.append({
                    'name': name,
                    'desc': f'{name}[命名空间:{ns_name}]:{message}'
                })
            else:
                success_list.append({
                    'name': name,
                    'desc': f'{name}[命名空间:{ns_name}]'
                })

        # 添加操作审计
        if success_list:
            name_list = [_s.get('name') for _s in success_list]
            desc_list = [_s.get('desc') for _s in success_list]

            desc_list_msg = ";".join(desc_list)
            message = f"以下{self.category}删除成功:{desc_list_msg}"

            utils.activity_log(project_id, username, ';'.join(name_list), message, True)

        if failed_list:
            name_list = [_s.get('name') for _s in failed_list]
            desc_list = [_s.get('desc') for _s in failed_list]

            desc_list_msg = ";".join(desc_list)
            message = f"以下{self.category}删除失败:{desc_list_msg}"

            utils.activity_log(project_id, username, ';'.join(name_list), message, False)

        # 有一个失败，则返回失败
        if failed_list:
            raise error_codes.APIError(message)

        return BKAPIResponse({}, message=message)

class HPAMetrics(views.APIView):
    renderer_classes = (BKAPIRenderer, BrowsableAPIRenderer)

    def get(self, request, project_id):
        """获取支持的HPA metric列表
        """
        return Response(constants.HPA_METRICS)
