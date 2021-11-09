# -*- coding: UTF-8 -*-

from urllib.parse import urljoin
from lxml import html
import requests
import os


def new_links(old, actual):
    r = []
    for i in actual:
        if i not in old:
            r.append(i)
            old.append(i)  # избавляемся от дубликатов
            print(i)
    return r


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

site = 'https://www.uksap.ru/'
array_links = '//div[@class="news-list"][1]' + '//a'

old_links = []
try:
    with open(os.path.join(BASE_DIR, 'links'), 'r') as file:
        old_links = file.read().split('\n')
except FileNotFoundError:
    print('Файла нет, но мы не расстраиваемся')

response = requests.get(site)
if response.status_code == 200:
    tree = html.fromstring(response.content)

    links = [urljoin(site, link.attrib['href']) for link in tree.xpath(array_links)]
    links = list(set(links))

    new = new_links(old_links, links)

    with open(os.path.join(BASE_DIR, 'links'), 'w') as file:
        file.write('\n'.join(links))
else:
    print('Сайт вернул', response.status_code)
