import os
from enum import Enum

# 项目根目录
base_dir = os.path.dirname(os.path.abspath(__file__))


# 测试用例excel文件地址
casefile_path = os.path.join(base_dir, 'testcase_file', 'case.xlsx')

# 测试yaml文件地址
caseyaml_path = os.path.join(base_dir, 'testcase_file')

# 自动生成测试文件地址
generate_case_path = os.path.join(base_dir, 'generate_case')

# 测试文件地址
testcase_path = os.path.join(base_dir, 'testcase_file')


# 测试执行文件
case_run_dir = os.path.join(base_dir, 'testcase')

# 测试日志文件
log_path = os.path.join(base_dir, 'logs')
# error_log_path = os.path.join(base_dir,'error_logs')

# 测试报告地址
report_path = os.path.join(base_dir, 'outputs')

# mysql 数据库
DB_USER = ''
DB_PASSWORD = ''
DB_HOST = ''
DB_PORT = 3306
DB_NAME = ''



# redis
REDIS_HOST = ''
REDIS_PORT = 6379
REDIS_USER = 'xx:'
REDIS_PASSWORD = 'xx:xx'



class GlobalVars:
    # 测试域名
    host = 'https://'
    url_session = 'xx'
    # 默认请求头
    headers = {'Authorization': 'xx'}



# 全局变量配置
global_vars = {
    'host':'https:',

}


class Email:
    user = "1@qq.com"
    pwd = ""

class CaseType(Enum):
    EXCEL = 1
    YAML = 2
    ALL = 0


case_type = CaseType.ALL

if __name__ == '__main__':
    # print(report_path)
    # print(casefile_path)
    # print(log_path)
    print(GlobalVars.__dict__)
    # setattr(GlobalVars,'k','value')
    # print(GlobalVars.__dict__)
    # print(CaseType.EXCEL)
    # print(CaseType.EXCEL.value)
    print(__file__)

