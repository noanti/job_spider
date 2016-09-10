#!/usr/bin/env python3
# coding: utf-8

from settings import *


def calc_text_weight(text):
    weight = 0
    for keyword, score in text_weight:
        if text.find(keyword) != -1:
            weight += score

    return weight


def calc_name_url_weight(name, url):
    weight = 0
    for keyword, score in name_url_weight:
        if name.find(keyword) != -1:
            weight += score
        if url.find(keyword) != -1:
            weight += score

    return weight

if __name__ == '__main__':
    pass