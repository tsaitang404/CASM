# 策略配置接口

提供对扫描策略的增删查改、关联POC插件等功能，支持对域名、IP、站点等多种扫描配置进行自定义。

## API概览

| 接口功能   | HTTP方法 | 请求路径              | 说明                     |
| ---------- | -------- | --------------------- | ------------------------ |
| 查询策略   | GET      | /api/policy/          | 获取策略列表或特定策略信息 |
| 添加策略   | POST     | /api/policy/add/      | 创建新的扫描策略         |
| 编辑策略   | POST     | /api/policy/edit/     | 修改已有策略配置         |
| 删除策略   | POST     | /api/policy/delete/   | 删除指定策略             |

## 通用字段说明

### 基础查询参数

| 字段名      | 类型     | 是否必填 | 说明                 |
| ----------- | -------- | -------- | -------------------- |
| name        | string   | 否       | 策略名称，支持模糊查询 |
| _id         | string   | 否       | 策略ID，精确查询     |
| page        | number   | 否       | 页码，默认为1        |
| size        | number   | 否       | 每页记录数，默认为10 |

### 策略配置字段

#### 域名相关配置选项（domain_config）

| 字段名            | 类型     | 是否必填 | 说明                           |
| ----------------- | -------- | -------- | ------------------------------ |
| domain_brute      | boolean  | 否       | 是否开启域名爆破，默认为true   |
| domain_brute_type | string   | 否       | 域名爆破类型，默认为"big"      |
| alt_dns           | boolean  | 否       | 是否开启DNS字典智能生成，默认为true |
| casm_search       | boolean  | 否       | 是否开启历史查询，默认为true   |
| dns_query_plugin  | boolean  | 否       | 是否开启域名插件查询，默认为false |

#### IP相关配置选项（ip_config）

| 字段名            | 类型     | 是否必填 | 说明                           |
| ----------------- | -------- | -------- | ------------------------------ |
| port_scan         | boolean  | 否       | 是否开启端口扫描，默认为true   |
| port_scan_type    | string   | 否       | 端口扫描类型，支持"test"、"top100"、"top1000"、"all"、"custom"，默认为"test" |
| service_detection | boolean  | 否       | 是否开启服务识别，默认为false  |
| os_detection      | boolean  | 否       | 是否开启操作系统识别，默认为false |
| ssl_cert          | boolean  | 否       | 是否开启SSL证书获取，默认为false |
| skip_scan_cdn_ip  | boolean  | 否       | 是否跳过CDN IP扫描，默认为true |
| port_custom       | string   | 否       | 自定义扫描端口，默认为"80,443"，仅当port_scan_type为"custom"时生效 |
| host_timeout_type | string   | 否       | 主机超时时间类别，支持"default"、"custom"，默认为"default" |
| host_timeout      | number   | 否       | 主机超时时间(秒)，默认为900    |
| port_parallelism  | number   | 否       | 探测报文并行度，默认为32       |
| port_min_rate     | number   | 否       | 最少发包速率，默认为60         |
| exclude_ports     | string   | 否       | 排除扫描的端口，默认为空       |

#### 站点相关配置选项（site_config）

| 字段名            | 类型     | 是否必填 | 说明                           |
| ----------------- | -------- | -------- | ------------------------------ |
| site_identify     | boolean  | 否       | 是否开启站点识别，默认为false  |
| site_capture      | boolean  | 否       | 是否开启站点截图，默认为false  |
| search_engines    | boolean  | 否       | 是否调用搜索引擎，默认为false  |
| site_spider       | boolean  | 否       | 是否开启站点爬虫，默认为false  |
| nuclei_scan       | boolean  | 否       | 是否开启nuclei扫描，默认为false |
| web_info_hunter   | boolean  | 否       | 是否开启JS信息收集，默认为false |

#### 资产组关联配置（scope_config）

| 字段名            | 类型     | 是否必填 | 说明                           |
| ----------------- | -------- | -------- | ------------------------------ |
| scope_id          | string   | 否       | 资产分组ID，默认为空           |

#### POC插件配置（poc_config）

| 字段名            | 类型     | 是否必填 | 说明                           |
| ----------------- | -------- | -------- | ------------------------------ |
| plugin_name       | string   | 是       | POC插件名称ID                  |
| enable            | boolean  | 否       | 是否启用，默认为true           |

#### 弱口令插件配置（brute_config）

| 字段名            | 类型     | 是否必填 | 说明                           |
| ----------------- | -------- | -------- | ------------------------------ |
| plugin_name       | string   | 是       | 弱口令插件名称ID               |
| enable            | boolean  | 否       | 是否启用，默认为true           |

## 通用响应格式

所有API响应都遵循以下格式：

```json
{
  "code": 0,       // 响应码，0表示成功，非0表示出错
  "msg": "Success", // 响应消息
  "data": {}       // 响应数据，格式因API而异
}
```

