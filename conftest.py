import pytest
import config
from utils.get_session import get_session


@pytest.fixture(scope='session', autouse=True)
def init_data():
     """
     初始化，获取session
     :return:
     """
     config.GlobalVars.headers = {'Authorization': get_session()}
     print(f'session:{config.GlobalVars.headers}')