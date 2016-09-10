#!/usr/bin/env python3
# coding: utf-8

from gevent import monkey
monkey.patch_all()

import json
from random import choice
import re

import gevent
from gevent.queue import PriorityQueue, Queue
import requests
import tldextract
import chardet

from utils import *
from settings import *

task_q = Queue()
result_q = Queue()
view_urls = []

max_depth = 1


class Request:
    def __init__(self, url, depth):
        self.url = url
        self.parent = ''
        self.depth = depth

    def __lt__(self, rhs):
        return True


class JobSpider:
    def __init__(self, start_requests):
        self.start_request = start_requests
        self.domain = tldextract.extract(self.start_request.url).domain

        self.request_queue = PriorityQueue()
        self.result = {
            start_requests.url: 0,
        }
        self.gl_list = []
        self.stop_flag = False

    def start(self, number):
        resp = requests.get(self.start_request.url)
        if resp.status_code != 200:
            raise Exception('HTTPError<%d>' % resp.status_code)

        self.request_queue.put((0, self.start_request))
        for i in range(number):
            gl = gevent.spawn(self.downloader)
            self.gl_list.append(gl)
            gl.start()

    def stop(self):
        self.stop_flag = True

    def join(self):
        return gevent.joinall(self.gl_list)

    def downloader(self):
        a_re = re.compile(r'''<a.+?href=(['"])([^>\s]+)\1.*?>([\S\s]+?)<\/a>''', re.IGNORECASE)

        while not self.request_queue.empty():
            if self.stop_flag: break
            prio, request = self.request_queue.get()
            print(self.request_queue.qsize(), request.url)
            headers = {'User-Agent': choice(random_ua)}
            try:
                resp = requests.get(request.url, headers=headers)
            except Exception as e:
                continue
            print('get a resp')

            encoding = chardet.detect(resp.content)['encoding']
            html_text = resp.content.decode(encoding) if encoding is not None else resp.text
            self.result[request.url] += calc_text_weight(html_text)
            if self.result[request.url] >= 100:
                self.stop()
                break

            if request.depth == max_depth:
                continue

            matches = a_re.findall(html_text)
            for each_a in matches:
                href = each_a[1]
                name = each_a[2]
                if href.startswith('javascript'): continue
                if href.startswith('/'): href = request.url + href
                if href.startswith('http'):
                    new_request = Request(href, request.depth + 1)
                    self.result[href] = calc_name_url_weight(name, href)
                    if tldextract.extract(href).domain == self.domain:
                        self.request_queue.put((-self.result[href], new_request))
                    elif self.result[href] >= 80:
                        self.request_queue.put((-self.result[href], new_request))

f = open('result.txt', 'a', encoding='utf-8')


def worker():
    while not task_q.empty():
        company, request = task_q.get()
        spider = JobSpider(request)
        try:
            spider.start(10)
        except Exception as e:
            company['job_url'] = 'Fail to fetch this site:' + str(e)
        else:
            spider.join()
            urls = sorted(spider.result.items(), key=lambda x: -x[1])
            company['job_url'] = 'Nothing' if len(urls) == 0 else urls[0][0]
        result_dict = {'id': company['company_id'], 'name': company['company_name'], 'job': company['job_url']}
        print(result_dict)
        f.write(json.dumps(result_dict, indent=4, ensure_ascii=False))
        f.write(',\n')
        f.flush()

def read_file():
    f = open('temp.txt', 'r', encoding='utf-8')
    data = f.read()
    company_list = json.loads(data)
    for i in company_list:
        task_q.put((i, Request(i['main_page'], 0)))
    return company_list


def main():
    read_file()
    gl_list = []
    for i in range(10):
        gl = gevent.spawn(worker)
        gl_list.append(gl)
    gevent.joinall(gl_list)


if __name__ == '__main__':
    # spider = JobSpider(Request('http://www.123u.com/', 0))
    # spider.start(20)
    # spider.join()
    # print(sorted(spider.result.items(), key=lambda x: -x[1]))
    main()
