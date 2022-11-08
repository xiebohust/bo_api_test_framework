import json

import allure


def allure_step(step_title, content):
    """

    :param step_title: 步骤或附件名称
    :param content: 附件内容
    :return:
    """
    with allure.step(step_title):
        allure.attach(json.dumps(content,ensure_ascii=False,indent=4),step_title,attachment_type=allure.attachment_type.TEXT)


