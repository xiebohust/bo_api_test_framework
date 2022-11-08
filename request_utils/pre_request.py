import json
import re
from string import Template

from utils.db_handle import DBHandle
from utils.functions import *
import config
from utils import logger
from utils.allure_step import allure_step

logger = logger.get_logger(__file__)


# def pre_request_data_handle(api_data):
#     """
#     请求数据预处理，替换变量${}，并且把字符串转成dict或list
#     :param api_data: { 'url': '${GlobalVars.host}/api','headers': '{'auth':'${auth}'}'}
#     :return: api_data: { 'url': 'www.baidu.com/api','headers': '{'auth':'6hhh4343h'}'}
#     """
#     for k, v in api_data.items():
#
#         if k in ['headers','params','json', 'data'] and v is not None and '${' in v:
#             api_data[k] = build_params(v)
#         if k in ['extract', 'expect','headers','params','json', 'data']:
#             api_data[k] = str_to_python(api_data[k])  # yml文件已经load成python,excel数据需要eval一下
#
#     api_data['url'] = config.GlobalVars.host + api_data['url']
#     api_data['headers'] = api_data['headers'] if api_data.get('headers') else config.GlobalVars.headers


def build_params(content):
    """
    替换接口数据中的动态参数 ${} 和 函数 ${}
    :param content: {'headers': {'auth':'${authorization}'}}
    :return: 'headers': {'auth':'ab5663jd3455'}
    """
    if content is None:
        return None
    logger.info(f"开始进行字符串替换: 替换字符串为：{content}")
    content = Template(str(content)).safe_substitute(config.GlobalVars.__dict__)
    for func in re.findall('\\${(.*?)}', content):
        try:
            content = content.replace('${%s}' %func,str(eval(func)))
        except Exception as e:
            logger.error(e)
    logger.info(f"字符串替换完成: 替换字符串后为：{content}")
    return content


def str_to_python(content):
    """
    字符串转成python，将"[1,2,3]" 或者"{'k':'v'}" -> [1,2,3], {'k':'v'}
    :param content:
    :return:
    """
    if content is None:
        return None

    if isinstance(content, str) and len(content) > 0:
        return eval(content)
    return content


