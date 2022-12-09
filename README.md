## 接口自动化框架

## 版本
初始
python3 + unittest + requests + HTMLTestRunner-rv + Excel + Yaml

进化后版本
python3 + pytest + requests + allure + yaml

## 框架主要功能：
1. 数据驱动：可以兼容Excel、Yaml格式的测试用例，把用例需要的数据从url到预期结果都可以读取
2. 测试数据参数化：为了保证用例的稳定性，测试数据也不能写死，应该参数话，比如user:\${user}，通过把数据中\${}格式内容动态替换可以实现参数化
3. 前置后置sql：在测试用例中加入前置  setup_sql 和后置字段   teardown_sql，来实现每个用例执行的前置和后置操作，保证用例的独立性
4. allure生成测试报告


## 框架目录结构

**generate_case:**
生成的测试py文件目录，用例结构如下：
其中data函数是一个pytest固件，可以实现前置和后置操作，而且能传递测试数据

```python
import pytest
import allure
from request_utils.pre_request import RequestPreHandle
from request_utils.request_handle import RequestHandle
from request_utils.assert_result import assert_results

@pytest.fixture(params=[{'id': 2, 'case_id': 'case_02', 'feature': '功能', 'title': '标题', 'url': '/api/test', 'method': 'GET', 'headers': None, 'cookies': '', 'data_type': 'params', 'data': "{'plan': '${plan}'}", 'expect': "{'eq': {'$.code': 0}}"}])
def data(request):
    test_data = RequestPreHandle(request.param).to_request_data
    yield test_data
    RequestPreHandle(request.param).teardown_sql_handle()


class TestName:

    @pytest.mark.smoke
    def test_name(self, data):
        allure.dynamic.feature(data.get('feature'))
        allure.dynamic.title(data.get('title'))
        result = RequestHandle.send_req(data)
        expect = data.get('expect')
        assert_results(result,expect)
```

**logs:**
日志存放
**outputs：**
allure测试报告文件的存放目录，包括json和html、css、js文件

**request_utils:** 
 1. pre_request.py： 请求数据预处理，替换数据里的变量\${}。
 2. request_handle.py ：请求执行
 3. after_request.py：请求后结果的处理，主要从响应json结果中提取jsonpath表达式
 4. assert_result.py：对请求结果进行断言


**utils:** 
封装通用功能，如用例生成（case_handle.py）、数据库读取、yaml读取、excel读取、日志配置、通用函数

 1. case_handle.py：读取测试用例的excel或yaml文件，然后通过模版生成用例py文件放在目录generate_case里，用例模版如下：
```python
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
```

**testcase:** 
测试py文件
**testcase_file:** 
测试数据excel和yaml存放

**config:**
全局变量配置

**conftest:**
fixture固件配置文件，在这里放了一个全局的数据初始化固件init_data，在一轮测试开始前会自动执行一次

**pytest.ini:**
pytest的配置文件，可以配置pytest命令执行参数、mark标签等等

**run_cases:**
启动入口文件