### 通用响应字段说明

| 字段名 | 类型   | 说明                                        |
| ------ | ------ | ------------------------------------------- |
| code   | number | 响应码，0表示成功，非0表示出错              |
| msg    | string | 响应消息，成功时为"Success"，失败时为错误信息 |
| data   | object | 响应数据，不同API返回的数据结构不同         |

## 详细API说明

### 1. 查询策略

**请求方法与地址**：
```
GET /api/policy/
```

**查询参数**：

通用字段说明中的基础查询参数。

**响应示例**：
```json
{
  "code": 0,
  "msg": "Success",
  "data": {
    "total": 5,
    "page": 1,
    "size": 10,
    "items": [
      {
        "_id": "60f8c2b2e13e4b1e8c8b4567",
        "name": "标准扫描策略",
        "desc": "适用于常规安全测试的标准扫描策略",
        "update_date": "2023-05-10",
        "policy": {
          "domain_config": {
            "domain_brute": true,
            "domain_brute_type": "big",
            "alt_dns": true,
            "casm_search": true,
            "dns_query_plugin": false
          },
          "ip_config": {
            "port_scan": true,
            "port_scan_type": "top100",
            "service_detection": true,
            "os_detection": false,
            "ssl_cert": true,
            "skip_scan_cdn_ip": true,
            "port_custom": "80,443",
            "host_timeout_type": "default",
            "host_timeout": 900,
            "port_parallelism": 32,
            "port_min_rate": 60,
            "exclude_ports": ""
          },
          "site_config": {
            "site_identify": true,
            "site_capture": true,
            "search_engines": false,
            "site_spider": false,
            "nuclei_scan": false,
            "web_info_hunter": false
          },
          "file_leak": false,
          "npoc_service_detection": false,
          "poc_config": [
            {
              "plugin_name": "springboot_actuator_unauthorized",
              "vul_name": "Spring Boot Actuator未授权访问",
              "enable": true
            }
          ],
          "brute_config": [
            {
              "plugin_name": "tomcat_weak_password",
              "vul_name": "Tomcat默认弱口令",
              "enable": true
            }
          ],
          "scope_config": {
            "scope_id": "60f8c2b2e13e4b1e8c8b5678"
          }
        }
      }
      // ... 更多策略
    ]
  }
}
```

**响应字段说明**：

| 字段名                       | 类型     | 说明                 |
| ---------------------------- | -------- | -------------------- |
| data.total                   | number   | 符合条件的记录总数   |
| data.page                    | number   | 当前页码             |
| data.size                    | number   | 每页记录数           |
| data.items                   | array    | 策略记录数组         |
| data.items[].\_id            | string   | 策略唯一ID           |
| data.items[].name            | string   | 策略名称             |
| data.items[].desc            | string   | 策略描述             |
| data.items[].update_date     | string   | 更新时间             |
| data.items[].policy          | object   | 策略配置详情         |
| data.items[].policy.domain_config | object | 域名相关配置       |
| data.items[].policy.ip_config | object  | IP相关配置           |
| data.items[].policy.site_config | object | 站点相关配置        |
| data.items[].policy.poc_config | array   | POC插件配置列表     |
| data.items[].policy.brute_config | array | 弱口令插件配置列表  |
| data.items[].policy.scope_config | object | 资产组关联配置     |

### 2. 添加策略

**请求方法与地址**：
```
POST /api/policy/add/
```

**请求体**：
```json
{
  "name": "定制扫描策略",
  "desc": "专门针对Web应用的深度扫描策略",
  "policy": {
    "domain_config": {
      "domain_brute": true,
      "domain_brute_type": "small",
      "alt_dns": true,
      "casm_search": true,
      "dns_query_plugin": true
    },
    "ip_config": {
      "port_scan": true,
      "port_scan_type": "custom",
      "port_custom": "80,443,8080,8443,3000,3306,6379",
      "service_detection": true,
      "os_detection": true,
      "ssl_cert": true,
      "skip_scan_cdn_ip": true
    },
    "site_config": {
      "site_identify": true,
      "site_capture": true,
      "search_engines": true,
      "site_spider": true,
      "nuclei_scan": true,
      "web_info_hunter": true
    },
    "file_leak": true,
    "npoc_service_detection": true,
    "poc_config": [
      {
        "plugin_name": "springboot_actuator_unauthorized",
        "enable": true
      },
      {
        "plugin_name": "apache_solr_rce",
        "enable": true
      }
    ],
    "brute_config": [
      {
        "plugin_name": "tomcat_weak_password",
        "enable": true
      }
    ],
    "scope_config": {
      "scope_id": "60f8c2b2e13e4b1e8c8b5678"
    }
  }
}
```

**参数说明**：

