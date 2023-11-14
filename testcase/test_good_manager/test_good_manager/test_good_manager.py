import pytest
from env.env_factory import ENV
from loguru import logger


def setup_module(module):
    # 模块级别的前置操作
    pass


def teardown_module(module):
    # 模块级别的后置操作
    print("清理。。。")


@pytest.fixture(scope='function', autouse=True)
def fix_add():
    # 部分方法前执行前后置方法
    pass
    yield
    pass


class TestGoodManager:
    # 类级别的前置操作
    @classmethod
    def setup_class(cls):
        # 新增模板数据
        cls.good = {
            "id": "",
            "merId": 0,
            "image": "https://image.dayouqiantu.cn/5ca081af6183f.jpg",
            "sliderImage": "https://image.dayouqiantu.cn/5ca04fa9c08ef.jpg",
            "imageArr": [
                "https://image.dayouqiantu.cn/5ca081af6183f.jpg"
            ],
            "sliderImageArr": [
                "https://image.dayouqiantu.cn/5ca04fa9c08ef.jpg"
            ],
            "storeName": "陕西西瓜",
            "storeInfo": "陕西大西瓜",
            "keyword": "甜甜甜甜甜甜",
            "barCode": "123123123123123",
            "cateId": 1,
            "storeCategory": {
                "id": 62
            },
            "price": 0,
            "vipPrice": 0,
            "otPrice": 0,
            "postage": 0,
            "unitName": "华信",
            "sort": 0,
            "sales": 0,
            "stock": "1",
            "isShow": 1,
            "isHot": 0,
            "isBenefit": 0,
            "isBest": 0,
            "isNew": 0,
            "description": "<p>陕西大西瓜额委屈委屈恶趣味驱蚊器我12312312312312</p>",
            "addTime": "",
            "isPostage": 0,
            "isDel": 0,
            "merUse": 0,
            "giveIntegral": 0,
            "cost": 0,
            "isSeckill": 0,
            "isBargain": 0,
            "isGood": 0,
            "ficti": 0,
            "browse": 0,
            "codePath": "",
            "soureLink": ""
        }
        # 开发环境请求路径
        cls.url = ENV.url

    def test_good_add(self, login_and_get_session):
        response_add = login_and_get_session.post(self.url + '/api/yxStoreProduct', json=self.good)
        # 一般不用状态码判断业务逻辑是否成功（根据实际情况而定，此项目，后端未封装统一msg，故看返回的新增商品信息（例如 返回的商品名称与新增时的商品名称一致即可）） assert response.status_code == 201
        assert 'id' in response_add.json()
        logger.info(f'添加商品成功,商品信息为:{response_add.json()}')
        # 删除脏数据
        logger.info('正在删除脏数据')
        login_and_get_session.delete(self.url + '/api/yxStoreProduct/' + str(response_add.json().get('id')))

    def test_good_update(self, login_and_get_session):
        # 新增
        response_add = login_and_get_session.post(self.url + '/api/yxStoreProduct', json=self.good).json()
        if 'id' in response_add:
            # 修改(接口无任何返回数据)
            response_add['storeName'] = '陕西西瓜用例修改'
            response_add['barCode'] = '594844654'
            login_and_get_session.put(self.url + '/api/yxStoreProduct/', json=response_add)
            # 查询
            params = {
                'isDel': 0,
                'storeName': response_add['storeName']
            }
            response_select = login_and_get_session.get(self.url + '/api/yxStoreProduct', data=params).json()
            for item in response_select['content']:
                if item['id'] == response_add['id']:
                    assert item['storeName'] == response_add['storeName'] and item['barCode'] == response_add['barCode']
                    logger.info(f'商品修改成功：修改后的商品信息为{item}')
                    # 删除脏数据
                    logger.info('正在删除脏数据')
                    login_and_get_session.delete(self.url + '/api/yxStoreProduct/' + str(response_add['id']))

    def test_good_find(self, login_and_get_session):
        # 新增
        response_add = login_and_get_session.post(self.url + '/api/yxStoreProduct', json=self.good)
        # 查询
        params = {
            "id": str(response_add.json()['id'])
        }
        response_select = login_and_get_session.get(self.url + '/api/yxStoreProduct', data=params).json()
        assert 'content' in response_select
        logger.info(f"查询成功，查询结果为：{response_select['content']}")

    def test_good_delete(self, login_and_get_session, fix_add):
        # 测试删除功能（先新增，后删除，最后查询是否删除）
        response_add = login_and_get_session.post(self.url + '/api/yxStoreProduct', json=self.good)
        if 'id' in response_add.json():
            # 执行删除（实际接口无返回结果，逻辑删除：字段is_del为1时删除）
            login_and_get_session.delete(self.url + '/api/yxStoreProduct/' + str(response_add.json().get('id')))
            # 查询是否删除 字段is_del是否为：1（接口不支持id查询，并且查询不出isDel=1的数据（默认查询isDel=0），反之利用此特性（实则为后端代码不完善），如果查询集合中没有之前添加的id说明删除成功）
            response = login_and_get_session.get(self.url + '/api/yxStoreProduct',
                                                 data={'storeName': self.good.get('storeName')})
            # logger.info(f'查询结果集合为：{response.json()}')
            id_list = [g['id'] for g in response.json()['content']]
            assert response_add.json().get('id') not in id_list
            logger.info('删除商品成功')


if __name__ == '__main__':
    pytest.main(['-vs'])
# -s: 表示输出调试信息，包括print打印的信息
# -v: 显示更详细的信息
# -vs：两个参数一起使用
# -n: 支持多线程或者分布式进行测试用例(需要安装pytest - xdist插件)
# 如：pytest.main(['-vs', "./testcase/test_login.py", "-n=2"])
# 代表两个线程跑用例
# --reruns
# NUM: 失败重跑次数
