import unittest

import json_tools
from jsonpath import jsonpath
from requests import Response

from request_utils.after_request import response_type,json_extract,re_extract
from utils import logger

logger = logger.get_logger(__file__)

def assert_results(response,expect):
    """ 断言方法
    :param response: 实际响应对象
    :param expect: 预期响应内容，从excel中或者yaml读取,dict
    return None
    """
    if expect is None:
        logger.info("当前用例无预期结果")
        return
    if isinstance(expect,str):
        expect = eval(expect)
    # expect结构   expect:{ eq: {$.code: '0',$.message: success},in: {$.code: '0',$.message: success} }
    index = 0
    for k,v in expect.items():
        for k1,v1 in v.items():
            if k1 == 'status_code':
                actual = response.status_code
            else:
                if response_type(response) == 'json':
                    actual = json_extract(response.json(),k1)
                else:
                    actual = re_extract(response.text,k1)
            index += 1
            logger.info(f'第{index}个断言数据,实际结果:{actual} | 预期结果:{v1} 断言方式：{k}')
            try:
                if k == 'eq':
                    assert actual == v1
                elif k == 'in':
                    assert actual in v1
                elif k == 'gt':
                    assert actual > v1
                elif k == 'lt':
                    assert actual < v1
                elif k == 'not':
                    assert actual != v1
                elif k == 'notin':
                    assert actual not in v1
                else:
                    logger.error(f"断言关键字: {k} 错误！")
            except Exception as e:
                raise AssertionError(f'第{index}个断言失败，断言方式：{k}， 实际结果:{actual}， 预期结果: {v1}')





# def assert_results(response, expect):
#     for k, v in expect.items():
#         expect = v
#         actual = jsonpath(response.json(), k)[0]
#         logger.info(f'expect:{expect},actual:{actual}')
#         assert expect == actual


class AssertResult(unittest.TestCase):

    def assert_result(self,response, expect):
        for k, v in expect.items():
            expected = v
            actual = jsonpath(response.json(), k)[0]
            dif = json_tools.diff(expected, actual)
            logger.info(f'断言结果：{dif}')
            self.assertEqual(dif,[])



