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
    return r


def get_title(link):
    page = requests.get(link)
    if page.status_code == 200:
        title = os.environ['TITLE']
        if title == '':
            title = '//title'

        page = html.fromstring(page.content)
        r = page.xpath(title)[0].text
        return r
    else:
        return ''


def post(link):
    title = get_title(link)
    text = link
    if title != '':
        text = title + '\n' + text

    url = 'https://api.telegram.org/bot' + os.environ['BOT_TOKEN']
    method = url + '/sendMessage'

    request = requests.post(
        method,
        data={
            'chat_id': os.environ['CHANNEL'],
            'text': text,
        }
    )


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

site = os.environ['SITE']
array_links = os.environ['ARRAY_LINKS'] + '//a'

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

    new_links = new_links(old_links, links)
    for link in new_links:
        post(link)

    with open(os.path.join(BASE_DIR, 'links'), 'w') as file:
        file.write('\n'.join(links))
else:
    print('Сайт вернул', response.status_code)
