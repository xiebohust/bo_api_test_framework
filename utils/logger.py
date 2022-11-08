import logging
import os.path
import config
from utils import common



def get_logger(logger_name=None):
    """
    封装日志模块
    :param name: 日志名字
    :return: 日志对象
    """
    # 创建日志对象
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)

    # create log directory
    if not os.path.exists(config.log_path):
        os.makedirs(config.log_path)

    # set log file name
    all_log_name = os.path.join(config.log_path, common.current_time()+'all_log.log')
    error_log_name = os.path.join(config.log_path, common.current_time()+'error_log.log')

    # set file and stream handlers
    # print(f'handlers:{logger.handlers}')
    if not logger.handlers:

        # all log file
        fh = logging.FileHandler(all_log_name, encoding='utf-8')
        fh.setLevel(logging.INFO)

        # error log file
        eh = logging.FileHandler(error_log_name,encoding='utf-8')
        eh.setLevel(logging.ERROR)

        # console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)


        # set log file format
        fmt = logging.Formatter('%(asctime)s %(filename)s - %(levelname)s - %(lineno)s - %(message)s')
        fh.setFormatter(fmt)
        eh.setFormatter(fmt)
        ch.setFormatter(fmt)

        logger.handlers.extend([fh,eh,ch])
        # print(logger.handlers)

    return logger


# logger = get_logger()
if __name__ == '__main__':
    get_logger().info(123)
    get_logger().info(345)
    get_logger().critical(33)


