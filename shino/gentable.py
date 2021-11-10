# coding: utf-8
# @Time : 10/8/21 11:25 AM
import os
import sys
import traceback

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(script_dir))

from conf import PropertiesCenter, GlobalSetting

import argparse

import pymysql

parser = argparse.ArgumentParser()

parser.add_argument("--env",
                    choices=["debug", "local", "dev", "prod", "local_to_dev", "local_to_prod"],
                    help="set env[debug、local、dev、prod、local_to_dev、local_to_prod]"
                    )

args = parser.parse_args()

if not args.env:
    raise Exception(f"u must set env args for config")

GlobalSetting.env(args.env)

from shino.libs.log_ext import LogExt

from shino.libs.mysql_ext import MysqlExt

log = LogExt("gentable.log").get_logger

# create db if not exists
cnx = pymysql.connect(host=PropertiesCenter.get_db('mysql.host'),
                      port=PropertiesCenter.get_db('mysql.port'),
                      user=PropertiesCenter.get_db('mysql.user'),
                      password=PropertiesCenter.get_db('mysql.password'))
try:
    cursor = cnx.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {PropertiesCenter.get_db('mysql.db')}")
except Exception as e:
    log.error(f"⚠️ Create mysql db failed:")
    for e_info in traceback.format_exception(*sys.exc_info()):
        for _ in e_info[:-1].split("\n"):
            log.error(_)
finally:
    cnx.close()

mysql = MysqlExt(**PropertiesCenter.get_db('mysql'))

# 主题表建表语句
create_topic_sql = """
create table if not exists _topic
(
    _id          int auto_increment
        primary key,
    _create_time timestamp default CURRENT_TIMESTAMP null,
    _update_time timestamp default CURRENT_TIMESTAMP null on update CURRENT_TIMESTAMP,
    _is_delete   tinyint   default 0                 null,
    name         varchar(100)                        not null comment '请求主题',
    `desc`       varchar(500)                        null comment '描述信息',
    `table`      varchar(100)                        not null comment '存储表名',
    `schema`     json                                null comment '主题表结构信息'
)
    collate = utf8mb4_unicode_ci;
"""

# 解析表（详情页）建表语句
create_parse_detail_sql = """
create table if not exists _parse_detail
(
    _id           int auto_increment
        primary key,
    _create_time  timestamp default CURRENT_TIMESTAMP null,
    _update_time  timestamp default CURRENT_TIMESTAMP null on update CURRENT_TIMESTAMP,
    _is_delete    tinyint   default 0                 null,
    `desc`        varchar(256)                        not null comment '描述',
    topic_id      int                                 not null,
    data_rule     json                                null,
    url_rule      json                                null,
    api           varchar(1024)                       not null,
    list_parse_id int                                 null,
    constraint _parse_detail__topic__id_fk
        foreign key (topic_id) references _topic (_id)
)
    collate = utf8mb4_unicode_ci;

"""

# 解析表（列表页）建表语句
create_parse_list_sql = """
create table if not exists _parse_list
(
    _id                  int auto_increment
        primary key,
    _create_time         timestamp default CURRENT_TIMESTAMP not null,
    _update_time         timestamp default CURRENT_TIMESTAMP not null on update CURRENT_TIMESTAMP,
    _is_delete           tinyint   default 0                 null,
    `desc`               varchar(100)                        not null comment '描述',
    start_page           int       default 1                 null comment '初始页码',
    page_size            int                                 not null comment '每页数量',
    max_page             int       default -1                null comment '爬取最大页数',
    page_field           varchar(128)                        not null comment 'page字段名',
    total_cnt_match_rule json                                not null comment '总数据量提取规则',
    index                idx_create_time (_create_time),
    index                idx_update_time (_update_time)
)
"""

# 请求依赖表建表语句
create_request_depend_sql = """
create table if not exists _request_depend
(
    _id          int auto_increment
        primary key,
    _create_time timestamp default CURRENT_TIMESTAMP null,
    _update_time timestamp default CURRENT_TIMESTAMP null on update CURRENT_TIMESTAMP,
    _is_delete   tinyint   default 0                 null,
    host         varchar(300)                        not null,
    headers_ext  json                                null comment '请求头扩充字段',
    use_proxy    tinyint   default 0                 not null
)
    collate = utf8mb4_unicode_ci;
"""

# 种子调度表建表语句
create_seed_sch_sql = """
create table if not exists _seed_sch
(
    _id              int auto_increment
        primary key,
    _create_time     timestamp   default CURRENT_TIMESTAMP null,
    _update_time     timestamp   default CURRENT_TIMESTAMP null on update CURRENT_TIMESTAMP,
    _is_delete       tinyint     default 0                 null,
    name             varchar(100)                          not null comment '调度维度名称',
    api              varchar(1024)                         not null comment '调度接口',
    seed_url         varchar(1024)                         not null comment '种子url',
    method           varchar(20) default 'get'             null comment '请求方法',
    post_data        json                                  null comment 'post_data 数据',
    get_from         varchar(20)                           null comment 'get_data from 外部数据库',
    get_from_conf    json                                  null comment 'get_data from 外部数据库连接信息',
    get_from_filter  json                                  null comment 'get_data from 外部数据库查询信息',
    post_from        varchar(20)                           null comment 'post_data from 外部数据库',
    post_from_conf   json                                  null comment 'post_data from 外部数据库连接信息',
    post_from_filter json                                  null comment 'post_data from 外部数据库查询信息',
    priority         int                                   not null comment '该接口优先级(数字大的优先级更高)',
    `interval`       int                                   null comment '接口请求间隔时长(单位：s)',
    appoint_crontab  varchar(100)                          null comment '定时调度任务语法',
    switch           varchar(10) default 'on'              not null comment '是否开启调度, on-开启, off-关闭',
    is_once          tinyint     default 0                 not null comment '是否属于一次性任务',
    get_many         json                                  null comment 'get 某些参数存在多个值',
    post_many        json                                  null comment 'post 某些参数存在多个值'
);
"""

# 服务监控表建表语句
create_service_monitor_sql = """
create table if not exists _service_monitor
(
    _create_time timestamp default CURRENT_TIMESTAMP not null,
    _update_time timestamp default CURRENT_TIMESTAMP not null on update CURRENT_TIMESTAMP,
    _is_delete   tinyint   default 0                 null,
    count        int       default 0                 not null comment '任务数量',
    status       varchar(32)                         not null comment '任务状态',
    service      varchar(32)                         not null comment '任务所属微服务',
    batch_no     varchar(64)                         not null comment '批次号',
    batch_time   varchar(16)                         not null comment '批次任务时间',
    api          varchar(1024)                       not null comment '批次任务关联的 api',
    index        idx_create_time (_create_time),
    index        idx_update_time (_update_time),
    primary key (batch_no, service, status)
);
"""

try:
    mysql.execute(create_topic_sql)
    mysql.execute(create_parse_detail_sql)
    mysql.execute(create_parse_list_sql)
    mysql.execute(create_request_depend_sql)
    mysql.execute(create_seed_sch_sql)
    mysql.execute(create_service_monitor_sql)
except Exception:
    log.error("⚠️ gen table failed(Unknown Error):")
    for e_info in traceback.format_exception(*sys.exc_info()):
        for _ in e_info[:-1].split("\n"):
            log.error(_)
else:
    log.success('table create success')
