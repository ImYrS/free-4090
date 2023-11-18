from typing import Optional
from hashlib import md5

from configobj import ConfigObj
import requests


def login(user: str, pwd: str) -> Optional[str]:
    """
    登录

    :param user: 用户名
    :param pwd: 经过 md5 加密的密码
    :return: 登陆成功返回 jwt, 否则返回 None
    """
    r = requests.post(
        'https://api.houdeyun.cn/userapi/api/v3/password/login',
        json={
            'username': user,
            'password': pwd,
        },
    )

    if r.status_code == 200:
        return r.json()['jweToken']

    raise Exception(r.text)


def get_gifts() -> list:
    """
    获取优惠券列表

    :return: 优惠券列表
    """
    params = {
        'sortBy': 'd,createAt',
    }
    r = requests.get('https://api.houdeyun.cn/order/api/v2.1/gift', **auth, params=params)
    return r.json()['items']


def get_new_gift() -> bool:
    """领取新优惠券"""
    r = requests.post('https://api.houdeyun.cn/order/api/v2.1/gift/renew', **auth, json={})
    if r.status_code == 200:
        return True
    else:
        raise Exception(r.text)


def reward_gift(gift_id: int) -> bool:
    """
    激活优惠券

    :param gift_id: 优惠券 ID
    :return: 是否激活成功 (对于已经兑换过的优惠券, 依然返回 True)
    """
    r = requests.post(f'https://api.houdeyun.cn/order/api/v2.1/gift/effect/{gift_id}', **auth, json={})
    return r.status_code == 200


def able_to_get_new_gift() -> bool:
    """
    是否可以领取新优惠券

    :return: 是否可以领取新优惠券
    """
    try:
        gifts = get_gifts()
        gift = gifts[0]

        if gift['total'] != gift['remain']:
            return True

        next_gift = gifts[1]
        remain = next_gift['remain']
        remain_hour = int(remain // 3)
        print(f'预计约 {remain_hour} 小时后可领取新优惠券')
        return False
    except IndexError:
        return True
    except KeyError:
        return False


if __name__ == '__main__':
    config = ConfigObj('config.ini', encoding='utf-8')
    username = config['username']
    password = config['password']
    used_md5 = config.as_bool('used_md5')
    jwt = config.get('jwt')

    if not used_md5:
        password = md5(password.encode()).hexdigest()

    jwt = jwt if jwt else login(username, password)
    cookies = {'jweToken': jwt}
    headers = {'Jwetoken': jwt}
    auth = {'headers': headers, 'cookies': cookies}

    if not able_to_get_new_gift():
        print('当前状态仍无法领取新优惠券, 稍后再试')
        exit(0)

    get_new_gift()
    gifts = get_gifts()
    gift = gifts[0]

    if reward_gift(gift['id']):
        print(f'成功激活优惠券: {gift["id"]}')
    else:
        print(f'激活优惠券失败')