class RequestPreHandle:
    def __init__(self, request_data):
        self.request_data = request_data
        self.host = config.GlobalVars.host
        self.db_conn = None

    # 请求路径处理
    def url_handle(self):
        url = str(build_params(self.request_data.get("url", "")))
        logger.info("处理请求前url：{}".format(url))
        host = self.host
        if url.lower().startswith("http"):
            self.request_data["url"] = url
        else:
            if host.endswith("/") or url.startswith("/"):
                self.request_data["url"] = host + url
            else:
                self.request_data["url"] = host + "/" + url
        allure_step('请求url地址', self.request_data["url"])
        logger.info("处理请求后 url：{}".format(self.request_data["url"]))

    def header_handle(self):
        if self.request_data.get("headers", None):
            logger.info("处理请求前头： {}".format(self.request_data.get("headers", None)))
            self.request_data["headers"] = str_to_python(build_params(self.request_data.get("headers", None)))
            logger.info("处理请求前头： {}".format(self.request_data["headers"]))
        elif config.GlobalVars.headers:
            self.request_data["headers"] = config.GlobalVars.headers
        allure_step('请求headers', self.request_data.get("headers", None))

    def datatype_handle(self):
        if not self.request_data.get("data_type", None):
            self.request_data['data_type'] = 'params'
        allure_step('请求data_type', self.request_data.get("data_type", None))

    def data_handle(self):
        if self.request_data.get("data", None):
            logger.info("处理请求前Data： {}".format(self.request_data.get("data", None)))
            self.request_data["data"] = str_to_python(build_params(self.request_data.get("data", None)))
            logger.info("处理请求后Data： {}".format(self.request_data["data"]))
        allure_step('请求data', self.request_data.get("data", None))

    def file_handle(self):
        """
        格式：接口中文件参数的名称:"文件路径地址"/["文件地址1", "文件地址2"]
        """
        files = self.request_data.get("file", None)
        logger.info("处理请求前files： {}".format(files))

        if files is None:
            return

        if files != "" and files is not None:
            files = eval(files)
            for k, v in files.items():
                # 多文件上传
                if isinstance(v, list):
                    files = []
                    for path in v:
                        files.append((k, (open(path, 'rb'))))
                else:
                    # 单文件上传
                    files = {k: open(v, 'rb')}

        self.request_data["file"] = files
        logger.info("处理请求后files： {}".format(str(files)))
        allure_step('请求files', files)

    def extract_handle(self):
        if self.request_data.get("extract", None):
            logger.info("处理后置提取参数前： {}".format(self.request_data.get("extract", None)))
            self.request_data["extract"] = str_to_python(self.request_data.get("extract", None))
            logger.info("处理后置提取参数后： {}".format(self.request_data.get("extract", None)))
        allure_step('请求extract', self.request_data.get("extract", None))

    def expect_handle(self):
        if self.request_data.get("expect", None):
            logger.info("请求预期结果处理前： {}".format(self.request_data.get("expect", None)))
            self.request_data["expect"] = str_to_python(self.request_data.get("expect", None))
            logger.info("请求预期结果处理后： {}".format(self.request_data.get("expect", None)))
        allure_step('请求预期结果', self.request_data.get("expect", None))

    def db_name_handle(self):
        if self.request_data.get("db_name", None):
            logger.info("处理前db_name： {}".format(self.request_data.get("db_name", None)))
            self.request_data["db_name"] = build_params(self.request_data.get("db_name", None))
            self.db_conn = DBHandle(db=self.request_data.get('db_name'))
            logger.info("处理后db_name： {}".format(self.request_data.get("db_name", None)))
        allure_step('请求db_name', self.request_data.get("db_name", None))

    def setup_sql_handle(self):
        if self.request_data.get("setup_sql", None):
            logger.info("处理请求前 setup_sql： {}".format(self.request_data.get("setup_sql", None)))
            self.request_data["setup_sql"] = str_to_python(build_params(self.request_data.get("setup_sql", None)))
            logger.info("处理请求后 setup_sql： {}".format(self.request_data["setup_sql"]))
            self.execute_setup_sql()
        allure_step('请求 setup_sql', self.request_data.get("setup_sql", None))

    def execute_setup_sql(self):
        '''
        执行setup_sql,并保存结果至参数池
        :param db_connect: mysql数据库实例
        :param setup_sql: 前置sql
        :return:
        '''
        for sql in self.request_data.get('setup_sql'):
            result = self.db_conn.execute_sql(sql)
            logger.info("执行前置sql====>{}，影响条数:{}".format(sql, result))
            if sql.lower().startswith("select"):
                logger.info("执行前置sql====>{}，获得以下结果集:{}".format(sql, result))
                # 获取所有查询字段，并保存至公共参数池
                for key in result.keys():
                    setattr(config.GlobalVars, key, result[key])
                    logger.info("保存 {}=>{} 到全局变量池".format(key, result[key]))

    def teardown_sql_handle(self):
        if self.request_data.get("teardown_sql", None):
            logger.info("处理请求前 teardown_sql： {}".format(self.request_data.get("teardown_sql", None)))
            self.request_data["teardown_sql"] = str_to_python(build_params(self.request_data.get("teardown_sql", None)))
            logger.info("处理请求后 teardown_sql： {}".format(self.request_data["teardown_sql"]))
            self.db_conn = DBHandle(db=self.request_data.get('db_name'))
            self.execute_teardown_sql()
        allure_step('请求 teardown_sql', self.request_data.get("teardown_sql", None))

    def execute_teardown_sql(self):
        '''
        执行teardown_sql,并保存结果至参数池
        :param db_connect: mysql数据库实例
        :param teardown_sql: 后置sql
        :return:
        '''
        for sql in self.request_data.get('teardown_sql'):
            result = self.db_conn.execute_sql(sql)
            logger.info("执行后置sql====>{}，影响条数:{}".format(sql, result))
            if sql.lower().startswith("select"):
                logger.info("执行后置sql====>{}，获得以下结果集:{}".format(sql, result))
                # 获取所有查询字段，并保存至公共参数池
                for key in result.keys():
                    setattr(config.GlobalVars, key, result[key])
                    logger.info("保存 {}=>{} 到全局变量池".format(key, result[key]))

    @property
    def to_request_data(self):
        self.db_name_handle()
        self.setup_sql_handle()
        self.url_handle()
        self.header_handle()
        self.datatype_handle()
        self.data_handle()
        self.file_handle()
        self.expect_handle()
        self.extract_handle()
        # self.teardown_sql_handle()

        return self.request_data


if __name__ == '__main__':

    # api_data = {'case_id': 'case_01', 'description': '获取随访模版列表', 'url': '/gateway/doctor/followupGroup/templates', 'method': 'GET', 'headers': '{"name":"${name}"}'}
    #
    # api_data = {'title': '正确查询', 'url': '/gateway/doctor/indicator/plan/query', 'method': 'GET', 'headers': {'Authorization': '385bcc285c9346a2999e43bad1be4862'}, 'params': {'planNo': 'FOLLOW_UP_PLAN_1'}, 'json': None, 'expect': {'$.code': 0}, 'extract': {'age': '$.code'}}
    #
    # r = pre_request_data_handle(api_data)
    #
    # print(r)
    # print(api_data)
    # content = {'headers': {'auth':'${authorization}'}}
    # print(build_params(content))
    #
    # print(str_to_python("dfds"))
    dict = {'params':{'planNo': 'FOLLOW_UP_PLAN_1'}}

    dict = 'gezhitestmr'
    # print(str_to_python(dict))

    print(eval('dfsd'))



