# coding=utf-8

from urllib.parse import urljoin
from lxml import html
import requests
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

site = 'https://www.uksap.ru/'
array_links = '//div[@class="news-list"][1]' + '//a'

response = requests.get(site)
if response.status_code == 200:
    tree = html.fromstring(response.content)

    links = [urljoin(site, link.attrib['href']) for link in tree.xpath(array_links)]
    print(links)

    with open(os.path.join(BASE_DIR, 'links'), 'w') as file:
        file.write('\n'.join(links))
else:
    print('Сайт вернул', response.status_code)
