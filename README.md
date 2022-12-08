# bo_api_test_framework


这是一个接口自动化框架

初始版本
python3 + unittest + requests + HTMLTestRunner-rv + Excel + Yaml

进化版本
python3 + pytest + requests + allure + yaml

generate_case:生成的测试py文件目录
logs:日志
outputs：allure测试报告目录，包括json和html、css、js文件
request_utils: 封装请求
utils: 封装通用功能，如用例生成（case_handle.py）、数据库读取、yaml读取、excel读取、日志配置、通用函数
testcase: 测试py文件
testcase_file: 测试数据excel和yaml存放
config:全局变量配置
conftest:fixture固件配置，这里有一个自动执行的函数init_data，用来对全局变量进行初始化
pytest.ini:pytest的配置文件，可以配置pytest命令执行参数、mark标签等等
run_cases:启动文件
