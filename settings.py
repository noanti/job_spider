# coding: utf-8

request_timeout = 5
request_retry = 2
random_ua = [
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36',
    'Mozilla/5.0 (MSIE 10.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20120101 Firefox/33.0',
]

name_url_weight = [
    ('joinus', 80),
    ('join us', 80),
    ('加入我们', 80),
    ('job', 80),
    ('社招', 60),
    ('校招', 60),
    ('招聘', 80),
    ('join', 60),
    ('诚聘', 80),
    ('招贤纳士', 80),
    ('recruit', 80),
    ('hire', 80),
    ('招募', 80),
    ('jrwm', 80)
]

text_weight = [
    ('工作职责', 20),
    ('职位名称', 20),
    ('职位要求', 20),
    ('诚聘', 20),
    ('工作经验', 5),
    ('精通', 5),
    ('后端', 5),
    ('前端', 5),
    ('移动端', 5),
    ('销售', 5),
    ('开发', 5),
    ('五险一金', 5),
    ('福利', 5),
    ('服务端', 5),
]