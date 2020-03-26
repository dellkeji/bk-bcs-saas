/*
 * Tencent is pleased to support the open source community by making 蓝鲸智云PaaS平台社区版 (BlueKing PaaS Community Edition) available.
 * Copyright (C) 2017-2019 THL A29 Limited, a Tencent company. All rights reserved.
 * Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 * http://opensource.org/licenses/MIT
 * Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
 * an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
 * specific language governing permissions and limitations under the License.
 */

package models

// BcsServiceConf : 用于存储bcs service层的信息
//go:generate goqueryset -in ${GOFILE} -out qs_${GOFILE}
// gen:qs
type BcsServiceConf struct {
	Model
	KindName      string `json:"kind_name" gorm:"size:16"`
	Environment   string `json:"environment" gorm:"size:16;unique_index:uix_kind_name_environment"`
	Description   string `json:"description" sql:"size:256"`
	Configuration string `json:"configuration" sql:"type:text"`
	Creator       string `json:"creator" gorm:"size:32"`
}
