import pytest
import allure

from request_utils.pre_request import RequestPreHandle
from utils import case_handle
from request_utils.request_handle import RequestHandle
from request_utils.assert_result import assert_results

api_data = case_handle.get_case_data()


@pytest.fixture(params=api_data)
def data(request):
    test_data = RequestPreHandle(request.param).to_request_data
    yield test_data
    RequestPreHandle(request.param).teardown_sql_handle()


class TestYamlCase:

    @pytest.mark.smoke
    def test_api(self, data):
        allure.dynamic.feature(data.get('feature'))
        allure.dynamic.title(data.get('title'))
        result = RequestHandle.send_req(data)
        expect = data.get('expect')
        assert_results(result,expect)


if __name__ == '__main__':
    pytest.main(['-svv', '--reruns=2','test_run_yaml.py'])


