# -*- coding: utf-8 -*-
import opencc
from pypinyin import pinyin, Style
from functools import lru_cache
from itertools import chain
import re


@lru_cache(1)
def _opencc_tw2s():
    return opencc.OpenCC('tw2s.json')

@lru_cache(1)
def _opencc_s2t():
    return opencc.OpenCC('s2tw.json')


def to_simplify(text: str) -> str:
    return _opencc_tw2s().convert(text)


def to_traditional(text: str) -> str:
    return _opencc_s2t().convert(text)


def to_upper(text: str) -> str:
    return text.upper()

def to_lower(text: str) -> str:
    return text.lower()

def to_pinyin(text: str) -> str:
    return " ".join(chain.from_iterable(pinyin(text)))

def to_pinyin_head(text: str) -> str:
    return " ".join(chain.from_iterable(pinyin(text, style=Style.INITIALS, strict=False)))

def replace_blank(text: str) -> str:
    return re.sub(r'[ \xa0\u3000\t]', "", text)

def replace_nl(text: str) -> str:
    return text.replace("\r", "").replace("\n", "")

def str_q2b(text: str) -> str:
    """全角转半角"""
    def _inner():
        for uchar in text:
            inside_code=ord(uchar)
            if inside_code == 12288:                              #全角空格直接转换            
                inside_code = 32 
            elif (inside_code >= 65281 and inside_code <= 65374): #全角字符（除空格）根据关系转化
                inside_code -= 65248

            yield chr(inside_code)
    return "".join(_inner())
    
def str_b2q(text: str) -> str:
    """半角转全角"""
    def _inner():
        for uchar in text:
            inside_code=ord(uchar)
            if inside_code == 32:                                 #半角空格直接转化                  
                inside_code = 12288
            elif inside_code >= 32 and inside_code <= 126:        #半角字符（除空格）根据关系转化
                inside_code += 65248

            yield chr(inside_code)
    return "".join(_inner())