| 参数名      | 类型     | 是否必填 | 说明                 |
| ----------- | -------- | -------- | -------------------- |
| name        | string   | 是       | 策略名称             |
| desc        | string   | 否       | 策略描述信息         |
| policy      | object   | 是       | 策略配置对象         |

**响应示例**：
```json
{
  "code": 0,
  "msg": "Success",
  "data": {
    "policy_id": "60f8c2b2e13e4b1e8c8b4568"
  }
}
```

**响应字段说明**：

| 字段名         | 类型    | 说明         |
| -------------- | ------- | ------------ |
| data.policy_id | string  | 新创建的策略ID |

### 3. 编辑策略

**请求方法与地址**：
```
POST /api/policy/edit/
```

**请求体**：
```json
{
  "policy_id": "60f8c2b2e13e4b1e8c8b4567",
  "policy_data": {
    "name": "更新后的策略名称",
    "desc": "更新后的策略描述",
    "policy": {
      "domain_config": {
        "domain_brute": false
      },
      "ip_config": {
        "port_scan_type": "top1000"
      },
      "site_config": {
        "nuclei_scan": true
      },
      "file_leak": true
    }
  }
}
```

**参数说明**：

| 参数名      | 类型     | 是否必填 | 说明                           |
| ----------- | -------- | -------- | ------------------------------ |
| policy_id   | string   | 是       | 策略ID                         |
| policy_data | object   | 是       | 策略更新数据，只需包含要更新的字段 |

**响应示例**：
```json
{
  "code": 0,
  "msg": "Success",
  "data": {
    "data": {
      "name": "更新后的策略名称",
      "desc": "更新后的策略描述",
      "policy": {
        "domain_config": {
          "domain_brute": false,
          "domain_brute_type": "big",
          "alt_dns": true,
          "casm_search": true,
          "dns_query_plugin": false
        },
        "ip_config": {
          "port_scan": true,
          "port_scan_type": "top1000",
          "service_detection": true,
          "os_detection": false,
          "ssl_cert": true,
          "skip_scan_cdn_ip": true,
          "port_custom": "80,443",
          "host_timeout_type": "default",
          "host_timeout": 900,
          "port_parallelism": 32,
          "port_min_rate": 60,
          "exclude_ports": ""
        },
        "site_config": {
          "site_identify": true,
          "site_capture": true,
          "search_engines": false,
          "site_spider": false,
          "nuclei_scan": true,
          "web_info_hunter": false
        },
        "file_leak": true,
        "npoc_service_detection": false,
        "poc_config": [
          {
            "plugin_name": "springboot_actuator_unauthorized",
            "vul_name": "Spring Boot Actuator未授权访问",
            "enable": true
          }
        ],
        "brute_config": [
          {
            "plugin_name": "tomcat_weak_password",
            "vul_name": "Tomcat默认弱口令",
            "enable": true
          }
        ],
        "scope_config": {
          "scope_id": "60f8c2b2e13e4b1e8c8b5678"
        }
      },
      "update_date": "2023-05-11"
    }
  }
}
```

**响应字段说明**：

| 字段名           | 类型    | 说明                  |
| ---------------- | ------- | --------------------- |
| data.data        | object  | 更新后的完整策略信息  |

### 4. 删除策略

**请求方法与地址**：
```
POST /api/policy/delete/
```

**请求体**：
```json
{
  "policy_id": ["60f8c2b2e13e4b1e8c8b4567", "60f8c2b2e13e4b1e8c8b4568"]
}
```

**参数说明**：

| 参数名    | 类型      | 是否必填 | 说明              |
| --------- | --------- | -------- | ----------------- |
| policy_id | string[]  | 是       | 要删除的策略ID列表 |

**响应示例**：
```json
{
  "code": 0,
  "msg": "Success",
  "data": {}
}
```

## 错误响应

### 通用错误码

| 错误码 | 描述                 | 说明                       |
| ------ | -------------------- | -------------------------- |
| 500    | Error                | 系统异常                   |
| 401    | NotLogin             | 用户未登录                 |
| 1100   | PolicyIDNotFound     | 策略不存在                 |
| 1103   | PolicyDataIsEmpty    | 策略数据为空               |
| 1104   | PortCustomInvalid    | 自定义端口格式无效         |
| 1105   | ExcludePortsInvalid  | 排除端口格式无效           |

### 错误响应字段说明

| 字段名      | 类型   | 说明                     |
| ----------- | ------ | ------------------------ |
| code        | number | 错误码                   |
| msg         | string | 错误类型描述             |
| data.error  | string | 详细错误信息（可选）     |
| data.policy_id | string | 相关策略ID（可选）     |

### 错误示例
策略不存在：
```json
{
  "code": 1100,
  "msg": "PolicyIDNotFound",
  "data": {}
}
```

自定义端口格式无效：
```json
{
  "code": 1104,
  "msg": "PortCustomInvalid",
  "data": {
    "port_custom": "无效的端口格式"
  }
}
```