import unittest

import json_tools
from ddt import ddt,data,unpack
from request_utils import after_request, assert_result
import config
from utils.logger import get_logger
from request_utils import request_handle
from utils.excel_handle import ExcelHandle

logger = get_logger(__file__)


@ddt
class TestRun(unittest.TestCase):
    test_data = ExcelHandle(config.casefile_path).data

    @data(*test_data)
    @unpack
    def test_api(self, **apidata):
        r = request_handle.RequestHandle.send_req(apidata)
        expect = apidata['expect']
        try:
            assert_result.assert_results(r,expect)
            logger.info(f'用例: {apidata.get("case_id")}, 描述: {apidata.get("description")}, 用例执行的结果:success')
        except AssertionError as e:
            logger.error(f'异常：{e}')
            raise AssertionError(f'用例: {apidata.get("case_id")}, 描述: {apidata.get("description")}, 用例执行的结果:fail')




if __name__ == '__main__':
    unittest.main()