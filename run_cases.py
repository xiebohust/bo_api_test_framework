import os
import shutil
import pytest
import config
# from package import HTMLTestRunner
from HTMLTestRunner import HTMLTestRunner
from utils import common, email_handle, case_handle


def run_cases():

    #  清空历史报告和日志
    # for f in os.listdir(config.report_path):
    #     os.remove(os.path.join(config.report_path,f))
    # for f in os.listdir(config.log_path):
    #     os.remove(os.path.join(config.log_path,f))

    if os.path.exists(config.log_path):
        shutil.rmtree(config.log_path)

    if os.path.exists(config.report_path):
        shutil.rmtree(config.report_path)

    # 删除生成的用例
    if os.path.exists(config.generate_case_path):
        shutil.rmtree(config.generate_case_path)

    # 生成用例py文件
    case_handle.get_case_data()

    # discover = unittest.defaultTestLoader.discover(config.case_run_dir, '*excel.py')
    # runner = HTMLTestRunner(log=True, output='report', verbosity=2, title='接口自动化测试报告',
    #                         description='接口自动化测试报告', report_name='report', open_in_browser=True,
    #                         tested_by='b', add_traceback=True)
    # runner.run(discover)
    # print(runner.html_report_file_name)
    # email_handle.send_email(runner.html_report_file_name)

    # testfile = os.path.join(config.case_run_dir,'test_run_yaml.py')
    testfile = config.generate_case_path

    pytest.main([testfile,'-sv','--reruns=2','-m smoke','--alluredir=outputs/report','--clean-alluredir'])
    os.system('allure generate outputs/report -o outputs/html --clean')
    os.system('allure serve outputs/report')


if __name__ == '__main__':
    run_cases()