# 项目概要设计

## 目录
* [数据库表](#数据库表)
* [表权限](#表权限)

## 数据库表

### 管理员（administrator）

| 字段名       | 字段类型      | 中文    | 说明            |
| :-----------| :----------- | :----- | :-------------- |
| id          | int(11)      | 用户id  | 自增主键 |
| name        | varchar(100) | 用户名  | 用于登陆，只允许唯一管理员admin |
| password    | text         | 密码    | 加密存储 |

### 国家（country）

| 字段名    | 字段类型      | 中文    | 说明    |
| :------- | :------------| :----- | :------ |
| id       | int(11)      | 国家id  | 自增主键 |
| name     | varchar(100) | 国家名称 ||

### 职位（position）

| 字段名    | 字段类型      | 中文    | 说明    |
| :------- | :----------- | :----- | :------ |
| id       | int(11)      | 职位id  | 自增主键 |
| name     | varchar(100) | 职位名称 ||

### 用户（user）

| 字段名       | 字段类型      | 中文    | 说明            |
| :-----------| :----------- | :----- | :-------------- |
| id          | int(11)      | 用户id  | 自增主键 |
| name        | varchar(100) | 用户名  | 用于用户登陆，UNIQUE限制保证系统唯一 |
| password    | text         | 密码    | 加密存储 |

### 用户信息（user_info）

| 字段名                          | 字段类型       | 中文         | 说明            |
| :----------------------------- | :------------ | :----------- | :------------- |
| id                             | int(11)       | 用户信息id    | 自增主键 |
| name                           |  varchar(100) | 用户名        | 外键 user.name |
| first_name                     | varchar(50)   | 名            ||
| last_name                      | varchar(50)   | 姓            ||
| position                       | varchar(100)  | 当前职位       ||
| company                        | varchar(100)  | 当前就职公司    ||
| nationality                    | varchar(100)  | 国籍           ||
| tobe_contacted                 | tinyint(1)    | 是否愿意被联系  ||
| skills_have                    | text          | 拥有的技能     ||
| skills_learned                 | text          | 学习到的技能  ||
| skills_recommend               | text          | 推荐的技能 ||
| skills_roles_in_company        | text          | 工作中需要沟通的角色 ||
| skills_tasks_auto              | text          | 自主完成的任务 ||
| skills_tasks_collab            | text          | 协作完成的任务 ||
| cc_competitiveness             | text          |||
| cc_desc_by_colleagues          | text          |||
| cc_working_approach            | text          |||
| cc_relationship_with_colleague | text          |||
| cc_relationship_with_mgr       | text          |||


## 表权限

### 国家（country）

| 用户     | 增 | 删 | 改 | 查 |
| :------ | :--- | :--- | :--- | :--- |
| admin   | Y | Y | Y | Y |
| 普通用户 | N | N | N | Y |
| 游客    | N | N | N | Y |

### 职位（position）

| 用户     | 增 | 删 | 改 | 查 |
| :------ | :--- | :--- | :--- | :--- |
| admin   | Y | Y | Y | Y |
| 普通用户 | N | N | N | Y |
| 游客    | N | N | N | Y |

### 用户（user）

| 用户     | 增 | 删 | 改 | 查 |
| :------ | :--- | :--- | :--- | :--- |
| admin   | Y | Y | Y | Y |
| 普通用户 | N | N | N | N |
| 游客    | N | N | N | N |

### 用户信息（user_info）

| 用户     | 增 | 删 | 改 | 查 |
| :------ | :--- | :--- | :--- | :--- |
| admin   | N | N | N | Y |
| 普通用户 | Y | Y | Y | Y |
| 游客    | N | N | N | Y |

> 用户信息（user_info）表中普通用户只能增、删、改自己的信息，而所有用户都有查看权限。
