#!/usr/bin/python3
# -*- coding: utf-8 -*-
import subprocess
import json
import asyncio
import requests
from bs4 import BeautifulSoup
# import re


async def get_ip_by_torapi(host, port):
    """
    Print proxy ip through tor api
    :param host: string - proxy host
    :param port: integer - proxy port
    :return: proxy ip
    """
    pipe = subprocess.PIPE
    cmd = 'curl --proxy socks5h://{}:{} https://check.torproject.org/api/ip'\
        .format(host, port)
    res_ip = None
    while True:
        p = subprocess.Popen(cmd, shell=True, stdout=pipe, stderr=pipe)
        res = p.stdout.read().decode('utf-8')
        try:
            d = json.loads(res)
            res_ip = d.get('IP')
            print('{0}:{1} => {2}'.format(host, port, res_ip))
        except json.decoder.JSONDecodeError as err:
            print(repr(err))
            return res_ip
        await asyncio.sleep(10)


async def get_ip_by_bs(host, port):
    """
    Print proxy ip through beautiful soup usage
    :param host: string - proxy host
    :param port: integer - proxy port
    :return: proxy ip
    """
    url = 'http://sitespy.ru/my-ip'
    proxies = {'http': 'socks5://{host}:{port}'.format(host=host, port=port),
               'https': 'socks5://{host}:{port}'.format(host=host, port=port)}
    res_ip = None
    while True:
        try:
            resp = requests.get(url, proxies=proxies)
            html = resp.text
            soup = BeautifulSoup(html, "html.parser")
            res_txt = soup.find('span', class_='ip')
            res_ip = res_txt.text if res_ip is not None else res_ip
            print('{0}:{1} => {2}'.format(host, port, res_ip))
        except requests.exceptions.ConnectionError as err:
            print('{0}:{1} => {2}'.format(host, port, repr(err)))
            return res_ip
        await asyncio.sleep(10)


async def get_ip_by_re(host, port, reg_exp):
    """
    Print proxy ip through regular expressions
    :param host: string - proxy host
    :param port: integer - proxy port
    :param reg_exp: re.compile() object - compiled reg. expression
    :return: proxy ip
    """
    url = 'http://www.whatip.org/'
    proxies = {'http': 'socks5://{host}:{port}'.format(host=host, port=port),
               'https': 'socks5://{host}:{port}'.format(host=host, port=port)}
    res_ip = None
    while True:
        try:
            resp = requests.get(url, proxies=proxies)
            html = resp.text
            res_arr = reg_exp.findall(html)
            if len(res_arr):
                res_ip = res_arr[0]
            print('{0}:{1} => {2}'.format(host, port, res_ip))
        except requests.exceptions.ConnectionError as err:
            print('{0}:{1} => {2}'.format(host, port, repr(err)))
            return res_ip
        await asyncio.sleep(10)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    localhost = '127.0.0.1'
    #  1) - through tor api
    fut = asyncio.gather(*[get_ip_by_torapi(localhost, port) for port in range(10025, 10030)])
    #  2) - through beautiful soup
    # fut = asyncio.gather(*[get_ip_by_bs(localhost, port, r_exp) for port in range(10025, 10030)])
    #  3) - through regular expression
    # r_exp = re.compile(r'(?<=\<title\>www\.whatip\.org -- Your IP is )'
    #                    '[\d]{1,3}.[\d]{1,3}.[\d]{1,3}.[\d]{1,3}(?=\<\/title\>)')
    # fut = asyncio.gather(*[get_ip_by_re(localhost, port, r_exp) for port in range(10025, 10030)])
    res = loop.run_until_complete(fut)
    loop.close()
    print(res)
