# coding: utf-8
# @Time : 9/8/21 9:45 AM


from shino.libs.mongo_ext import MongoExt

from shino.seed_generator.dynamic_url import DynamicUrl

from furl import furl

from urllib.parse import (urlencode, unquote_plus)

from functools import reduce

from shino.libs.mysql_ext import MysqlExt


class UrlGenerator:
    __mongo_conn = None

    def __init__(self, conf):

        self.log = conf["log"]

        self.__url_query_params = []

        self.dynamic_url = DynamicUrl(conf)

    def __dict_to_raw_url(self, info):
        return unquote_plus(urlencode(info))

    def __load_params_from_mysql(self, mysql_conf, query_rule):
        mysql_conn = MysqlExt(**mysql_conf)
        results = [_ for _ in mysql_conn.select_many(query_rule["sql"])]
        field_map = query_rule["map"]
        if not field_map:
            new_results = results
        else:
            new_results = []
            for per_result in results:
                for k, db_k in field_map.items():
                    per_result[k] = per_result.pop(db_k)
                new_results.append(per_result)
        return new_results

    def __load_params_from_mongo(self, mongo_conf, query_rule):
        self.__mongo_conn = MongoExt(
            dbhost=mongo_conf["host"],
            dbport=mongo_conf["port"],
            dbname=mongo_conf["db"],
            dbuser=mongo_conf["user"],
            dbpass=mongo_conf["password"],
            table=mongo_conf["table"],
        )

        self.log.info(f"post_from_filter|query={query_rule.get('query')}\t"
                      f"sort={query_rule.get('sort')}\t"
                      f"field={query_rule.get('field')}")

        results = []
        for per_query in self.__mongo_conn.traverse_batch(where=query_rule.get("query"),
                                                          sort=query_rule.get("sort"),
                                                          field=query_rule.get("field")
                                                          ):
            if "map" in query_rule:
                for key, db_key in query_rule["map"].items():
                    per_query[key] = per_query.pop(db_key)

            del per_query["_id"]
            results.append(per_query)
        return results

    def __assem_get_from(self, sch_info, middle_urls):
        if not sch_info.get_from:
            return middle_urls

        if sch_info.get_from == "mysql":
            db_get_infos = self.__load_params_from_mysql(sch_info.get_from_conf, sch_info.get_from_filter)
        elif sch_info.get_from == "mongo":
            db_get_infos = self.__load_params_from_mongo(sch_info.get_from_conf, sch_info.get_from_filter)
        else:
            db_get_infos = []

        new_mid_urls = list(map(lambda x: f"{furl(sch_info.seed_url).add(x).tostr()}", db_get_infos))

        return new_mid_urls

    def __assem_post_data(self, sch_info, middle_urls):
        if not sch_info.post_data:
            return middle_urls

        new_mid_urls = []
        post_data = unquote_plus(urlencode(sch_info.post_data))
        for per_url in middle_urls:
            url = f"{per_url}|post_data:{post_data}"
            new_mid_urls.append(url)
        return new_mid_urls

    def __parse_many(self, many_items):

        field_k_v = []
        for k, values in many_items.items():
            design = []
            for v in values:
                v_r = f"{k}={v}"
                design.append(v_r)
            field_k_v.append(design)

        def pack_result(a, b):
            result = []
            for per_a in a:
                for per_b in b:
                    c = f"{per_a}&{per_b}"
                    result.append(c)
            return result

        result = reduce(pack_result, field_k_v)

        return result

    def __assem_get_many(self, sch_info, middle_urls):
        if not sch_info.get_many:
            return middle_urls

        new_mid_urls = []
        for per_url in middle_urls:
            for per_get in self.__parse_many(sch_info.get_many):
                url = furl(per_url).add(per_get).tostr()
                new_mid_urls.append(url)
        return new_mid_urls

    def __assem_post_many(self, sch_info, middle_urls):
        if not sch_info.post_many:
            return middle_urls

        new_mid_urls = []
        for per_url in middle_urls:
            for per_post in self.__parse_many(sch_info.post_many):
                url = f"{per_url}|post_data:{per_post}" if "|post_data:" not in per_url else f"{per_url}&{per_post}"
                new_mid_urls.append(url)
        return new_mid_urls

    def __assem_post_from(self, sch_info, middle_urls):
        if not sch_info.post_from:
            return middle_urls

        if sch_info.post_from == "mysql":
            db_post_infos = self.__load_params_from_mysql(sch_info.post_from_conf, sch_info.post_from_filter)
        elif sch_info.post_from == "mongo":
            db_post_infos = self.__load_params_from_mongo(sch_info.post_from_conf, sch_info.post_from_filter)
        else:
            db_post_infos = []

        new_mid_urls = []

        for per_url in middle_urls:
            for per_post in db_post_infos:
                post_data = unquote_plus(urlencode(per_post))
                url = f"{per_url}|post_data:{post_data}" if "|post_data:" not in per_url else f"{per_url}&{post_data}"
                new_mid_urls.append(url)

        return new_mid_urls

    def __assme_dynamic_url(self, sch_info, middle_urls):
        sch_urls = self.dynamic_url.change_url(sch_info, middle_urls)
        return sch_urls

    def gen_url(self, sch_info):

        sch_urls = [sch_info.seed_url]

        for assem_url_method in [self.__assem_get_from, self.__assem_get_many,
                                 self.__assem_post_data, self.__assem_post_many,
                                 self.__assem_post_from, self.__assme_dynamic_url]:
            try:
                sch_urls = assem_url_method(sch_info, sch_urls)
            except Exception as e:
                self.log.error(f"execute「{assem_url_method}」error happened：")
                self.log.exception(e)
                return []

        return sch_urls
