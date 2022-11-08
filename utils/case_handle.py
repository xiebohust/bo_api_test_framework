import os
from string import Template

import config
from utils.yaml_handle import YamlHandle
from utils.excel_handle import ExcelHandle


def get_case_data():
    cases = []
    files = os.listdir(config.testcase_path)
    print(f'测试文件列表{files}')
    for file in files:
        file_path = os.path.join(config.testcase_path,file)
        file_extension = os.path.splitext(file)[-1]
        if file_extension in ['.xlsx','.xls']:
            case_data = ExcelHandle(file_path).get_data()
        elif file_extension in ['.yaml','.yml']:
            case_data = YamlHandle(file_path).read_yaml()
        else:
            continue
        cases.extend(case_data)
        name = 'test_' + os.path.splitext(file)[0]
        class_name = 'Test_' + os.path.splitext(file)[0]
        generate_case_file(name=name, case_data=case_data, class_name=class_name)

    for item in cases:
        print(f'用例{item}')

    return cases


case_template = """
import pytest
import allure
from request_utils.pre_request import RequestPreHandle
from request_utils.request_handle import RequestHandle
from request_utils.assert_result import assert_results

@pytest.fixture(params=${case_data})
def data(request):
    test_data = RequestPreHandle(request.param).to_request_data
    yield test_data
    RequestPreHandle(request.param).teardown_sql_handle()


class ${class_name}:

    @pytest.mark.smoke
    def ${case_title}(self, data):
        allure.dynamic.feature(data.get('feature'))
        allure.dynamic.title(data.get('title'))
        result = RequestHandle.send_req(data)
        expect = data.get('expect')
        assert_results(result,expect)

"""


def generate_case_file(name, case_data, class_name):
    """"""
    if not os.path.exists(config.generate_case_path):
        os.makedirs(config.generate_case_path)
    my_case = Template(case_template).safe_substitute({"case_data": case_data,
                                                       "case_title": name,
                                                       "class_name": class_name})
    with open(os.path.join(config.generate_case_path, name + '.py'), "w", encoding="utf-8") as fp:
        fp.write(my_case)


if __name__ == '__main__':
    get_case_data()
