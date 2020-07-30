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

from django.utils.translation import ugettext_lazy as _

from backend.components import paas_cc
from backend.utils.errcodes import ErrorCode
from backend.utils.error_codes import error_codes


def get_clusters(access_token, project_id):
    resp = paas_cc.get_all_clusters(access_token, project_id, desire_all_data=True)
    if resp.get('code') != ErrorCode.NoError:
        raise error_codes.APIError(f"get clusters error, {resp.get('message')}")
    return resp.get('data', {}).get('results', [])


def get_cluster_versions(access_token, kind="", ver_id="", env=""):
    resp = paas_cc.get_cluster_versions(access_token, kind=kind, ver_id=ver_id, env=env)
    if resp.get('code') != ErrorCode.NoError:
        raise error_codes.APIError(f"get cluster version, {resp.get('message')}")
    data = resp.get("data") or []
    version_list = []
    # 以ID排序，稳定版本排在前面
    data.sort(key=lambda info: info["id"])
    for info in data:
        configure = json.loads(info.get("configure") or "{}")
        version_list.append({
            "version_id": info["version"],
            "version_name": configure.get("version_name") or info["version"]
        })
    return version_list


def get_cluster_masters(access_token, project_id, cluster_id):
    """获取集群下的master信息
    """
    resp = paas_cc.get_master_node_list(access_token, project_id, cluster_id)
    if resp.get("code") != ErrorCode.NoError:
        raise error_codes.APIError(_("获取集群master ip失败，{}").format(resp.get("message")))
    results = resp.get("data", {}).get("results") or []
    if not results:
        raise error_codes.APIError(_("获取集群master ip为空"))
    return results


def get_cluster_nodes(access_token, project_id, cluster_id, allow_null=False):
    """获取集群下的node信息
    """
    resp = paas_cc.get_node_list(access_token, project_id, cluster_id)
    if resp.get("code") != ErrorCode.NoError:
        raise error_codes.APIError(_("获取集群node ip失败，{}").format(resp.get("message")))
    results = resp.get("data", {}).get("results") or []
    if not (results or allow_null):
        raise error_codes.APIError(_("获取集群node ip为空"))
    return results


def get_cluster_snapshot(access_token, project_id, cluster_id):
    """获取集群快照
    """
    resp = paas_cc.get_cluster_snapshot(access_token, project_id, cluster_id)
    if resp.get("code") != ErrorCode.NoError:
        raise error_codes.APIError(_("获取集群快照失败，{}").format(resp.get("message")))
    return resp.get("data") or {}


def get_cluster_info(access_token, project_id, cluster_id):
    resp = paas_cc.get_cluster(access_token, project_id, cluster_id)
    if resp.get("code") != ErrorCode.NoError:
        raise error_codes.APIError(_("获取集群信息失败，{}").format(resp.get("message")))
    return resp.get("data") or {}


def update_cluster_status(access_token, project_id, cluster_id, status):
    """更新集群状态
    """
    data = {"status": status}
    resp = paas_cc.update_cluster(access_token, project_id, cluster_id, data)
    if resp.get("code") != ErrorCode.NoError:
        raise error_codes.APIError(_("更新集群状态失败，{}").format(resp.get("message")))
    return resp.get("data") or {}
