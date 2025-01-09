#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: 钉钉或微信pythontesting 钉钉群21734177
# CreateDate: 2019-2-21

import argparse
import collections
import pprint
import datetime

from bidict import bidict
import lunar_python
from datas import *
from ganzhi import *
from sizi import summarys

def check_gan(gan, gans):
    result = ''
    if ten_deities[gan]['合'] in gans:
        result += "合" + ten_deities[gan]['合']
    if ten_deities[gan]['冲'] in gans:
        result += "冲" + ten_deities[gan]['冲']
    return result

def yinyang(item):
    if item in Gan:
        return '＋' if Gan.index(item)%2 == 0 else '－'
    else:
        return '＋' if Zhi.index(item)%2 == 0 else '－'
    
def yinyangs(zhis):
    result = []
    for item in zhis:
        result.append(yinyang(item))
    if set(result) == set('＋'):
        print("四柱全阳")
    if set(result) == set('－'):
        print("四柱全阴")
    
    
    
    
def get_empty(zhu, zhi):
    empty = empties[zhu]
    if zhi in empty:
        return "空"
    return ""

def get_zhi_detail(zhi, me, multi=1):
    out = ''
    for gan in zhi5[zhi]:
        out = out + "{}{}{}{} ".format(gan, gan5[gan], zhi5[zhi][gan]*multi,  
                                       ten_deities[me][gan])
    return out

def check_gong(zhis, n1, n2, me, hes, desc='三合拱'):
    result = ''
    if zhis[n1] + zhis[n2] in hes:
        gong = hes[zhis[n1] + zhis[n2]] 
        if gong not in zhis:
            result += "\t{}：{}{}-{}[{}]".format(
                desc, zhis[n1], zhis[n2], gong, get_zhi_detail(gong, me))
    return result


def get_geng(me,zhis):
    for zhi in [zhis.year, zhis.month, zhis.day, zhis.time]:
        for gan in zhi5[zhi]:
            if me == gan:
                # print(f"有根，根在{zhi}")
                return True #"强" 
    return False #"弱" 

# 计算八字强弱
def calculate_bazi_strength(me, zhis, lunar):
    if ten_deities[me]['阴阳'] == '阳':
        if ten_deities[me]['本'] == '土':
            if zhis[1] in ['辰','戌','丑','未']:  # 辰戌丑未月
                if lunar.getDay() >15:
                    return "强" 
                else:
                    return "弱"
            else:
                return "弱"
        else:
            if ten_deities[me]['本'] == zhi_wuhangs[zhis[1]]:
                return "强"
            else:
                return "弱"
    else:#yin
        if ten_deities[me]['本'] == '土':
            if zhis[1] in ['辰','戌','丑','未']:  # 辰戌丑未月
                if lunar.getDay() >15:
                    return "强" 
                else:
                    return "弱"
            else:
                return "弱"
        else:
            if ten_deities[me]['本'] == zhi_wuhangs[zhis[1]]:
                return "强"
            elif ten_deities[me]['被克'] == zhi_wuhangs[zhis[1]]:#日主被月令克
                return "弱"
            else:
                if get_geng(me,zhis):
                    return "强"#有根
                else:
                    return "弱"

    
    
# 魁罡格
def is_kuigang(zhus):
    if zhus[2] in (('庚','辰'), ('庚','戌'),('壬','辰'), ('戊','戌'),):
        return True
    else:
        return False

# 阳刃格 
def is_yangren(me,zhi_shens):
    if zhi_shens[1] == '劫' and  ten_deities[me]['阴阳'] == '阳':
        return True
    else:
        return False


def is_jianlu(zhi_shens):
    # 建禄格
    if zhi_shens[1] == '比':
        return True
    else: 
        return False