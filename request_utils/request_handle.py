import requests

from request_utils import after_request
from request_utils.pre_request import RequestPreHandle
from utils import logger
from utils.allure_step import allure_step

logger = logger.get_logger(__file__)


class RequestHandle:
    session = None

    @classmethod
    def get_session(cls):
        if cls.session is None:
            cls.session = requests.session()
        return cls.session

    @classmethod
    def send_req(cls, api_data:dict):
        logger.info("开始执行用例： {}".format(api_data.get("title")))

        # 请求数据预处理
        # api_data = RequestPreHandle(api_data).to_request_data

        try:
            method = api_data.get('method')
            url = api_data.get('url')
            headers = api_data.get('headers')
            cookies = api_data.get('cookies')
            data_type = api_data.get('data_type')
            data = api_data.get('data')
            files = api_data.get('files')
            extract = api_data.get('extract')

            logger.info(f'请求参数：{api_data}')
            r = cls.send_api(method=method, url=url, data_type=data_type, headers=headers, cookies=cookies, data=data, files=files)
            logger.info(f'请求结果：{r.text}')
            allure_step('请求结果', r.text)

            # 请求后的参数提取处理
            if extract:
                after_request.after_request_data_handle(r,extract)

            return r
        except Exception as e:
            print(e)
            logger.error('异常：', e)


    @classmethod
    def send_api(cls, url, method, data_type, headers=None, data=None, files=None, cookies=None):
        """
        :param method: 请求方法
        :param url: 请求url
        :param data_type: 入参关键字， params(查询参数类型，明文传输，一般在url?参数名=参数值), data(一般用于form表单类型参数)
        json(一般用于json类型请求参数)
        :param data: 参数数据，默认等于None
        :param files: 文件对象
        :param headers: 请求头
        :return: 返回res对象
        """
        session = cls.get_session()
        data_type = data_type.lower()
        if data_type == 'params':
            res = session.request(method=method, url=url, params=data, headers=headers, cookies=cookies)
        elif data_type == 'data':
            res = session.request(method=method, url=url, data=data, files=files, headers=headers, cookies=cookies)
        elif data_type == 'json':
            res = session.request(method=method, url=url, json=data, files=files, headers=headers, cookies=cookies)
        else:
            raise ValueError('data_type可选关键字为params, json, data')
        return res


if __name__ == '__main__':
    logger.info(f'hahahaa')