import ddddocr
import requests
import base64
from PIL import Image
import io
import pytest
import os
import sys
# 获取当前脚本所在目录
current_dir = os.path.dirname(__file__)

# 添加当前目录到 sys.path
sys.path.append(current_dir)

# 添加 env 包的路径到 sys.path
sys.path.append(os.path.abspath(os.path.join(current_dir, "env")))
print(sys.path)

from env.env_factory import ENV
from loguru import logger


@pytest.fixture(scope="session", autouse=True)
def login_and_get_session():
    # 定义登陆重试次数
    num = 0
    while num <= 1:
        try:
            logger.info('开始获取token~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            username = ENV.username
            password = ENV.password
            url = ENV.url
            response = requests.get(url + '/auth/code', timeout=3)
            data = response.json()
            # 获取 img 值
            base64_data = data['img']
            uuid = data['uuid']
            # 移除前缀 "data:image/png;base64," 并解码 Base64 数据
            base64_data = base64_data.replace("data:image/png;base64,", "")
            image_data = base64.b64decode(base64_data)
            # 将数据转换为图像
            image = Image.open(io.BytesIO(image_data))
            ocr = ddddocr.DdddOcr()
            res = ocr.classification(image)
            logger.info('识别出的验证码为：' + res)
            nummer = 0
            if res[1] == '-':
                nummer = int(res[0]) - int(res[2])
            elif res[1] == 'x':
                nummer = int(res[0]) * int(res[2])
            elif res[1] == '÷':
                nummer = int(res[0]) / int(res[2])
            elif res[1] == 'e':
                nummer = int(res[0]) - int(res[2])
            elif res[1] == '=':
                nummer = int(res[0]) - int(res[2])
            elif res[1] == '+':
                nummer = int(res[0]) + int(res[2])
            elif res[1] == 't':
                nummer = int(res[0]) + int(res[2])
            elif res[1] == '4':
                nummer = int(res[0]) + int(res[2])
            elif res[1] == 's':
                nummer = int(res[0]) + int(res[2])
            logger.info(f'验证码计算结果为：{nummer}')
            # 打开图像
            # image.show()
            data = {
                'code': str(nummer),
                'username': username,
                'password': password,
                'uuid': uuid
            }
            logger.info(f'请求参数为:{data}')
            # 发送POST请求
            response = requests.post(url + '/auth/login', json=data, timeout=3)
            # 检查响应
            if response.status_code == 200:
                logger.info(f"登陆成功，状态码：{response.status_code}")
                logger.info(f"响应token:{response.json()['token']}")
                token = response.json().get('token')
                # 创建一个 Session 对象并设置通用的 headers
                session = requests.Session()
                session.headers.update({'Authorization': token})
                return session
            else:
                logger.info(f"登陆失败，状态码: {response.status_code}")
                logger.info('继续获取token')
        except Exception as E:
            logger.error(f"登陆失败:{E}")
        finally:
            num += 1
