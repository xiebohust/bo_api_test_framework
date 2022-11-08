import re
from requests import Response
from jsonpath import jsonpath
from utils import logger

from config import GlobalVars
from utils.allure_step import allure_step

logger = logger.get_logger(__file__)


def after_request_data_handle(response: Response, expr:dict):
    """
    请求后的处理：根据extract字段的设置，从响应体中提取需要给其他接口提供关联的参数，并存储在全局变量global_vars里
    :param response:
    :param expr: 比如 id:$.data.id
    :return:
    """
    logger.info(f'开始提取响应结果json表达式{expr}')
    if expr is None:
        return GlobalVars

    if response_type(response) == 'json':
        res = response.json()
        for k, v in expr.items():
            # config.global_vars[k] = json_extract(res,v)
            setattr(GlobalVars,k,json_extract(res,v))
    else:
        res = response.text
        for k, v in expr.items():
            # config.global_vars[k] = re_extract(res,v)
            setattr(GlobalVars,k,re_extract(res,v))

    logger.info(f'新增全局变量{k}:{getattr(GlobalVars,k)}')
    allure_step('请求后置提取参数结果', {k:getattr(GlobalVars,k)})
    return GlobalVars


# def assert_result(response: Response, expect: dict):
#
#     for k, v in expect.items():
#         expected = v
#         actual = jsonpath(response.json(), k)[0]
#
#         dif = json_tools.diff(expected, actual)
#         logger.info(f'断言结果：{dif}')
#         assert dif == []


def json_extract(obj, expr):
    """
    从响应json结果中提取jsonpath表达式
    :param obj: dict类型数据
    :param expr: jsonpath表达式，如$.message 提取一级字典message
    :return:
    """
    try:
        result = jsonpath(obj, expr)[0]
        logger.info(f'从表达式{expr}提取到参数值{result}')
    except Exception as e:
        result = None
        logger.error(f'从表达式{expr}没有提取到参数值')
    return result

def re_extract(obj, expr):
    """
    从响应结果中提取正则表达式结果
    :param obj: 字符串
    :param expr: 正则表达式
    :return:
    """
    try:
        result = re.findall(obj, expr)[0]
        logger.info(f'从正则表达式{expr}提取到参数值{result}')
    except Exception as e:
        result = None
        logger.error(f'从字符串{obj}未提取到正则表达式{expr}')
    return result


def response_type(response:Response):
    """
    判断请求响应结果类型是json还是字符串
    :param response:
    :return:
    """
    try:
        response.json()
        return 'json'
    except:
        return 'str'

if __name__ == '__main__':
    pass
