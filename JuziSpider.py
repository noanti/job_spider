#!/usr/bin/env python3
# coding: utf-8

import json
from random import choice

import requests
from bs4 import BeautifulSoup

from settings import *

itjuzi_url = 'http://www.itjuzi.com/company/'


class CompanyInfo:
    def __init__(self, company_id, company_name=''):
        self.company_id = company_id
        self.company_name = company_name
        self.state = ''
        self.main_page = ''
        self.place = ''
        self.production = []

    def __repr__(self):
        return self.company_id + ',' + self.company_name


def scrap_info(company_id):
    url = itjuzi_url + company_id

    resp = None
    retry_times = 0
    headers = {'User-Agent': choice(random_ua)}
    while resp is None and retry_times < request_retry:
        try:
            resp = requests.get(url, headers=headers, allow_redirects=False)
        except Exception as e:
            print(e)
            retry_times += 1
    if resp.status_code != 200: return CompanyInfo(company_id, 'HTTPError<%d>' % resp.status_code)

    company = CompanyInfo(company_id)
    soup = BeautifulSoup(resp.content, 'html.parser')

    name_state = soup.find('span', class_='title').contents[1].contents
    company.company_name = name_state[0].string.strip().replace('\t', '')
    company.state = name_state[1].string.strip()
    company.main_page = soup.find('a', class_='weblink marl10')['href']
    place = soup.find('span', class_='loca c-gray-aset').contents
    company.place = place[1].string if len(place) >= 1 else ''
    company.place += '-' + place[5].string if len(place) >= 5 else ''
    productions = soup.find('ul', class_='list-prod')
    if productions is None:
        company.production = []
    else:
        for each_prod in productions.children:
            if each_prod.name != 'li':
                continue
            type = each_prod.div.h4.span.string
            name = each_prod.div.h4.b.a.string
            intro = each_prod.div.p.string
            company.production.append((type,name, intro))

    return company


def main():
    result = []
    temp_file = open('temp.txt', 'a', encoding='utf-8')
    for i in range(1651, 2001):
        company = scrap_info(str(i))
        print(company)
        temp_file.write(json.dumps(company.__dict__, ensure_ascii=False, indent=4))
        temp_file.write(',\n')
        temp_file.flush()
        result.append(company.__dict__)

    f = open('juzi.txt', 'w', encoding='utf-8')
    f.write(json.dumps(result, ensure_ascii=False, indent=4))
    f.close()

if __name__ == '__main__':
    main()
    # print(json.dumps(scrap_info('1651').__dict__, ensure_ascii=False, indent=4).encode('utf8'))
