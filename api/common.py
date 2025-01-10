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
    
def get_lucky_color(colors_data, scores):
    """根据五行分数选择幸运色"""
    # 找出得分最高的五行
    max_element = max(scores.items(), key=lambda x: x[1])[0]
    
    # 五行与颜色分组的对应关系（基于colors.json的完整分组）
    element_to_color_category = {
        "金": ["金银", "灰白"],     # 金属光泽、白色系
        "木": ["绿", "青", "苍"],   # 植物、生机色系
        "水": ["蓝", "黑", "水"],   # 水系、暗色系
        "火": ["红", "紫"],         # 火焰、暖色系
        "土": ["黄", "棕"]  # 大地、土系
    }
    
    # 获取对应的颜色类别
    target_categories = element_to_color_category[max_element]
    
    # 从colors.json中筛选符合的颜色
    suitable_colors = []
    for color_group in colors_data:
        # 检查颜色组是否属于目标类别
        if color_group["name"] in target_categories:
            # 添加该组所有颜色，同时记录颜色分组信息
            suitable_colors.extend([{
                "name": color["name"],
                "hex": color["hex"],
                "category": color_group["name"]  # 添加分组信息
            } for color in color_group["colors"]])
    
    # 如果找到合适的颜色，随机选择一个
    if suitable_colors:
        import random
        lucky_color = random.choice(suitable_colors)
        # 返回时包含分组信息
        return {
            "name": lucky_color["name"],
            "hex": lucky_color["hex"],
            "category": lucky_color["category"]
        }
    
    # 如果没找到，返回默认颜色
    return {
        "name": "素",
        "hex": "#f2ecde",
        "category": "灰白"
    }

def get_lucky_numbers(gans, zhis, today_gans, today_zhis):
    """根据八字和当天天干地支计算幸运数字"""
    # 天干地支对应的数字
    gan_numbers = {
        "甲": 1, "乙": 2,
        "丙": 3, "丁": 4,
        "戊": 5, "己": 6,
        "庚": 7, "辛": 8,
        "壬": 9, "癸": 10
    }
    
    zhi_numbers = {
        "子": 1, "丑": 2, "寅": 3, "卯": 4,
        "辰": 5, "巳": 6, "午": 7, "未": 8,
        "申": 9, "酉": 10, "戌": 11, "亥": 12
    }
    
    # 收集所有数字
    numbers = []
    
    # 添加个人八字对应的数字
    for gan in gans:
        if gan in gan_numbers:
            numbers.append(gan_numbers[gan])
    
    for zhi in zhis:
        if zhi in zhi_numbers:
            num = zhi_numbers[zhi]
            numbers.append(num)
    
    # 添加当天天干地支对应的数字
    for gan in today_gans:
        if gan in gan_numbers:
            numbers.append(gan_numbers[gan])
    
    for zhi in today_zhis:
        if zhi in zhi_numbers:
            num = zhi_numbers[zhi]
            numbers.append(num)
    
    # 计算所有数字的和
    total = sum(numbers)
    
    # 获取当天日柱地支对应的数字作为除数
    day_zhi_number = zhi_numbers[today_zhis.day]
    
    # 计算余数（如果余数为0，则使用除数的值）
    lucky_number = total % day_zhi_number if total % day_zhi_number != 0 else day_zhi_number
    
    # 如果结果大于9，继续进行数字相加直到得到个位数
    while lucky_number > 9:
        lucky_number = sum(int(digit) for digit in str(lucky_number))
    
    return str(lucky_number)