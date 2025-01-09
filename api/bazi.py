import sxtwl
import argparse
import collections
import pprint
import datetime
import sys
import cnlunar
from lunar_python import Lunar, Solar
from colorama import init
from yuantiangang import  ShengChen
from datas import *
from sizi import summarys
from common import *
from yue import months

original_stdout = sys.stdout
output_file = open('bazi_output.md', 'w', encoding='utf-8')
sys.stdout = output_file

print("# 八字分析报告\n")
print("## 免责声明\n")
print("1. 本报告仅基于您所提供的信息进行本次规划分析，结果仅供参考。")
print("2. 若有人利用本报告从事违法犯罪、非法牟利等行为，均由行为人自行承担全部法律责任，与\"金酒\"无关。")
print("3. 五行命理规划是中国传统文化的一部分，不属于封建迷信，请理性看待。")
print("4. 本报告不构成任何投资、法律、医疗等专业建议，重要决策请咨询相关领域专业人士。\n")

def get_gen(gan, zhis):
    zhus = []
    zhongs = []
    weis = []
    result = ""
    for item in zhis:
        zhu = zhi5_list[item][0]
        if ten_deities[gan]['本'] == ten_deities[zhu]['本']:
            zhus.append(item)

    for item in zhis:
        if len(zhi5_list[item]) ==1:
            continue
        zhong = zhi5_list[item][1]
        if ten_deities[gan]['本'] == ten_deities[zhong]['本']:
            zhongs.append(item)

    for item in zhis:
        if len(zhi5_list[item]) < 3:
            continue
        zhong = zhi5_list[item][2]
        if ten_deities[gan]['本'] == ten_deities[zhong]['本']:
            weis.append(item)

    if not (zhus or zhongs or weis):
        return "无根"
    else:
        result = result + "强：{}{}".format(''.join(zhus), chr(12288)) if zhus else result
        result = result + "中：{}{}".format(''.join(zhongs), chr(12288)) if zhongs else result
        result = result + "弱：{}".format(''.join(weis)) if weis else result
        return result


def gan_zhi_he(zhu):
    gan, zhi = zhu
    if ten_deities[gan]['合'] in zhi5[zhi]:
        return "|"
    return ""

def get_gong(zhis):
    result = []
    for i in range(3):
        if  gans[i] != gans[i+1]:
            continue
        zhi1 = zhis[i]
        zhi2 = zhis[i+1]
        if abs(Zhi.index(zhi1) - Zhi.index(zhi2)) == 2:
            value = Zhi[(Zhi.index(zhi1) + Zhi.index(zhi2))//2]
            #if value in ("丑", "辰", "未", "戌"):
            result.append(value)
        if (zhi1 + zhi2 in gong_he) and (gong_he[zhi1 + zhi2] not in zhis):
            result.append(gong_he[zhi1 + zhi2]) 
            
        #if (zhi1 + zhi2 in gong_hui) and (gong_hui[zhi1 + zhi2] not in zhis):
            #result.append(gong_hui[zhi1 + zhi2])             
        
    return result


def get_shens(gans, zhis, gan_, zhi_):
    
    all_shens = []
    for item in year_shens:
        if zhi_ in year_shens[item][zhis.year]:    
            all_shens.append(item)
                
    for item in month_shens:
        if gan_ in month_shens[item][zhis.month] or zhi_ in month_shens[item][zhis.month]:     
            all_shens.append(item)
                
    for item in day_shens:
        if zhi_ in day_shens[item][zhis.day]:     
            all_shens.append(item)
                
    for item in g_shens:
        if zhi_ in g_shens[item][me]:    
            all_shens.append(item) 
    if all_shens:  
        return "  神:" + ' '.join(all_shens)
    else:
        return ""
                
def jin_jiao(first, second):
    return True if Zhi.index(second) - Zhi.index(first) == 1 else False

def is_ku(zhi):
    return True if zhi in "辰戌丑未" else False  

def zhi_ku(zhi, items):
    return True if is_ku(zhi) and min(zhi5[zhi], key=zhi5[zhi].get) in items else False

def is_yang():
    return True if Gan.index(me) % 2 == 0 else False

def not_yang():
    return False if Gan.index(me) % 2 == 0 else True

def gan_ke(gan1, gan2):
    return True if ten_deities[gan1]['克'] == ten_deities[gan2]['本'] or ten_deities[gan2]['克'] == ten_deities[gan1]['本'] else False
    
description = '''

'''

parser = argparse.ArgumentParser(description=description,
                                 formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('year', action="store", help=u'year')
parser.add_argument('month', action="store", help=u'month')
parser.add_argument('day', action="store", help=u'day')
parser.add_argument('time', action="store",help=u'time')    
parser.add_argument("--start", help="start year", type=int, default=1850)
parser.add_argument("--end", help="end year", default='2030')
parser.add_argument('-b', action="store_true", default=False, help=u'直接输入八字')
parser.add_argument('-g', action="store_true", default=False, help=u'是否采用公历')
parser.add_argument('-r', action="store_true", default=False, help=u'是否为闰月，仅仅使用于农历')
parser.add_argument('-n', action="store_true", default=False, help=u'是否为女，默认为男')
parser.add_argument('--version', action='version',
                    version='%(prog)s 1.0')
parser.add_argument('-name', action="store", help=u'命主姓名')

options = parser.parse_args()

Gans = collections.namedtuple("Gans", "year month day time")
Zhis = collections.namedtuple("Zhis", "year month day time")

if options.b:
    import sxtwl
    gans = Gans(year=options.year[0], month=options.month[0], 
                day=options.day[0],  time=options.time[0])
    zhis = Gans(year=options.year[1], month=options.month[1], 
                day=options.day[1],  time=options.time[1])
    jds = sxtwl.siZhu2Year(getGZ(options.year), getGZ(options.month), getGZ(options.day), getGZ(options.time), options.start, int(options.end));
    for jd in jds:
        t = sxtwl.JD2DD(jd )
        # print("可能出生时间: python bazi.py -g %d %d %d %d :%d:%d"%(t.Y, t.M, t.D, t.h, t.m, round(t.s)))   
    
else:

    if options.g:
        solar = Solar.fromYmdHms(int(options.year), int(options.month), int(options.day), int(options.time), 0, 0)
        lunar = solar.getLunar()
    else:
        month_ = int(options.month)*-1 if options.r else int(options.month)
        lunar = Lunar.fromYmdHms(int(options.year), month_, int(options.day),int(options.time), 0, 0)
        solar = lunar.getSolar()

    day = lunar
    ba = lunar.getEightChar() 
    gans = Gans(year=ba.getYearGan(), month=ba.getMonthGan(), day=ba.getDayGan(), time=ba.getTimeGan())
    zhis = Zhis(year=ba.getYearZhi(), month=ba.getMonthZhi(), day=ba.getDayZhi(), time=ba.getTimeZhi())


me = gans.day
month = zhis.month
alls = list(gans) + list(zhis)
zhus = [item for item in zip(gans, zhis)]

gan_shens = []
for seq, item in enumerate(gans):    
    if seq == 2:
        gan_shens.append('--')
    else:
        gan_shens.append(ten_deities[me][item])
#print(gan_shens)

zhi_shens = [] # 地支的主气神
for item in zhis:
    d = zhi5[item]
    zhi_shens.append(ten_deities[me][max(d, key=d.get)])
# print("地支主气神：",zhi_shens)
shens = gan_shens + zhi_shens

zhi_shens2 = [] # 地支的所有神，包含余气和尾气, 混合在一起
zhi_shen3 = [] # 地支所有神，字符串格式
for item in zhis:
    d = zhi5[item]
    tmp = ''
    for item2 in d:
        zhi_shens2.append(ten_deities[me][item2])
        tmp += ten_deities[me][item2]
    zhi_shen3.append(tmp)
shens2 = gan_shens + zhi_shens2



# 计算五行分数 http://www.131.com.tw/word/b3_2_14.htm

scores = {"金":0, "木":0, "水":0, "火":0, "土":0}
gan_scores = {"甲":0, "乙":0, "丙":0, "丁":0, "戊":0, "己":0, "庚":0, "辛":0,
              "壬":0, "癸":0}   

for item in gans:  
    scores[gan5[item]] += 5
    gan_scores[item] += 5


for item in list(zhis) + [zhis.month]:  
    for gan in zhi5[item]:
        scores[gan5[gan]] += zhi5[item][gan]
        gan_scores[gan] += zhi5[item][gan]


# 计算八字强弱
# 子平真诠的计算
weak = True
me_status = []
for item in zhis:
    me_status.append(ten_deities[me][item])
    if ten_deities[me][item] in ('长', '帝', '建'):
        weak = False
        

if weak:
    if shens.count('比') + me_status.count('库') >2:
        weak = False

# 计算大运
seq = Gan.index(gans.year)
if options.n:
    if seq % 2 == 0:
        direction = -1
    else:
        direction = 1
else:
    if seq % 2 == 0:
        direction = 1
    else:
        direction = -1

dayuns = []
gan_seq = Gan.index(gans.month)
zhi_seq = Zhi.index(zhis.month)
for i in range(12):
    gan_seq += direction
    zhi_seq += direction
    dayuns.append(Gan[gan_seq%10] + Zhi[zhi_seq%12])

# 网上的计算
me_attrs_ = ten_deities[me].inverse
strong = gan_scores[me_attrs_['比']] + gan_scores[me_attrs_['劫']] \
    + gan_scores[me_attrs_['枭']] + gan_scores[me_attrs_['印']]


# if not options.b:
#     #print("direction",direction)
#     sex = '女' if options.n else '男'
#     print("{}命".format(sex), end=' ')
#     print("\t公历:", end=' ')
#     print("{}年{}月{}日".format(solar.getYear(), solar.getMonth(), solar.getDay()), end=' ')
#     yun = ba.getYun(not options.n)   
#     print("  农历:", end=' ')
#     print("{}年{}月{}日 穿=害 上运时间：{} 命宫:{} 胎元:{}\n".format(lunar.getYear(), lunar.getMonth(), 
#         lunar.getDay(), yun.getStartSolar().toFullString().split()[0], ba.getMingGong(), ba.getTaiYuan()), end=' ')
#     print("\t", siling[zhis.month], lunar.getPrevJieQi(True), lunar.getPrevJieQi(True).getSolar().toYmdHms(),lunar.getNextJieQi(True), 
#         lunar.getNextJieQi(True).getSolar().toYmdHms())
options.name
if not options.b:
    sex = '女' if options.n else '男'
    print("## 一、基本信息\n")
    print("<table align=\"center\">")
    print("  <tr>")
    print(f"    <td align=\"center\"><strong>命主:</strong></td>")
    print(f"    <td align=\"center\">{sex}命</td>")
    print(f"    <td align=\"center\"><strong>姓名:</strong></td>")
    print(f"    <td align=\"center\" colspan=\"3\">{options.name}</td>")
    print("  </tr>")
    print("  <tr>")
    print(f"    <td align=\"center\"><strong>公历:</strong></td>")
    print(f"    <td align=\"center\">{solar.getYear()}年{solar.getMonth()}月{solar.getDay()}日</td>")
    print(f"    <td align=\"center\"><strong>农历:</strong></td>")
    print(f"    <td align=\"center\">{lunar.getYear()}年{lunar.getMonth()}月{lunar.getDay()}日</td>")
    print(f"    <td align=\"center\"><strong>上运时间:</strong></td>")
    yun = ba.getYun(not options.n)
    print(f"    <td align=\"center\">{yun.getStartSolar().toFullString().split()[0].replace('-', '年', 1).replace('-', '月', 1) + '日'}</td>")
    print("  </tr>")
    print("  <tr>")
    print(f"    <td align=\"center\"><strong>节气:</strong></td>")
    print(f"    <td align=\"center\" colspan=\"5\">{lunar.getPrevJieQi(True)}{lunar.getPrevJieQi(True).getSolar().toYmdHms()}——{lunar.getNextJieQi(True)}{lunar.getNextJieQi(True).getSolar().toYmdHms()}</td>")
    print("  </tr>")
    print("</table>\n")

#print(zhi_3hes, "生：寅申巳亥 败：子午卯酉　库：辰戌丑未")
#print("地支六合:", zhi_6hes)
out = ''
for item in zhi_3hes:
    out = out + "{}:{}  ".format(item, zhi_3hes[item])

def get_color(wuxing):
    colors = {
        '木': 'green',
        '火': 'red',
        '土': 'brown',
        '金': 'gold',
        '水': 'blue'
    }
    return colors.get(wuxing, 'black')
# print('\033[1;36;40m' + ' '.join(list(gans)), ' '*5, ' '.join(list(gan_shens)) + '\033[0m',' '*5, out,)
print("\n## 二、八字详解\n")
print(f"您的八字是：{gans.year}{zhis.year}年，{gans.month}{zhis.month}月，{gans.day}{zhis.day}日，{gans.time}{zhis.time}时\n")
print("<table align=\"center\">")
print("  <tr>")
print("    <th></th>")
print("    <th>年柱</th>")
print("    <th>月柱</th>")
print("    <th>日柱</th>")
print("    <th>时柱</th>")
print("  </tr>")
print("  <tr>")
print("    <td><strong>天干</strong></td>")
for gan in [gans.year, gans.month, gans.day, gans.time]:
    wuxing = gan5[gan]
    color = get_color(wuxing)
    print(f"    <td align=\"center\"><font color=\"{color}\">{gan}</font></td>")
print("  </tr>")
print("  <tr>")
print("    <td><strong>地支</strong></td>")
for zhi in [zhis.year, zhis.month, zhis.day, zhis.time]:
    wuxing = zhi_wuhangs[zhi]
    color = get_color(wuxing)
    print(f"    <td align=\"center\"><font color=\"{color}\">{zhi}</font></td>")
print("  </tr>")
print("  <tr>")
print("    <td><strong>天干十神</strong></td>")
for i, shen in enumerate(gan_shens):
    wuxing = gan5[gans[i]] if i != 2 else gan5[me]
    color = get_color(wuxing)
    print(f"    <td align=\"center\"><font color=\"{color}\">{shen}</font></td>")
print("  </tr>")
print("  <tr>")
print("    <td><strong>地支十神</strong></td>")
for i, shen in enumerate(zhi_shens):
    wuxing = zhi_wuhangs[zhis[i]]
    color = get_color(wuxing)
    print(f"    <td align=\"center\"><font color=\"{color}\">{shen}</font></td>")
print("  </tr>")
print("  <tr>")
print("    <td><strong>地支藏干</strong></td>")
for zhi in [zhis.year, zhis.month, zhis.day, zhis.time]:
    hidden_gans = ""
    for gan in zhi5[zhi]:
        wuxing = gan5[gan]
        color = get_color(wuxing)
        hidden_gans += f"<font color=\"{color}\">{gan}</font>"
    print(f"    <td align=\"center\">{hidden_gans}</td>")
print("  </tr>")
print("</table>\n")


# print('\033[1;36;40m' + ' '.join(list(zhis)), ' '*5, ' '.join(list(zhi_shens)) + '\033[0m', ' '*5, out, "解读:")


# print("-"*120)
# print("{1:{0}^15s}{2:{0}^15s}{3:{0}^15s}{4:{0}^15s}".format(chr(12288), '【年】{}:{}{}{}'.format(temps[gans.year],temps[zhis.year],ten_deities[gans.year].inverse['建'], gan_zhi_he(zhus[0])), 
#     '【月】{}:{}{}{}'.format(temps[gans.month],temps[zhis.month], ten_deities[gans.month].inverse['建'], gan_zhi_he(zhus[1])),
#     '【日】{}:{}{}'.format(temps[me], temps[zhis.day], gan_zhi_he(zhus[2])), 
#     '【时】{}:{}{}{}'.format(temps[gans.time], temps[zhis.time], ten_deities[gans.time].inverse['建'], gan_zhi_he(zhus[3]))))
# print("-"*120)


# print("\033[1;36;40m{1:{0}<15s}{2:{0}<15s}{3:{0}<15s}{4:{0}<15s}\033[0m".format(
#     chr(12288),
#     '{}{}{}【{}】{}'.format(
#         gans.year, yinyang(gans.year), gan5[gans.year], ten_deities[me][gans.year], check_gan(gans.year, gans)),
#     '{}{}{}【{}】{}'.format(
#         gans.month, yinyang(gans.month), gan5[gans.month], ten_deities[me][gans.month], check_gan(gans.month, gans)),
#     '{}{}{}{}'.format(me, yinyang(me),gan5[me], check_gan(me, gans)),
#     '{}{}{}【{}】{}'.format(gans.time, yinyang(gans.time), gan5[gans.time], ten_deities[me][gans.time], check_gan(gans.time, gans)),
# ))

# print("\033[1;36;40m{1:{0}<15s}{2:{0}<15s}{3:{0}<15s}{4:{0}<15s}\033[0m".format(
#     chr(12288),
#     "{}{}{}【{}】{}".format(
#         zhis.year, yinyang(zhis.year), ten_deities[me][zhis.year],
#         ten_deities[gans.year][zhis.year], get_empty(zhus[2],zhis.year)),
#     "{}{}{}【{}】{}".format(
#         zhis.month, yinyang(zhis.month), ten_deities[me][zhis.month],
#         ten_deities[gans.month][zhis.month], get_empty(zhus[2],zhis.month)),
#     "{}{}{}".format(zhis.day, yinyang(zhis.day), ten_deities[me][zhis.day]),   
#     "{}{}{}【{}】{}".format(
#         zhis.time, yinyang(zhis.time), ten_deities[me][zhis.time], 
#         ten_deities[gans.time][zhis.time], get_empty(zhus[2],zhis.time)),
# ))

statuses = [ten_deities[me][item] for item in zhis]


for seq, item in enumerate(zhis):
    out = ''
    multi = 2 if item == zhis.month and seq == 1 else 1

    for gan in zhi5[item]:
        out = out + "{}{}{}　".format(gan, gan5[gan], ten_deities[me][gan])
    # print("\033[1;36;40m{1:{0}<15s}\033[0m".format(chr(12288), out.rstrip('　')), end='')

# print()
# 输出地支关系
for seq, item in enumerate(zhis):

    output = ''
    others = zhis[:seq] + zhis[seq+1:] 
    for type_ in zhi_atts[item]:
        flag = False
        if type_ in ('害',"破","会",'刑'):
            continue
        for zhi in zhi_atts[item][type_]:
            if zhi in others:
                if not flag:
                    output = output + "　" + type_ + "：" if type_ not in ('冲','暗') else output + "　" + type_
                    flag = True
                if type_ not in ('冲','暗'):
                    output += zhi
        output = output.lstrip('　')
    # print("\033[1;36;40m{1:{0}<15s}\033[0m".format(chr(12288), output), end='')


# 输出地支minor关系
for seq, item in enumerate(zhis):

    output = ''
    others = zhis[:seq] + zhis[seq+1:] 
    for type_ in zhi_atts[item]:
        flag = False
        if type_ not in ('害',"会"):
            continue
        for zhi in zhi_atts[item][type_]:
            if zhi in others:
                if not flag:
                    output = output + "　" + type_ + "："
                    flag = True
                output += zhi
    output = output.lstrip('　')
    # print("\033[1;36;40m{1:{0}<15s}\033[0m".format(chr(12288), output), end='')


# 输出根
for  item in gans:
    output = output.lstrip('　')
    # print("\033[1;36;40m{1:{0}<15s}\033[0m".format(chr(12288), get_gen(item, zhis)), end='')


for seq, item in enumerate(zhus):

    # 检查空亡 
    result = "{}－{}".format(nayins[item], '亡') if zhis[seq] == wangs[zhis[0]] else nayins[item]
    
    # 天干与地支关系
    result = relations[(gan5[gans[seq]], zhi_wuhangs[zhis[seq]])] + result
        
    # 检查劫杀 
    result = "{}－{}".format(result, '劫杀') if zhis[seq] == jieshas[zhis[0]] else result
    # 检查元辰
    result = "{}－{}".format(result, '元辰') if zhis[seq] == Zhi[(Zhi.index(zhis[0]) + direction*-1*5)%12] else result    
    # print("{1:{0}<15s} ".format(chr(12288), result), end='')


all_ges = []

# 神煞计算

strs = ['','','','',]

all_shens = set()
all_shens_list = []

for item in year_shens:
    for i in (1,2,3):
        if zhis[i] in year_shens[item][zhis.year]:    
            strs[i] = item if not strs[i] else strs[i] + chr(12288) + item
            all_shens.add(item)
            all_shens_list.append(item)
            
for item in month_shens:
    for i in range(4):
        if gans[i] in month_shens[item][zhis.month] or zhis[i] in month_shens[item][zhis.month]:     
            strs[i] = item if not strs[i] else strs[i] + chr(12288) + item
            if i == 2 and gans[i] in month_shens[item][zhis.month]:
                strs[i] = strs[i] + "●"
            all_shens.add(item)
            all_shens_list.append(item)
            
for item in day_shens:
    for i in (0,1,3):
        if zhis[i] in day_shens[item][zhis.day]:     
            strs[i] = item if not strs[i] else strs[i] + chr(12288) + item    
            all_shens.add(item)
            all_shens_list.append(item)
            
for item in g_shens:
    for i in range(4):
        if zhis[i] in g_shens[item][me]:    
            strs[i] = item if not strs[i] else strs[i] + chr(12288) + item
            all_shens.add(item)
            all_shens_list.append(item)
            
# print(all_shens_list)
#print(strs)           
# for seq in range(2):
#     print("{1:{0}<15s} ".format(chr(12288), strs[seq]), end='')
# for seq in range(2,4):
#     print("{1:{0}<14s} ".format(chr(12288), strs[seq]), end='')
    


# 计算六合:相邻的才算合

zhi_6he = [False, False, False, False]

for i in range(3):
    if zhi_atts[zhis[i]]['六'] == zhis[i+1]:
        zhi_6he[i] = zhi_6he[i+1] = True
        
# 计算六冲:相邻的才算合

zhi_6chong = [False, False, False, False]

for i in range(3):
    if zhi_atts[zhis[i]]['冲'] == zhis[i+1]:
        zhi_6chong[i] = zhi_6chong[i+1] = True
        
# 计算干合:相邻的才算合

gan_he = [False, False, False, False]
for i in range(3):
    if (gans[i],gans[i+1]) in set(gan_hes) or (gans[i+1],gans[i]) in set(gan_hes):
        gan_he[i] = gan_he[i+1] = True
        
# 计算刑:相邻的才算

zhi_xing = [False, False, False, False]

for i in range(3):
    if zhi_atts[zhis[i]]['刑'] == zhis[i+1] or zhi_atts[zhis[i+1]]['刑'] == zhis[i]:
        zhi_xing[i] = zhi_xing[i+1] = True
# print()
print("```")      
print("大运：", end=' ')

for item in dayuns:
    print(item, end=' ')


print("\n```")
# print()
# for item in gans:
#     print(get_gen(item, zhis), end=" \t")
# print()
me_lu = ten_deities[me].inverse['建']

me_jue = ten_deities[me].inverse['绝']
me_tai = ten_deities[me].inverse['胎']
me_di = ten_deities[me].inverse['帝']
shang = ten_deities[me].inverse['伤']
shang_lu = ten_deities[shang].inverse['建']
shang_di = ten_deities[shang].inverse['帝']
yin = ten_deities[me].inverse['印']
yin_lu = ten_deities[yin].inverse['建']
xiao = ten_deities[me].inverse['枭']
xiao_lu = ten_deities[xiao].inverse['建']
cai = ten_deities[me].inverse['财']
cai_lu = ten_deities[cai].inverse['建']
cai_di = ten_deities[cai].inverse['帝']
piancai = ten_deities[me].inverse['才']
piancai_lu = ten_deities[piancai].inverse['建']
piancai_di = ten_deities[piancai].inverse['帝']
guan = ten_deities[me].inverse['官']
guan_lu = ten_deities[guan].inverse['建']
guan_di = ten_deities[guan].inverse['帝']
sha = ten_deities[me].inverse['杀']
sha_lu = ten_deities[sha].inverse['建']
sha_di = ten_deities[sha].inverse['帝']

jie = ten_deities[me].inverse['劫']
shi = ten_deities[me].inverse['食']
shi_lu = ten_deities[shi].inverse['建']
shi_di = ten_deities[shi].inverse['帝']

me_ku = ten_deities[me]['库'][0]
cai_ku = ten_deities[cai]['库'][0]
guan_ku = ten_deities[guan]['库'][0]
yin_ku = ten_deities[yin]['库'][0]
shi_ku = ten_deities[shi]['库'][0]



print("## 调候与格局分析")
print("```")
print(f"- 调候：{tiaohous[f'{me}{zhis[1]}']}")
print(f"- 金不换大运：{jinbuhuan[f'{me}{zhis[1]}']}")
# print(f"- 金不换大运说明：{jins[f'{me}']}")
print("\n```")
# print(f"- 格局选用：{ges[ten_deities[me]['本']][zhis[1]]}")

if len(set('寅申巳亥')&set(zhis)) == 0:
    print("缺四生：一生不敢作为")
if len(set('子午卯酉')&set(zhis)) == 0:
    print("缺四柱地支缺四正，一生避是非")
if len(set('辰戌丑未')&set(zhis)) == 0:
    print("四柱地支缺四库，一生没有潜伏性凶灾。")
if ( '甲', '戊', '庚',) in (tuple(gans)[:3], tuple(gans)[1:]):
    print("地上三奇：白天生有申佳，需身强四柱有贵人。")
if ( '辛', '壬', '癸',) in (tuple(gans)[:3], tuple(gans)[1:]):
    print("人间三奇，需身强四柱有贵人。")
if ( '乙', '丙', '丁',) in (tuple(gans)[:3], tuple(gans)[1:]):
    print("天上三奇：晚上生有亥佳，需身强四柱有贵人。")
    
if zhi_shens2.count('亡神') > 1:
    print("二重亡神，先丧母；")
    
if get_empty(zhus[2],zhis.time):
    print("时坐空亡，子息少。 母法P24-41 母法P79-4：损破祖业，后另再成就。")
    
if zhis.count(me_jue) + zhis.count(me_tai) > 2:
    print("胎绝超过3个：夭或穷。母法P24-44 丁未 壬子 丙子 戊子")
       
if not_yang() and zhi_ku(zhis[2], (me,jie)) and zhi_ku(zhis[3], (me,jie)):
    print("阴日主时日支入比劫库：性格孤独，难发达。母法P28-112 甲申 辛未 辛丑 己丑 母法P55-11 为人孤独，且有灾疾")

#print(cai_lu, piancai_lu)
if zhis[1:].count(piancai_lu) + zhis[1:].count(cai_lu) + zhis[1:].count(piancai_di) + zhis[1:].count(cai_di) == 0:
    print("月日时支没有财或偏财的禄旺。")
    
if zhis[1:].count(guan_lu) + zhis[1:].count(guan_di) == 0:
    print("月日时支没有官的禄旺。")
    
if '辰' in zhis and ('戌' not in zhis) and options.n: 
    print("女命有辰无戌：孤。")
if '戌' in zhis and ('辰' not in zhis) and options.n: 
    print("女命有戌无辰：带禄。")
    
if emptie4s.get(zhus[2], 0) != 0:
    if scores[emptie4s.get(zhus[2], 0)] == 0:
        print("四大空亡：33岁以前身体不佳！")


# print("## 神煞分析")
# for item in all_shens:
#     print(item, ":",  shens_infos[item])
    
if options.n:
    # print("#"*20, "女命")
    if all_shens_list.count("驿马") > 1:
        # print("二逢驿马，母家荒凉。丙申 丙申 甲寅 丁卯")
        print("驿马：驿马为动星，主迁移、变动、迁移、旅游等。驿马在年柱，主祖业漂泊不定；驿马在月柱，主兄弟姐妹多变动；驿马在日柱，主婚姻多变；驿马在时柱，主子女多变动。")
    # if gan_shens[0] == '伤':
    #     print("年上伤官：带疾生产。戊寅 戊午 丁未 丁未")    


            


children = ['食','伤'] if options.n else ['官','杀']

liuqins = bidict({'才': '父亲',"财":'财' if options.n else '妻', "印": '母亲', "枭": '偏印' if options.n else '祖父',
                  "官":'丈夫' if options.n else '女儿', "杀":'情夫' if options.n else '儿子', "劫":'兄弟' if options.n else '姐妹', "比":'姐妹' if options.n else '兄弟', 
                  "食":'女儿' if options.n else '下属', "伤":'儿子' if options.n else '孙女'})

# 六亲分析
# for item in Gan:
#     print("{}:{} {}-{} {} {} {}".format(item, ten_deities[me][item], liuqins[ten_deities[me][item]],  ten_deities[item][zhis[0]] ,ten_deities[item][zhis[1]], ten_deities[item][zhis[2]], ten_deities[item][zhis[3]]), end='  ')
#     if Gan.index(item) == 4:
#         print()
    
# print()
# print()

# 计算上运时间，有年份时才适用

temps_scores = temps[gans.year] + temps[gans.month] + temps[me] + temps[gans.time] + temps[zhis.year] + temps[zhis.month]*2 + temps[zhis.day] + temps[zhis.time]
# print("\033[1;36;40m五行分数", scores, '  八字强弱：', strong, "通常>29为强，需要参考月份、坐支等", "weak:", weak)

print("### 五行分数\n")
print("五行分数表：共", sum(scores.values()), "分")

print("| 金 | 木 | 水 | 火 | 土 |")
print("|:---:|:---:|:---:|:---:|:---:|")
print(f"| {scores['金']:^3} | {scores['木']:^3} | {scores['水']:^3} | {scores['火']:^3} | {scores['土']:^3} |")

print("```")
print("天运五行：", zhi_wuhangs[zhis[1]])
# print("五行旺衰：")



gongs = get_gong(zhis)
zhis_g = set(zhis) | set(gongs)

jus = []
for item in zhi_hes:
    if set(item).issubset(zhis_g):
        print("三合局", item)
        jus.append(ju[ten_deities[me].inverse[zhi_hes[item]]])
        
        
for item in zhi_huis:
    if set(item).issubset(zhis_g):
        print("三会局", item)
        jus.append(ju[ten_deities[me].inverse[zhi_huis[item]]])


for item in gan_scores:  
    print("{}[{}]:{} ".format(
        item, ten_deities[me][item], gan_scores[item]),  end='  ') 

print("\n```")


print(f"- 格局选用：{ges[ten_deities[me]['本']][zhis[1]]}")


print("\n### 八字暖寒分析\n")
# print(f"湿度分数: {temps_scores}")
# print("- 正为暖燥，负为寒湿")  
# print("- 正常区间: [-6, 6]")
if temps_scores > 6:
    print(f"湿度结果: 偏暖燥 ({temps_scores})")
elif temps_scores < -6:
    print(f"湿度结果: 偏寒湿 ({temps_scores})")
else:
    print(f"湿度结果: 正常 ({temps_scores})")
# print(f"拱: {get_gong(zhis)}")

print()

print("\n### 八字十神分析\n")
print("以日干为主，分析十神关系，为八字局部关系。分析有专业术语，后续以命理解读内容为准。")

print("```")
yinyangs(zhis)
shen_zhus = list(zip(gan_shens, zhi_shens))

minggong = Zhi[::-1][(Zhi.index(zhis[1]) + Zhi.index(zhis[3]) -6  )%12 ]
# print(minggong, minggongs[minggong])
# print("坐：", rizhus[me+zhis.day])



# 天罗地网
if ('辰' in zhis and '巳' in zhis) or ('戌' in zhis and '亥' in zhis):
    print("命局中出现天罗地网：天罗为戌亥，地网为辰巳。这种组合通常被视为不利，可能会给人生带来阻碍和困难。")

# 魁罡格
if zhus[2] in (('庚','辰'), ('庚','戌'),('壬','辰'), ('戊','戌'),):
    print("命局中出现魁罡格：日柱为庚辰、庚戌、壬辰或戊戌。这是一种较为特殊的格局，代表人具有独特的个性和能力。如果日主强，且没有刑冲，通常是很好的命格。")
    print("魁罡格特点：性格刚强，有领导才能，但也可能固执。如果财官显露过多，可能会遇到困难。建议保持谦逊，避免与人冲突。")

# 金神格
if zhus[3] in (('乙','丑'), ('己','巳'),('癸','酉')):
    print("命局中出现金神格：时柱为乙丑、己巳或癸酉。这种格局只适用于甲日或己日出生的人，尤其是甲子日和甲辰日最为突出。如果月支与金火相通，通常预示着良好的命运。")
    
# 六阴朝阳
if me == '辛' and zhis.time == '子':
    print("命局中出现六阴朝阳格：辛日生人，时柱为子时。这种格局象征着在困境中看到希望，预示人生可能会有转机。")
    
# 六乙鼠贵
if me == '乙' and zhis.time == '子':
    print("命局中出现六乙鼠贵格：乙日生人，时柱为子时。这是一种吉利的格局，但需要注意避开午冲和丑合。最好月支通木局或水局，不宜金火。申酉大运可能带来不利影响。")

# 从格
if max(scores.values()) > 25:
    print("命局中某个五行的得分超过25分，需要考虑是否形成专格或从格。")
    print("从旺格：代表人生态度安稳，远离伤害，淡泊名利。从势格：表示日主较弱，需要依附他人。这两种格局都需要根据具体情况来判断利弊。")
    
    
if zhi_6he[3]:
    if abs(Gan.index(gans[3]) - Gan.index(gans[2])) == 1:
        print("日时干邻支合，形成连珠得合：这种格局通常预示婚姻美满，子女优秀，但与事业成就关系不大。")
        
for i,item in enumerate(zhis):
    if item == me_ku:
        if gan_shens[i] in ('才','财'):
            print("财坐劫库：这种格局可能导致财运不稳，易有破财之象。建议在理财方面要特别谨慎。")
            
if zhi_6chong[3] and  gans[3] == me:
    print("日时天比地冲：对于女性，可能意味着家庭生活较为辛劳；对于男性，可能在艺术或宗教方面有特殊的才能或兴趣。")
    
if zhi_xing[3] and  gan_ke(me, gans[3]):
    print("日时天克地刑：这种格局可能意味着难以继承家业，需要自立发展，但可能缺乏长久稳定性。建议培养独立自主的能力。")
    
if (cai,yin_lu) in zhus and (cai not in zhi_shens2):
    print("浮财坐印禄：这种格局可能预示家族财富难以继承，且自身财运也不稳定。建议努力学习理财技能，谨慎处理财务问题。")
    
    
for i in range(3):
    if is_yang():
        break
    if zhi_xing[i] and zhi_xing[i+1] and gan_ke(gans[i], gans[i+1]):
        print("阴日主天克地刑：这种格局可能导致人际关系较为孤独。对于婚姻，可能会经历多次婚姻或感情波折。建议多关注人际交往，培养稳定的感情关系。")


# 建禄格
if zhi_shens[1] == '比':
    all_ges.append('建')
    print("命局中出现建禄格：这种格局最好天干有财官。如果官杀不成格，性格可能较为任性，且有兄弟。在财务方面既有争财也有理财的双重性格。")
    print("建议：如果创业，独自经营可能更好；如果合伙，需要建立完善的财务制度。")
    if gan_shens[0] in '比劫':
        print("\t建禄年透比劫，可能不利，需要注意克制自我，多与他人合作。")
    elif '财' in gan_shens and '官' in gan_shens:
        print("\t建禄财官双透，这是很好的格局，预示事业和财运都有良好发展。")
    if me in ('甲','乙'):
        print("\t甲乙日主的建禄格：如果四柱劫财多，可能缺乏祖业，不利于婚姻，财运不稳定。性格可能较为浮夸，做事不够踏实。乙日主如果财官多则较为有利。")
        print("\t对于甲日主，壬申时较好；对于乙日主，辛巳时较好。")

    if me in ('丙'):
        print("\t丙日主的建禄格：己亥时较为有利。")        
    if me in ('丁'):
        print("\t丁日主的建禄格：对于男性，可能会影响到三次婚姻；对于女性，可能会影响到一次婚姻。如果财官多则较为有利。庚子时较好。")
    if me in ('戊'):
        print("\t戊日主的建禄格：如果四柱无财，可能不利于婚姻和家庭。如果与申子辰相合，可能子息较晚，有两个子女。甲寅时较好。")       
    if me in ('己'):
        print("\t己日主的建禄格：即使官财出干成格，婚姻也可能较晚。偏财、杀印成格较为有利。乙丑时较好。")    
    if me in ('庚'):
        print("\t庚日主的建禄格：上半月出生可能较难继承家业，下半月相对较好。财格比官杀格更有利。丙戌时较好。")   
    if me in ('辛'):
        print("\t辛日主的建禄格：如果干透劫财，可能婚姻较晚且财运较弱。丁酉时较好。")      
    if me in ('壬'):
        print("\t壬日主的建禄格：戊申时较好。")  
    if me in ('癸'):
        print("\t癸日主的建禄格：己亥时较好。")      

        
# 甲分析 

if me == '甲':
    if zhis.count('辰') > 1 or zhis.count('戌') > 1:
        print("甲日：辰或戌多，性格可能急躁，不易忍耐。")
    if zhis[2] == '子':
        print("甲子日：调候需要火元素。")
    if zhis[2] == '寅':
        print("甲寅日：具有主见，需要财官旺的地支来支持。")        
    if zhis[2] == '辰':
        print("甲辰日：印库，性格温和且有实权。")   
    if zhis[2] == '午':
        print("甲午日：一生有财，调候需要水元素。")        
    if zhis[2] == '戌':
        print("甲戌日：自坐伤官，不易生财，为人仁善。")      
        
if me in ('庚', '辛') and zhis[1] == '子' and zhis.count('子') >1:
    print("冬金子月，再有一子字，可能出现孤克现象。")  
    

## 比肩分析
if '比' in gan_shens:
    print("\n----比肩分析----")

    print("比肩：同性相斥。可能不太喜欢自己。常常反思是否有错误。做事缺乏持久性，最多坚持三五年。容易散财，月上比肩，做事没有定性，不太看重钱，感情不持久。不易怀疑他人，心地善良。善意好心可能引起麻烦。年上比肩问题不大。")
    
    if gan_shens[0] == '比' and gan_shens[1] == '比':
        print("比肩年月天干并现：可能不是长子/长女，出身平常。性格端庄，有自己的思想；不太重视钱财,话多不能守秘密。30岁以前是非小人可能较多。")

    if gan_shens[1] == '比' and '比' in zhi_shen3[1]:
        print("月柱干支比肩：感情丰富。30岁以前可能经济紧张。")
        
    if gan_shens[0] == '比':
        print("年干比：上面可能有兄或姐，出身一般。")
        
    if zhi_shens[2] == '比':
        if options.n:
            print("坐比透比:夫妻关系可能不和睦")  
                
        
    if gan_shens.count('比') > 1:
        print("""可能存在自我排斥，易后悔、举棋不定、匆促决定而有失；倾向于群策群力，自己决策容易孤注一掷，小事谨慎，大事决定后不再重复考虑。
有自己的思想、注重外表，注意细节，喜欢小孩。
难以保守秘密，不适合多言；
地支有根，一生小是非可能不断。没官杀制，可能缺乏耐心。""")
    
                
    # 比肩过多
    if shens2.count('比') > 2 and '比' in zhi_shens:
        print('''比肩过多：
        对子女的爱可能超过配偶；容易否定配偶。 另一种说法：有理想、自信、贪财、不惧内。可能有多段婚姻。
        兄弟之间缺乏帮助。夫妻有时不太和谐。好友知交相处不会很久。
        即使成好格局，也是劳累命，事必躬亲。除非有官杀制服。感情可能烦心。
        善意多言，引无畏之争；难以保守秘密，不适合多言；易犯无事忙的自我表现；不好意思拒绝他人;累积情绪而突然放弃。
        比肩过多，可能有帮助配偶事业的运势，多协助对方的事业，多提意见，偶尔有争执，问题也不大。感情可能啰嗦
        对人警惕性低，乐天知命;情感过程多有波折
        ''') 
        
        if (not '官' in shens) and  (not '杀' in shens):
            print("比肩多，四柱无正官七杀，性情可能急躁。")            
            

        if '劫' in gan_shens:
            print("天干比劫并立，比肩地支专位，感情丰富，可能遇到感情纠纷。")    
            
        if gan_shens[0] == '比':
            print("年干为比，不是长子，父母缘较薄，可能晚婚。")  
            
        if gan_shens[3] == '比':
            print("时干为比，如日时地支冲，可能对配偶不利，或为配偶辛劳，九流艺术、宗教则关系不大。")              
            
        if gan_shens[1] == '比':
            if zhi_shens[1] == '食':
                print("月柱比坐食，易得贵人相助。")
            if zhi_shens[1] == '伤':
                print("月柱比坐伤，一生只有小财气，难富贵。")    
            if zhi_shens[1] == '比':
                print("月柱比坐比，可能来自单亲家庭，第一段婚姻可能不能到头。地支三合或三会比，天干2比也如此。")
            if zhi_shens[1] == '财':
                print("月柱比坐财，可能不利配偶，也主父母身体不佳。因亲友、人情等招财物的无谓损失。")      
            if zhi_shens[1] == '杀':
                print("月柱比坐杀，性格稳重。")                   
        
        
    for seq, gan_ in enumerate(gan_shens):
        if gan_ != '比':
            continue
        if zhis[seq] in  empties[zhus[2]]:
            print("比肩坐空亡，可能不利父亲与配偶。年不利父，月不利父和配偶，在时则没有关系。")
        if zhi_shens[seq] == '比':
            print("比坐比-平吉：与官杀对立，无主权。养子：克偏财，泄正印。吉：为朋友尽力；凶：受兄弟朋友拖累。父缘分薄，自我孤僻，可能迟婚")   
        if zhi_shens[seq] == '劫':
            print("比肩坐劫:夫妻关系可能不和睦。")     
            print("比坐劫-大凶：为忌亲友受损，合作事业中途解散，与配偶不合。如年月3见比，父缘薄或已死别。")   
            if ten_deities[gans[seq]][zhis[seq]] == '绝' and seq < 2:
                print("比肩坐绝，兄弟不多，或者很难谋面。戊己和壬癸的准确率偏低些。")   
        if zhi_shens[seq] == '财':
            print("比肩坐财：因亲人、人情等原因引起无谓损失。")  
        if zhi_shens[seq] == '杀':
            print("比肩坐杀:性格稳重。")    
        if zhi_shens[seq] == '枭':
            print("比肩坐偏印：三五年发达，后面守成。")    
        if zhi_shens[seq] == '劫' and Gan.index(me) % 2 == 0:
            print("比肩坐阳刃：父亲可能先亡，基于在哪柱判断时间。在年不利父，在其他柱位可能有刀伤、车祸、意外灾害。")    
        if zhi_shens[seq] in ('劫','比') and'劫' in gan_shens:
            print("天干比劫并立，比肩又坐比劫，个性可能较强，不易协调。")   
        if  zhi_xing[seq]:
            print("比肩坐刑(注意不是半刑)，幼年可能艰苦，白手自立长。")
            if zhi_shens[seq] == '劫':
                print("比肩坐刑劫,兄弟可能不合、也可能与配偶分居。")      
        if zhi_6chong[seq]:
            print("比肩冲，手足可能不和，基于柱定时间。个性可能较强，可能因任性引发困难之事。")                




if zhi_shens[2] == '比':
    print("日支为比肩：对家务事有家长式领导；钱来得不容易且有时有小损财。自我意识强，如有刑冲，不喜归家！")
if zhi_shens[3] == '比':
    print("时支为比肩：子女为人公正倔强、行动力强，能得资产。")    
if '比' in (gan_shens[1],zhi_shens[1]):
    print("月柱有比肩：三十岁以前难有成就。性格冒进、不稳定。恋爱关系不持久、大男子主义。")
if '比' in (gan_shens[3],zhi_shens[3]):
    print("时柱有比肩：与亲人意见不合。")

if shens.count('比') + shens.count('劫') > 1:
    print("比劫大于两个，男性可能遇到感情阻碍、事业起伏不定。")



# 日坐禄   
if me_lu == zhis[2]:
    
    if zhis.count(me_lu) > 1:
        if yin_lu in zhis:
            if '比' in gan_shens or '劫' in gan_shens:
                
                print("双禄带比印（专旺）、孤克之命。比论孤，劫论凶。比禄印劫不可合见四位")
                
    if zhi_6he[2] and '比' in gan_shens:
        if yin_lu in zhis:   
            print("透比，坐禄六合，有印专旺：可能遇到官非、残疾。")
          
        print("透比，坐禄六合，如地支会印，恐有不利。")    
        

    if (zhi_xing[3] and gan_he[3] and gan_shens[3] == '财') or (zhi_xing[2] and gan_he[2] and zhi_xing[1] and gan_he[1] and gan_shens[1] == '财'):
          
        print("日禄与正财干合支刑：可能克妻子，即便是吉命，也可能无天伦之乐。")    
        
if zhis.count(me_lu) > 2:
    print("禄有三个，可能孤独。")
    
    
if zhis[3] == me_ku:
    if '财' in gan_shens or '才' in gan_shens:
        print("时支日库，透财：性格清高，可能从事艺术或非主流行业。")
        
    if piancai_lu == zhis[2]:
        print("时支日库，坐偏财：吉祥近贵，但亲属关系可能淡薄。")
    


    
# 时坐禄   
if me_lu == zhis[3]:
    if '伤' in gan_shens and '伤' in zhi_shens2:   
        print("时禄，伤官格，晚年可能吉利。")
    if '杀' == gan_shens[3]:   
        print("杀坐时禄：为人可能反复不定。")
    
# 自坐劫库
if  zhis[2] == me_ku: 
    if gan_shens[3] == '杀' and '杀' in zhi_shen3[3]:
        print("自坐劫库,时杀格，可能贵重！")  
        
    if gan_shens[3] == '官' and '官' in zhi_shen3[3]:
        print("自坐劫库,正官格，可能孤贵！")   
            
    if zhi_ku(zhis[3], (cai,piancai)):
        print("自坐劫库,时财库，另有刃禄孤刑艺术，无者可能辛劳！") 
        
    if gan_shens[3] == '财' and '财' in zhi_shen3[3]:
        print("自坐劫库，时正财格，可能有双妻或丧妻之象。")
        
    if (yin, me_lu) in zhus:
        print("自坐劫库,即便吉利，也可能有猝亡之险。")


# 劫财分析
if '劫' in gan_shens:
    print("\n----劫财分析----")

    print("劫财扶助，无微不至。劫财多者谦虚之中带有傲气。凡事先理情，而后情理。先细节后全局。性格刚强、精明干练、女命不适合干透支藏。")
    print("务实，不喜欢抽象性的空谈。不容易认错，比较倔强。有理想，但是不够灵活。不怕闲言闲语干扰。不太顾及别人面子。")
    print("合作事业可能有始无终。过于重视细节。做小领导还是可以的。有志向，自信。有杀或食神透干可解所有负面。女命忌讳比劫和合官杀，可能因任性引发困难之事。")
    
    if gan_shens[0] == '劫' and gan_shens[1] == '劫':
        print("年月天干都是劫财：喜怒容易形于色，三十岁以前可能经历一次大失败。过度自信，精明反被精明误。")

    if gan_shens[1] == '劫':
        if  '劫' in zhi_shen3[1]:
            print("月柱干支都是劫财：可能与父亲缘分薄，三十岁以前性格任性，早婚需防分手，自我精神压力可能极重。")
        if  zhis[1] == cai_lu and zhis.count(yin_lu) > 1:
            print("月干劫财：月支财禄，如地支有两个旺印，旺财不敌，可能有官非、刑名意外。")            
          
        
    if shens2.count('劫') > 2:
        print('劫财过多, 婚姻可能不顺')
    if zhi_shens[2] == '劫':
        print("日坐劫财，透天干。在年柱可能父亲早亡，在月柱夫妻关系可能不好。比如财产互相防范；鄙视对方；自己决定，哪怕对方不同意；老夫少妻；身世有差距；斤斤计较；敢爱敢恨的后遗症\n\t以上多针对女性。男性一般可能有双妻。天干有杀或食神可解。") 
            
if zhus[2] in (('壬','子'),('丙','午'), ('戊','午')):
    print("日主专位劫财，壬子和丙午，可能晚婚。不透天干，一般是眼光高、独立性强。对配偶可能不利，互相轻视；若刑冲，做事立场不明可能遭嫉妒，但不会有大灾。女性婚后通常还有自己的事业,能办事。") 
if ('劫','伤') in shen_zhus or ('伤','劫',) in shen_zhus:
        print("同一柱中，劫财、阳刃伤官都有，外表可能华美，富屋穷人，婚姻可能不稳定，富而不久；年柱不利家长，月柱不利婚姻，时柱不利子女。伤官可能带来狂妄。")      

if gan_shens[0] == '劫':
    print("年干劫财：家运可能不济。可能克父，如果坐劫财，通常少年可能失父；反之要看地支劫财根在哪一柱子。")
        
if '劫' in (gan_shens[1],zhi_shens[1]):
    print("月柱有劫财：容易孤注一掷，三十岁以前可能难稳定。男性早婚可能不利。")
if '劫' in (gan_shens[3],zhi_shens[3]):
    print("时柱有劫财：只要不是掌握经济大权还好。")   
if zhi_shens[2] == '劫':
    print("日支劫财：男性可能克妻，一说是家庭有纠纷，对外尚无重大损失。如再透月或时天干，可能有严重内忧外患。")
    
if '劫' in shens2 and  '比' in zhi_shens and '印' in shens2 and not_yang():
    print("阴干比劫印齐全，可能单身，适合入道！")
    
if zhi_shens[0] == '劫' and is_yang(): 
    print("年支阳刃：可能得不到长辈福；不知足、施恩反怨。")
if zhi_shens[3] == '劫' and is_yang(): 
    print("时支阳刃：可能与妻子不和，晚年无结果，四柱再有比刃，可能有疾病与外灾。")
    
# 阳刃格        
if zhi_shens[1] == '劫' and is_yang():
    all_ges.append('刃')
    print("阳刃格：喜七杀或三四个官。甲戊庚逢冲多祸，壬丙逢冲还好。")  
    if me in ('庚', '壬','戊'):
        print("阳刃'庚', '壬','戊'忌讳正财运。庚逢辛酉凶，丁酉吉，庚辰和丁酉六合不凶。壬逢壬子凶，戊子吉；壬午和戊子换禄不凶。")
    else:
        print("阳刃'甲', '丙',忌讳七杀运，正财偏财财库运还好。甲：乙卯凶，辛卯吉；甲申与丁卯暗合吉。丙：丙午凶，壬午吉。丙子和壬午换禄不凶。")
        
    if zhis.count(yin_lu) > 0 and gan_shens[1] == '劫':
        print("阳刃格月干为劫财：如果印禄位有两个，过旺，可能有凶灾。不透劫财，有一印禄,食伤泄气，仍然可以吉利。")
        
    if gan_shens[3] == '枭' and '枭' in zhi_shen3[3]:
        
        print("阳刃格:时柱成偏印格，可能贫穷、短命、带疾。")
                
        
if zhi_shens.count('劫') > 1 and Gan.index(me) % 2 == 0:
    if zhis.day == yin_lu:
        print("双阳刃，自坐印专位：可能刑妻、妨子。可能凶终、官非、意外灾害。")
        
if zhi_shens[1:].count('劫') > 0 and Gan.index(me) % 2 == 0:
    if zhis.day == yin_lu and ('劫' in gan_shens or '比' in gan_shens):
        print("阳刃，自坐印专位，透比或劫：可能刑妻。")
        
if zhis[2] in (me_lu,me_di) and zhis[3] in (me_lu,me_di):
    print("日时禄刃全，如没有官杀制，可能刑伤父母，妨碍妻子。")
    
for seq, gan_ in enumerate(gan_shens):
    if gan_ != '劫':
        continue    
    if zhis[seq] in (cai_lu, piancai_lu):
        print("劫财坐财禄，如逢冲，可能大凶。先冲后合和稍缓解！")
        
        if zhi_shens[seq] == '财' and zhi_6he[seq]:
            print("劫财坐六合财支：可能有久疾暗病！")

if gan_shens[1] == '劫' and zhis[1] in (cai_lu, piancai_lu)  and zhis.count(yin_lu) > 1 and '劫' in gan_shens:
    print("月干劫财坐财禄，有两个印禄，劫财透出，财旺也败：可能有官非、刑名、意外灾害！")
    
# 自坐阳刃
if '劫' in zhi_shen3[2] and is_yang() and zhis[2] in zhengs:  
    if zhis[3] in (cai_lu, piancai_lu):
        print("坐阳刃,时支财禄，吉祥但是妻子性格可能不受管制！")
    if zhi_ku(zhis[3], (cai, piancai)):
        print("坐阳刃,时支财库，名利可能时进时退！")
            
    if gan_shens[3] == '杀' and '杀' in zhi_shen3[3]:
        print("坐阳刃,时杀格，可能有贵人提携而富贵！")
  
 
# 偏印分析    
if '枭' in gan_shens:
    print("----偏印分析----")
    print("偏印格特点：")
    print("1. 最佳组合：偏印在前，偏财在后，有天月德贵人更佳。")
    print("2. 注意事项：忌讳倒食，但坐绝地支时无此影响。")
    print("3. 一般特征：")
    print("   - 需要身旺才能发挥作用")
    print("   - 见官杀未必有利")
    print("   - 喜伤官、财")
    print("   - 忌日主无根")
    print("   - 女命重视兄弟姐妹关系")
    print("   - 男命六亲关系较疏远")
    print("4. 不利情况：干支有冲、合、刑，或地支是偏印的绝位")
    
    if (gan_shens[1] == '枭' and '枭' in zhi_shen3[1]):        
        print("月柱偏印重叠：福薄慧多，青年时期可能较为孤独，有文艺或宗教倾向。")
        
    if zhi_shens2.count('枭') > 1:
        print("偏印根透两柱：可能较为孤独，感情生活可能有波折。做事可能有始无终，女性需注意维护声誉。")

    if  zhi_shens2.count('枭'):
        print("偏印成格：最佳搭配是生财或配印。尤其喜欢同时有偏财成格，偏印在前，偏财在后。需要避免日柱和时柱坐实比劫或阳刃。")
        all_ges.append('枭')
              
    if shens2.count('枭') > 2:
        print("偏印过多的影响：")
        print("1. 性格可能较为孤僻，表达方式含蓄")
        print("2. 可能有悲观倾向")
        print("3. 可能具有艺术天赋")
        print("4. 做事可能有始无终")
        print("5. 女性需要注意维护声誉")
        print("6. 对兄弟姐妹关系较好")
        print("7. 男性可能因才干受到子女尊敬")
        print("8. 女性偏印多，可能子女较少")
        print("改善方法：有偏财和天月德贵人可以改善这些特征。")
        
        if '伤' in gan_shens: 
            print("女命偏印多且与伤官同现，需要注意婚姻和子女关系。有偏财和天月德贵人可以改善。")
        
    if gan_shens.count('枭') > 1:
        print("天干有两个偏印：可能会影响婚姻，如迟婚或独身倾向。若有三个偏印，家族人口可能较少。")
        
    if shen_zhus[0] == ('枭', '枭'):
        print("年柱偏印双透：可能不利于长辈。可能是领养、庶出或同父异母等情况。")

    if zhi_shen3[1] == ['枭']:
        print("月支专位偏印：可能有特殊手艺。若坐衰地支，外表可能平平无奇。")
        
    
for seq, zhi_ in enumerate(zhi_shens):
    if zhi_ != '枭' and gan_shens[seq] != '枭':
        continue   

    if ten_deities[gans[seq]][zhis[seq]] == '绝':
        print("偏印坐绝，或天干偏印坐绝地支：可能难以施展才能，付出努力可能得不到相应回报。")    

    if  gan_shens[seq] == '枭':
        if '枭' in zhi_shen3[seq] :
            print("干支都有偏印：可能影响婚姻，福分可能较薄。")  

        if '比' in zhi_shen3[seq] :
            print("偏印坐比：可能劳心劳力，容易遇到暗中的阻碍。")   

        if zhi_shens[seq] == '伤':
            print("偏印坐伤官：需要注意婚姻和子女关系。")        

    
if zhi_shens[3]  == '枭' and gan_shens[0]  == '枭':
    print("偏印在年干和时支：可能长期受到家庭影响。")
    
if '枭' in (gan_shens[0],zhi_shens[0]):
    print("偏印在年柱：可能出身普通家庭；可能有宗教素养，不太喜欢享乐，第六感可能较强。")
if '枭' in (gan_shens[1],zhi_shens[1]):
    print("偏印在月柱：可能聪慧但福分较浅，有舍己为人的倾向。")
    if zhi_shens[1]  == '枭' and zhis[1] in "子午卯酉":
        print("偏印专位在月支：可能适合音乐、艺术、宗教等领域。22-30岁之间可能确定职业方向。")
        if gan_shens[1] == '枭':
            print("月柱干支皆偏印且专位：可能聪慧但福分较浅，不太追求名利。")    
if '枭' in (gan_shens[3],zhi_shens[3]):
    if(options.n):
        print("偏印在时柱：男性50岁前可能奠定基础，晚年可能享清福。")
    else:
        print("偏印在时柱：女性可能与后代分居。")     
if zhi_shens[2] == '枭' or zhis.day == xiao_lu:
    print("偏印在日支：家庭生活可能较为平淡")
    if zhi_6chong[2] or zhi_xing[2]:
        print("偏印在日支且有冲刑：可能较为孤独。")
    if zhus[2] in (('丁','卯'),('癸','酉')):
        print("日柱专位偏印（丁卯或癸酉）：婚姻可能不顺。若有刑冲，可能因性格而引发争端，甚至意外伤害。")   
    if zhis[3] == me_jue:
        print("日坐偏印，时支绝：可能缺乏亲人依靠，生活可能较为贫乏。")  
    
    if '枭' in gan_shens and is_yang() and zhis.time == me_di:
        print("日坐偏印成格，时支阳刃：可能不利于婚姻，自身可能有健康问题。")  
    if gan_shens[3] == zhi_shens[3] == '劫':
        print("日坐偏印，时干支劫：可能因自身性格而引发不利情况。")
        
    if zhis.count(me_di) > 1 and is_yang():
        print("日坐偏印，地支双阳刃：性格可能有极端倾向。")

        
if zhis.time == xiao_lu:
    if zhi_shens[3] == '枭' and '枭' in gan_shens:
        if '财' in shens2 or '才' in shens2:
            print("时支偏印成格有财：可能因机智而引发不利情况。")        
        else:
            print("时支偏印成格无财：性格可能较为顽固，可能引发不利情况。")
        

# 印分析    
if '印' in gan_shens:
    if '印' in zhi_shens2:
        print("\n----正印分析----")
        print("正印成格特点：")
        print("1. 有利条件：官杀、身弱")
        print("2. 不利条件：财克印")
        print("3. 其他特征：")
        print("   - 合印留财，可能见利忘义")
        print("   - 透财官杀可以通关，或印生比劫")
        print("   - 合冲印若无其他格局可能破格")
        print("   - 日主强则不利，有禄刃一支可以通过食伤泄气来改善")
        all_ges.append('印')
        
    if (gan_shens[1] == '印' and '印' in zhi_shen3[1]):    
        if(options.n):
            print("月柱正印重叠：女性可能晚婚，若月支有阳刃可能会离婚。通常能独立谋生，可能是有修养的才女。")

    if gan_shens[0] == '印' :        
        print("年干有正印：可能出身较好的家庭。")
            
    if shens2.count('印') > 2:
        print("正印较多的特征：")
        print("1. 聪明有谋略，性格较为含蓄")
        print("2. 不害人，识时务")
        print("3. 正印不怕日主弱，反而怕日主太强")
        print("4. 日主强且正印多，可能较为孤寂，不善理财")
        if(options.n):
            print("5. 男性可能对妻子影响较大，子嗣可能较少")
        else:
            print("5. 女性可能对母亲影响较大")
    for seq, gan_ in enumerate(gan_shens):
        if gan_ != '印':
            continue   
        if ten_deities[gans[seq]][zhis[seq]] in ('绝', '死'):
            if seq <3:
                print("正印坐死绝，或天干正印地支有冲刑，可能不利于母亲。（时柱不计）")   
        if zhi_shens[seq] == '财':
            print("男性正印坐正财，夫妻关系可能不佳。月柱正印坐正财专位，可能会离婚。在时柱，50多岁后婚姻可能趋于稳定。")   
        if zhi_shens[seq] == '印':
            if(options.n):
                print("正印坐正印专位：可能过于自信。特点包括务实，能放得下。男性可能适合艺术，经商则可能较为孤僻，不易积累财富。")          
            else:
                print("正印坐正印专位：可能过于自信。特点包括务实，能放得下。女性可能晚婚。母亲可能长寿；女性可能晚育，头胎可能有风险。女性若四柱没有官杀，婚姻可能较差。")          
        if zhi_shens[seq] == '枭' and len(zhi5[zhis[seq]]) == 1:
            print("正印坐偏印专位：可能有多种职业；家庭可能不太和睦：亲人可能有健康问题或特殊嗜好。子女可能较晚；财务可能复杂。行为可能表里不一。")   
            
        if zhi_shens[seq] == '伤':
            print("正印坐伤官：可能适合清高的职业。可能不太适合追逐名利，女性婚姻可能不太顺利。")    
            
        if zhi_shens[seq] == '劫' and me in ('甲','庚','壬'):
            print("正印坐阳刃，可能身心俱疲，工作压力较大。主要指月柱情况。")    
                        
            
    if '杀' in gan_shens and '劫' in zhi_shens and me in ('甲','庚','壬'):
            if(options.n):
                print("正印、七杀、阳刃同时出现：男性可能小病不断，理论强于实践，婚姻可能不佳，可能有非婚生子女，性格细腻对人要求较高。")    
            else:
                print("正印、七杀、阳刃同时出现：女性可能倾向宗教，否则可能独身，性格可能清高，身体可能有隐疾，性格可能较为狭隘缺乏耐心。")    
            
    if '官' in gan_shens or '杀' in gan_shens: 
        print("身弱时官杀和印都透天干，格局较佳。")
    else:
        print("单独正印主秀气、艺术、文才。性格可能较为保守")  
    if '官' in gan_shens or '杀' in gan_shens or '比' in gan_shens: 
        print("正印较多时，天干有比肩，不怕财。天干有官杀也不怕。财不强也没关系。")  
    else:
        print("正印怕财。") 
    if '财' in gan_shens:     
        print("印和财都透天干且都有根，最好先财后印，人生可能较为顺利。先印后财，能力可能不错，但可能多为他人奔波。（主要指男性）") 
       
       
if zhi_shens[1]  == '印':
    if(not options.n):
        print("月支印：女性可能觉得丈夫不如自己，分居可能是常态，自己可能有独立能力。") 
    if gan_shens[1]  == '印':
        if(not options.n):
            print("月干支印：男性可能重视权力胜过名声。")    
        if '比' in gan_shens:
            print("月干支印格，透比，可能有意外损失。")
            
if zhi_shens[2]  == '印':
    if gan_shens[3] == '才' and '才' in zhi_shen3[3]:
        print("日坐印，时偏财格：可能在异乡发展顺利，可能改变信仰或生活方式，家庭可能和睦。") 
        
    if gan_shens[3] == '财' and ('财' in zhi_shen3[3] or zhis[3] in (cai_di, cai_lu)):
        print("日坐印，时正财格：晚年可能发达，妻贤但子女可能不孝顺。") 

            
if zhi_shens[3]  == '印' and zhis[3] in zhengs:
    print("时支专位正印：男性可能终身忙碌。女性的子女可能各居一方，亲情可能较淡薄。")  
    
if gan_shens[3]  == '印' and '印' in zhi_shen3[3]:
    if(not options.n):
        print("时柱正印格：不论男女，老年可能较为辛苦。女性可能到老都要掌控家产。与子女缘分可能较浅。") 
    else:  
        print("时柱正印格：不论男女，老年可能较为辛苦。与子女缘分可能较浅。") 
    
if gan_shens.count('印') + gan_shens.count('枭') > 1:
    if(not options.n):
        print("印枭在年干月干：性格可能较为迂腐，可能故作清高，女性可能晚育，婚姻可能有阻碍。印枭在时干，可能不利于母子关系，性格可能不太和谐。")  
    

if zhis[1] in (yin_lu, xiao_lu) :
    print("印或枭在月支：可能有压制丈夫的心态。")  
    
if zhis[3] in (yin_lu, xiao_lu) :
    print("印或枭在时支：可能对配偶或子女关系有影响。")  
 
# 坐印库   
if zhi_ku(zhis[2], (yin, xiao)):
    if shens2.count('印') >2:
        print("日坐印库，又成印格：印过旺，需要注意可能的意外伤害。")
    if zhi_shens[3] == '劫':
        print("日坐印库，时支阳刃：如果有比肩、禄、印可能较贫困，没有则较吉利。")  

if zhis.count("印") > 1:
    if gan_shens[1] == "印" and zhi_shens[1] == "印" and '比' in gan_shens:
        print("月干支印，印旺，透比：可能兴旺不久，有损失的可能。") 
        
if zhis[1] == yin_lu:
    if ('财' in gan_shens and '财' in zhi_shens) or ('才' in gan_shens and '才' in zhi_shens):
        print("月支正印专位，成财格：可能在异乡发展顺利，可能改变信仰或生活方式，家庭可能和睦。") 
   
        
# 偏财分析    
if '才' in gan_shens:
    print("\n----偏财分析----")
    print("偏财出现在天干：")
    print("- 财富可能被外人看到，但实际财力可能不及表面的一半")
    print("- 可能经常帮助他人，超过自己的能力")
    print("- 如果与天月德贵人同天干，可能有声名远扬的父亲或聪慧的红颜知己")
    print("- 喜欢奉承，善于享受")
    print("- 讲究原则，不拘小节")
    
    if '才' in zhi_shens2:
        print("财格基础较好，但需要注意:")
        print("- 比劫需用食伤通关或官杀制")
        print("- 身弱有比劫仍需用食伤通关")
        print("- 如果时柱坐实比劫，晚年可能破产")
        all_ges.append('才')
    
    if ('比' in gan_shens or '劫' in gan_shens) and gan_shens[3] == '才':
        print("年月有比劫，时干透出偏财：可能祖业凋零后白手起家")
        print("如有刑冲，可能是千金散尽还复来的情况")
    
    if '杀' in gan_shens and '杀' in zhi_shens:
        print("偏财和七杀并位，且地支有根：")
        print("- 父子可能外合心不合")
        print("- 如在日时，可能遇到难相处的伴侣")
        
    if zhi_shens[0] == '才':
        print("偏财根透年柱：家世可能良好，且能承受祖业")
        
    for seq, gan_ in enumerate(gan_shens):
        if gan_ != '才':
            continue
        if '劫' in zhi_shen3[seq] and zhis[seq] in zhengs:
            print("偏财坐阳刃劫财：可能与父缘薄，幼年家境贫寒，或父亲早逝")   
        if get_empty(zhus[2],zhis[seq]) == '空':
            print("偏财坐空亡：财运和官运可能较差")                    
                
if shens2.count('才') > 2:
    print("偏财多的特征：")
    print("- 为人慷慨，看淡得失")
    print("- 花钱不易后悔，性格乐观")
    print("- 生活习惯可能颠倒，适应能力强")
    print("- 有团队精神，容易得到女性欢心")
    print("- 小事很少失信，乐善好施")
    print("- 女命偏财，可能较听父亲的话")
    print("- 时柱偏财的女性，善于理财，中年后可能有自己的事业")

if (zhi_shens[2] == '才' and len(zhi5[zhis[2]]) == 1) or (zhi_shens[3] == '才' and len(zhi5[zhis[3]]) == 1):
    print("日时地支坐专位偏财，且无刑冲：")
    print("- 时干不是比劫")
    print("- 大运也没有比劫刑冲")
    print("- 晚年可能发达")
    
    
# 财分析    

if (gan_shens[0] in ('财', '才') and gan_shens[1] in ('财', '才')) or (gan_shens[1] in ('财', '才') and ('财' in zhi_shen3[1] or '才' in zhi_shen3[1])):
    print("\n----正财分析----")
    print("财或偏财在年月重叠：")
    if(options.n):
        print("- 女性可能是职业妇女，有理财和办事能力")
    print("- 理财能力可能影响婚姻")
    print("- 男性可能有双妻现象")
    

if '财' in gan_shens:
    if '财' in zhi_shens2:
        all_ges.append('财')
        
    if is_yang():        
        print("男命日主合财星：夫妻可能恩爱")
        print("如果有争合或天干有劫财，可能有双妻现象")
    if '财' in zhi_shens:
        print("财格基础较好，但需要注意:")
        print("- 比劫需用食伤通关或官杀制")
        print("- 身弱有比劫仍需用食伤通关")
        
    if '官' in gan_shens:
        print("正官正财并行透出：如果身强，可能出身书香门第")
    if '官' in gan_shens or '杀' in gan_shens:
        print("官或杀与财并行透出：")
        if(options.n):
            print("- 女性可能压制丈夫")
            print("- 财生官杀，丈夫可能压力较大")
    if gan_shens[0] == '财':
        print("年干正财为喜用：可能出身富裕家庭，但可能不利母亲")
    if '财' in zhi_shens:
        if '官' in gan_shens or '杀' in gan_shens:
            print("男命财旺透官杀：妻子可能不满意丈夫")
    if gan_shens.count('财') > 1:
        print("天干两正财：")
        print("- 财源可能较多，可能同时经营多种生意")
        print("- 喜欢赶潮流，容易随大流")
        print("- 有时可能会做自己不熟悉的生意")
        if '财' not in zhi_shens2:
            print("正财多而无根：财运可能虚而不实，重财不一定富")
            
for seq, gan_ in enumerate(gan_shens):
    if gan_ != '财' and zhis[seq] != '财':
        continue   
    if zhis[seq] in day_shens['驿马'][zhis.day] and seq != 2:
        print("女命柱有财+驿马：可能有动力持家")
    if zhis[seq] in day_shens['桃花'][zhis.day] and seq != 2:
        print("女命柱有财+桃花：可能不太吉利")        
    if zhis[seq] in empties[zhus[2]]:
        print("财坐空亡：财运可能不持久")    
    if ten_deities[gans[seq]][zhis[seq]] in ('绝', '墓'):
        print("男命财坐绝或墓：可能不利婚姻")
            
if shens2.count('财') > 2:
    print("正财多的特征：")
    print("- 为人端正，有信用")
    print("- 性格简朴稳重")
    if '财' in zhi_shens2 and (me not in zhi_shens2):
        print("正财多而有根，日主不在生旺库：身弱可能惧内")   
        
if zhi_shens[1] == '财' and options.n:
    print("女命月支正财：可能有务实的婚姻观")
    
if zhi_shens[1] == '财':
    print("月令正财，无冲刑：")
    print("- 可能有贤内助")
    print("- 但母亲与妻子可能不和")
    print("- 生活可能简朴，多为理财人士")
if zhi_shens[3] == '财' and len(zhi5[zhis[3]]) == 1:
    print("时支正财：可能有两个儿子")
if zhus[2] in (('戊','子'),) or zhus[3] in (('戊','子'),):
    print("日支或时支戊子：")
    print("- 可能得勤俭的配偶")
    print("- 如果日时支正财又透正官，中年以后可能发达，独立富贵") 
    
if zhus[2] in (('壬','午'),('癸','巳'),):
    print("日坐财官印：如果四柱没有刑冲，大吉") 
    
if '财' == gan_shens[3] or '财' == zhi_shens[3]:
    print("时柱有正财：")
    print("- 可能口快心直，不喜拖泥带水")
    print("- 如有刑冲则可能浮躁")
    print("- 如无刑冲，可能有美妻佳子") 

if (not '财' in shens2) and (not '才' in shens2):
    print("四柱无财：")
    print("- 即便逢财运，也可能是虚名虚利")
    print("- 男命可能晚婚")
    
if zhis.day in (cai_lu, cai_di):
    if (zhi_shens[1] == '劫' or zhi_shens[3] == '劫' ) and Gan.index(me) % 2 == 0:
        print("自坐财禄，月支或时支为阳刃：")
        print("- 可能有凶险")
        print("- 无冲可能是非多")
        print("- 有冲刑可能主病灾")   
    if ('劫' in zhi_shens ) and Gan.index(me) % 2 == 0 and '劫' in gan_shens :
        print("自坐财禄，透劫财，有阳刃：可能刑克配偶") 
    if me in ('甲', '乙') and ('戊' in gans or '己' in gans):
        print("火土代用财，如果透财：可能多成多败，早年灰心") 
        
    if gan_shens[3] == '枭':
        print("财禄时干偏印：可能亲属关系较为疏远")
        if '枭' in zhi_shen3[3]:
            print("财禄时干偏印格：")
            print("- 财运可能较好")
            print("- 但人丁可能较少")
            print("- 性格可能偏向艺术化")
            
    if zhis[3] == yin_lu:
        print("坐财禄，时支印禄：人生可能先难后易")
                  
     
if (gan_he[3] and gan_shens[3] == '财' and jin_jiao(zhis[2], zhis[3])) or (gan_he[2] and gan_he[1] and gan_shens[1] == '财' and jin_jiao(zhis[1], zhis[2])):
    print("日主合财且进角合：一生可能吉祥、平安有裕")    
    
    
if zhis.day == cai_lu or zhi_shens[2] == '财':
    if gan_shens[3] == '枭' and ('枭' in zhi_shen3[3] or zhis[3] == xiao_lu):
        print("日坐财，时偏印格：")
        print("- 可能在他乡有所成就")
        print("- 为人可能敦厚")
    if zhi_6chong[2] or zhi_xing[2]:
        print("日坐财，有冲或刑：财运可能较好，但可能有疾病")    

        
if gan_shens[3] == '财' and zhi_ku(zhis[3], (me,jie)):
    print("正财坐日库于时柱:")
    print("- 可能较为孤独")
    print("- 可能难为父母")
    print("- 但事业可能有成就")

# 自坐财库    
if zhis[2] == cai_ku: 
    if zhis[3] == me_ku:
        print("自坐财库,时劫库：可能有财但较为孤单")
        
    if zhis[2] == zhis[3]:
        print("自坐财库,时坐财库：")
        print("- 妻子可能有灾")
        print("- 妻子可能反被妾制服")
    
    if gan_shens[3] == '杀' and '杀' in zhi_shen3[3]:
        print("自坐财库,时杀格：财生杀，可能有凶险")    
    
# 时坐财库    
if zhi_ku(zhis[3], (cai,piancai)): 
    if '伤' in gan_shens and '伤' in zhi_shens:
        print("时坐财库,伤官生财:")
        print("- 财运可能较好")
        print("- 但体质可能较弱")
        print("- 在旺处可能寿命较短")

if gan_shens[3] == '财' and '财' in zhi_shen3[3]:
    print("时上正财格：不必财旺，可能因妻致富") 
    
    if zhis[3] == me_ku:
        print("时上正财格坐比劫库：可能克妻")
    if zhis[2] == cai_ku:
        print("时上正财格自坐财库：")
        print("- 妻子可能贤良")
        print("- 但可能中年丧妻")
        print("- 续弦也可能较好")

if zhis[3] in (cai_di, cai_lu):
    if gan_he[3]:
        print("时财禄，天干日时双合：可能损妻家财")
    if '伤' == gan_shens[3] and '伤' in zhi_shens2:
        print("时支正财时干伤成格：虽然可能富有，但也可能有刑克")
    if zhi_ku(zhis[1], (shi,shang)) and zhis[3] == cai_lu:
        print("时支正财禄，月支伤入墓：生财可能极为辛勤")
        
if zhis[3] == cai_lu:
    if zhi_xing[3] or zhi_6chong[3]:
        print("时支正财禄有冲刑：")
        print("- 可能得女伴")
        print("- 可能有文学才华和清贵之象")
    if any(zhi_xing[:3]) or any(zhi_6chong[:3]):
        print("时支正财禄,它支有冲刑：")
        print("- 可能刑克配偶")
        print("- 性格可能孤高")
        print("- 可能有艺术天分")
        print("- 可能近贵人")
    if gan_shens.count('财') > 1:
        print("时支正财禄,天干财星多：")
        print("- 可能性格孤雅")
        print("- 可能从事艺术等行业")
        print("- 表面可能风光")



# 官分析    
if '官' in gan_shens:
    print("\n----正官分析----")
    if '官' in zhi_shens2:
        print("官格成立：忌伤官，忌混杂。有伤官时需要财星通关或印星制化。混杂时需要合化或者身官两停。日主弱时不宜扶。")
        all_ges.append('官')
        
        if '比' in gan_shens or '劫' in gan_shens:
            print("官格中有比劫：可能表现为清高或有洁癖的文人气质。")

        if '伤' in gan_shens:
            print("官格中有伤官：可能表里不一。")    
            
        if '财' in gan_shens or '才' in gan_shens:
            print("官格中有财星：有利于聚财。")     
            
        if '印' in gan_shens:
            print("官格中有印星：人品可能清雅。")   
            
        if not ('印' in gan_shens or '财' in gan_shens or '才' in gan_shens):
            print("官星独透成格：性格可能敦厚。")               

        
    if (gan_shens[0] == '官' and gan_shens[1] == '官') or (gan_shens[1] == '官' and '官' in zhi_shen3[1]):
        print("官星在年月重叠：女性可能易离婚，早婚不利。性格可能温和。")
            
    if gan_shens[3] == '官' and len(zhi5[zhis[3]]) == 1:
        print("时柱官星坐专位：男性可能有得力子息。")
    if gan_shens[0] == '官' :
        print("年干为官，身强时可能出身书香门第。")
        if gan_shens[3] == '官':
            print("男命年干、时干都为官，对后代和头胎可能不利。")
    if (not '财' in gan_shens) and (not '印' in gan_shens):
        print("官星独透天干成格，四柱无财或印：可能为老实人。")
    if '伤' in gan_shens:
        print("正官伤官通根透露，又无其他格局：可能不利。尤其是女命，可能异地分居较多，婚姻不美满。")
    if '杀' in gan_shens:
        print("年月干有七杀和偏官：30岁以前婚姻可能不稳定。月时多为体弱多病。")
        
    if '印' in gan_shens and '印' in zhi_shens2 and '官' in zhi_shens2:
        print("官印同根透露，无刑冲合：吉利。")
        if '财' in gan_shens and '财' in zhi_shens2:
            print("财官印同根透露，无刑冲合：更加吉利。")
        
    if gan_shens[1] == '官' in ten_deities[me][zhis[1]] in ('绝', '墓'):
        print("官星在月柱坐墓绝：可能有特殊婚姻或迟婚。如果与天月德同柱，仍然不错。丈夫在库中可能意味着：1. 老夫少妻；2. 不为外人所知的亲密感情；3. 特殊又合法的婚姻。")
    if zhi_shens[1] == '官' and gan_shens[1] == '官':
        print("月柱正官坐正官：可能有婚变。月柱不宜通根。")  

    
    for seq, gan_ in enumerate(gan_shens):
        if gan_ != '官':
            continue   
        if zhi_shens[seq] in ('劫','比') :
            print("天干正官，地支比肩或劫财：亲友之间不适合合作，但适合经营困难的事业。")
        if zhi_shens[seq] == '杀' :
            print("正官坐七杀：男命可能有诉讼之灾。女命婚姻可能不佳。月柱尤其麻烦，可能有两次感情纠纷。年柱不算，时柱影响较轻。")
        if zhi_shens[seq] == '劫' and Gan.index(me) % 2 == 0:
            print("官坐羊刃：可能有力不从心之事。")   
        if zhi_shens[seq] == '印':
            print("官坐印，无刑冲合：吉利")   
        
            
if shens2.count('官') > 2 and '官' in gan_shens and '官' in zhi_shens2:
    print("正官多者：可能有虚名。为人性格温和，比较实在。可按七杀格局看待")
if zhis.day == guan_lu or zhi_shens[2] == '官':
    print("日坐正官专位：女性可能温婉贤淑。")
    if is_yang() and zhis.time == me_di:
        print("日坐正官，时支阳刃：可能先富后败，再东山再起。")
    
if gan_shens.count('官') > 2 :
    print("天干有两个以上官星：女性可能需要照顾弟妹，一生可能为情所困。")   
    

if zhi_shens[1] == '官' and '伤' in zhi_shens2:
    print("月支正官，又成伤官格：可能难成真正夫妻。有实无名。")
    
    
# 杀分析    
if '杀' in gan_shens:
    print("\n----七杀分析----")
    print("七杀格：可能是非多。但对男性有时是贵格。成格需要食神制化，或印星生扶，或身杀两停。")
    if '杀' in zhi_shens2:
        print("杀格：喜食神制化，要食在前，杀在后。阳刃驾杀：杀在前，刃在后。身杀两停：如甲寅日庚申月。杀印相生，忌食神同时成格。")
        all_ges.append('杀')
        
        if '比' in gan_shens or '劫' in gan_shens:
            print("杀格透比或劫：性格可能急躁但有分寸。")

        if '杀' in gan_shens:
            print("杀格透官：可能精明琐屑，不怕脏。")    
            
        if '食' in gan_shens or '伤' in gan_shens:
            print("杀格透食伤：可能外表宁静，内心刚毅。")     
            
        if '印' in gan_shens:
            print("杀格透印：可能圆润、精明干练。")   
        
    if (gan_shens[0] == '杀' and gan_shens[1] == '杀') :
        print("杀星在年干月干重叠：可能不是长子，出身平常，多灾，性格不稳重。")
        
    if (gan_shens[1] == '杀' and '杀' in zhi_shen3[1]):        
        print("杀星在月柱重叠：女性易离婚，其他格局可能一生多病。")
        
    if gan_shens[0] == '杀':
        print("年干为七杀：早年可能不顺。家境可能贫寒或身体不好。")
        if gan_shens[1] == '杀':
            print("年月天干都是七杀：家庭可能复杂。")
    if '官' in gan_shens:
        print("官星和七杀同见天干不佳。女性如在年干月干，30岁以前婚姻可能不佳，或体弱多病。")
    if gan_shens[1] == '杀' and zhi_shens[1] == '杀':
        print("月柱天干地支都是七杀：克制过度。可能有福不会享。六亲缘分薄。")
        if '杀' not in zhi_shens2 :
            print("七杀年月浮现天干：性格可能多变，不容易安定。30岁以前可能不顺。")        
    if '杀' in zhi_shens and '劫' in zhi_shens:
        print("七杀地支有根时需要阳刃强才佳。杀身两停。")
    if gan_shens[1] == '杀' and gan_shens[3] == '杀':
        print("月时天干为七杀：可能体弱多病")    
    if gan_shens[0] == '杀' and gan_shens[3] == '杀':
        print("七杀在年干时干：男性头胎可能有麻烦，女性婚姻可能有阻碍。")  
    if gan_shens[3] == '杀':
        print("七杀在时干：可能性格固执有毅力。")       
    if '印' in gan_shens:
        print("身弱杀生印：不少是精明练达的商人。")  
    if '财' in gan_shens or '才' in gan_shens:
        print("财生杀：如果不是身弱有印，不佳。")  
        for zhi_ in zhis: 
            if set((ten_deities[me].inverse['杀'], ten_deities[me].inverse['财'])) in set(zhi5[zhi_]):
                print("杀不喜与财同根透出，这样杀的力量可能过强。")  


for seq, gan_ in enumerate(gan_shens):
    if gan_ != '杀' and zhi_shens[seq] != '杀':
        continue   
    if gan_ == '杀' and '杀' in zhi_shen3[seq] and seq != 3:
        print("七杀坐七杀：六亲缘分可能薄。")
    if get_empty(zhus[2],zhis[seq]) == '空':
        print("七杀坐空亡：女命夫缘可能薄。")
    if zhis[seq] == '食':
        print("七杀坐食：可能易有错误判断。")
    if zhi_xing[seq] or zhi_6chong[seq]:
        print("七杀坐刑或对冲：夫妻可能不和。")
        
            
if shens2.count('杀') > 2:
    print("杀多者如果无制：性格可能刚强。喜欢打抱不平，不易听人劝。女性可能喜欢令人佩服的人。")
if zhi_shens[2]  == '杀' and len(zhi5[zhis[2]]) == 1:
    print("天元坐杀（如乙酉，己卯）：如无食神、阳刃，性格可能急躁，聪明，对人不信任。如果七杀还透出月干无制，可能体弱多病，甚至夭折。如果在时干，晚年可能不好。")
    
if zhus[2] in (('丁', '卯'), ('丁', '亥'), ('丁', '未')) and zhis.time == '子':
    print("七杀坐桃花：如有刑冲，可能因感情引祸。忌讳午运。")
    
if gan_shens.count('杀') > 2 :
    print("天干有两个以上七杀：可能不是长子，性格浮躁不持久。")   

if ten_deities[shang].inverse['建'] in zhis and options.n:
    print("女命地支有七杀的禄：丈夫条件可能还不错。对外性格急躁，对丈夫还算顺从。")  
    
    
    
if zhis[2] == me_jue:
    print("#"*10, "日主自坐绝地")
    if zhi_6he[2]:
        
        print("日主自坐绝地（天元坐杀）：日支与它支合化，可能双妻，子息迟。") 
        
    print("日主自坐绝地，绝地合会：可能先贫后富。")  
    if zhis[3] == zhis[2]:
        print("日主日时同在绝地：旺相则可能有刑灾。")  
        
    if zhis[3] == zhis[2] == zhis[1]:
        print("日主月日时同在绝地：旺相则可能有刑灾，平常人不要紧。")  
    if zhi_shens.count('比') + zhi_shens.count('劫') > 1 :
        print("日主自坐绝地，地支比劫大于1：旺衰可能巨变，不利。")
    
    if zhis[1] == me_jue:
        print("日主月日同在绝地：即使有格局也可能疾病夭折。")  
        
    if zhis[3] == cai_lu:
        print("日主自坐绝地，时支财禄：身弱财旺时可能有衰困，克妻子。")   
        
    if zhis[3] == cai_di:
        print("日主自坐绝地，时支偏财禄：有困顿时可能娶背景不佳的妻子。")   



        
if zhis[3] == me_jue:
    print("#"*10, "日主时柱坐绝地: 若成伤官格，可能难求功名，适合艺术九流。")
    if zhi_shens[2] == '枭':
        print("日主时支坐绝地，日坐枭神: 可能不适合做生意，可能是清贫的艺术九流人士。")
    if zhis[1] in (cai_di, cai_lu):
        print("日主时支坐绝地，月支坐财：可能先富，晚年大败，有刑克。")    

    if zhis[1] in (me_lu, me_di):
        print("日主时支坐绝地，月支坐帝旺或禄：可能刑妻克子。")   
        
    if zhis[3] in (cai_di,cai_lu):
        print("日主时支坐绝地，时支坐财：中年发达后可能无作为。")   
        

if zhis[2] == sha_lu:
    if zhi_ku(zhis[3], (guan, sha)):
        print("日主自坐七杀禄，时支为官杀库：一生可能有疾，生计平常。")    
        
if zhis[3] == sha_lu:
    if zhi_xing[3] or zhi_6chong[3]:
        
        print("时支七杀禄带刑冲：即使吉命也可能带疾不长寿。")  

if gan_shens[3] == '杀' and zhis[3] in (cai_di, cai_lu):
    print("七杀时柱坐财禄旺：性格可能严肃。可能双妻，子息迟。")  

if zhis[3] == sha_lu:
    if (zhi_6chong[3] or zhi_xing[3]):
        print("七杀时禄旺遇刑冲：可能寿命短，带疾。") 
    if zhis[1] == sha_lu:
        print("七杀时月禄旺：可能体弱多病。")
 
if zhi_ku(zhis[2], (guan,sha)):
    if set(zhis).issubset(set('辰戌丑未')):
        print("日主自坐七杀入墓，地支都为库：可能孤独，适合艺术。") 
        
if '杀' in gan_shens and zhi_shens.count('杀') > 1:
    print("七杀透干，地支双根：不论贫富，亲属可能离散。") 
    
if  '杀' in jus + all_ges:

    if '比' in gan_shens or '劫' in gan_shens:
        print("杀格透比或劫：性格可能急躁但有分寸。")
    
    if '杀' in gan_shens:
        print("杀格透官：可能精明琐屑，不怕脏。")    
        
    if '食' in gan_shens or '伤' in gan_shens:
        print("杀格透食伤：可能外表宁静，内心刚毅。")     
        
    if '印' in gan_shens:
        print("杀格透印：可能为人圆润、精明干练。")   


     
# 食神分析    
if '食' in gan_shens:
    print("\n----食神分析----")

    if '食' in zhi_shens2:
        print("食神成格：")
        print("- 寿命较好，尤其食神和偏财格更长寿")
        print("- 为人厚道，不太慷慨")
        print("- 有口福")
        print("- 喜财忌偏印（只能用偏财制）")
        print("- 无财时一生衣食无忧，但无大福")
        print("- 有印时需用比劫通关或财制")
        all_ges.append('食')
        
    if (gan_shens[0] == '食' and gan_shens[1] == '食') or (gan_shens[1] == '食' and '食' in zhi_shen3[1]):
        print("食神月重叠：")
        print("- 生长在安定环境")
        print("- 性格仁慈")
        print("- 无冲刑则长寿")
        print("- 女性早年得子")
        print("- 无冲刑偏印者为佳命")

    if '枭' in gan_shens:
        print("食神遇偏印：")
        print("- 男性身体较差")
        print("- 四柱透出偏财可缓解")
        if '劫' in gan_shens:
            print("- 食神与劫财、偏印同时出现在天干，体弱多病")
        if '杀' in gan_shens:
            print("- 食神与七杀、偏印同时成格，体弱多病")
    if '食' in zhi_shens:
        print("食神天透地藏：")
        print("- 女命阳日主适合社会性职业")
        print("- 女命阴日主适合上班族")
    if (not '财' in gan_shens) and (not '才' in gan_shens):
        print("食神多而无财：需要食伤生财才好，否则难发")
    if '伤' in gan_shens:
        print("食伤混杂：食神和伤官同透天干，志大才疏")
    if '杀' in gan_shens:
        print("食神制杀：杀不是主格时，容易施舍后后悔")

    for seq, gan_ in enumerate(gan_shens):
        if gan_ == '食' and zhi_shens[seq] =='劫':
            print("食神坐阳刃：辛劳")
        
            
if shens2.count('食') > 2:
    print("食神过多：")
    print("- 四个及以上视为伤官")
    print("- 需要食伤生财才好，无财难发")
    if '劫' in gan_shens or '比' in gan_shens:
        print("- 带比劫时，好施舍，乐于做社会服务")
        
if ('杀', '食') in shen_zhus or ( '食', '杀') in shen_zhus:
    print("食神与七杀同柱：易怒，食神制杀最好食在前")
    
if ('枭', '食') in shen_zhus or ( '食', '枭') in shen_zhus:
    print("食神与偏印同柱：女命不利后代，尤其在时柱")
    
if '食' in zhi_shen3[2] and zhis[2] in zhengs:
    print("日支食神专位：")
    print("- 容易发胖，有福")
    print("- 男命有助力之妻")
if zhi_shens[2]  == '食' and zhi_shens[2]  == '杀':
    print("自坐食神，时支杀专，二者不出天干：多成败，最后失局")  
    
if zhi_shens[2]  == '食':
    print("自坐食神：")
    print("- 相敬相助，即使透枭也无事")
    print("- 心思不定，做事毅力不足")
    print("- 可能假客气")
    print("- 专位容易发胖，有福")
 
    
if zhis[2]  == shi_lu:
    if zhis[3]  == sha_lu and (sha not in gan_shens):
        print("自坐食，时支专杀不透干：多成败，终局失制")

if '食' in zhi_shen3[3] and '枭' in zhi_shen3[3] + gan_shens[3]:
    print("时支食神逢偏印：")
    print("- 体弱，易有慢性病")
    print("- 女性一婚可能不长久")  
    
if zhis[2] in kus and zhi_shen3[2][2] in ('食', '伤'):
    print("自坐食伤库：总觉得钱不够")
    
if  '食' in (gan_shens[0], zhi_shens[0]):
    print("年柱食：可能三代同堂")

if zhi_ku(zhis[3], (shi, shang)) and ('食' in zhi_shen3[1] or '伤' in zhi_shen3[1]):
    print("时食库，月食当令：孤克")

# 自坐食伤库
if zhi_ku(zhis[2], (shi, shang)):  
    if zhis[3] == guan_lu:
        print("坐食伤库，时支官：发达时接近寿终")

# 自坐食伤库
if zhi_ku(zhis[3], (shi, shang)):  
        
    if zhis[1] in (shi_di, shi_lu):
        print("坐食伤库，月支食伤当令：吉命而孤克")
    

# 伤官分析    
if '伤' in gan_shens:
    print("\n----伤官分析----")

    print("伤官特点：")
    print("- 有才华，但清高")
    print("- 需要生财或印制")
    if '伤' in zhi_shens2:
        print("伤官成格：")
        print("- 不适合配印")
        print("- 金水、土金、木火命造更佳")
        print("- 火土命需调候，易火炎土燥")
        print("- 伤官和七杀的局不适合月支为库")
        all_ges.append('伤')
        print("- 生正财用偏印，生偏财用正印")
        print("- 配印时，如果透杀，透财不佳")
        print("- 伤官七杀同时成格，不透财为上好命局")

    if (gan_shens[0] == '伤' and gan_shens[1] == '伤') or (gan_shens[1] == '伤' and '伤' in zhi_shen3[1]):
        print("伤官重叠：")
        print("- 父母兄弟缘薄")
        print("- 性格刚毅好掌权")
        print("- 30岁前感情生活可能较苦")
        print("- 适合老夫少妻，或先同居后结婚")

    if '印' in gan_shens and ('财' not in gan_shens):
        print("伤官配印无财：")
        print("- 有手艺，但不善理财")
        print("- 个性较强")
    if gan_shens[0] == '伤' and gan_shens[1] == '伤' and (not '伤' in zhi_shens2):
        print("年月天干都是伤官：亲属缘薄")

    if zhi_shens[1]  == '伤' and len(zhi5[zhis[1]]) == 1 and gan_shens[1] == '伤':
        print("月柱伤官坐专位：")
        print("- 夫缘不定")
        print("- 可能有名无实的婚姻关系")

    for seq, gan_ in enumerate(gan_shens):
        if gan_ == '伤' and zhi_shens[seq] =='劫':
            print("伤官地支坐阳刃：")
            print("- 力不从心")
            print("- 背禄逐马，克官劫财")
            print("- 影响约15年")
            print("- 只适合纯粹的精明商人或严谨掌握财之人")       
            
if shens2.count('伤') > 2:
    if options.n:        
        print("女命伤官多：即使不入伤官格，也缘分浅，多有苦情")
    if gan_shens.count('伤') > 2:
        print("天干两个以上伤官：")
        print("- 性格骄傲")
        print("- 六亲缘薄")
        print("- 婚前诉说家人，婚后埋怨配偶")
        print("- 30岁前为婚姻危机期")
        
    
if zhi_shens[2]  == '伤' and len(zhi5[zhis[2]]) == 1:
    print("婚姻宫伤官专位：")
    print("- 女命：强势克夫")
    print("- 男命：对妻子不利")
    
if gan_shens[3]  == '伤' and me_lu == zhis[3]:
    print("伤官坐时禄：")
    print("- 六亲缘薄")
    print("- 无冲刑晚年发，有冲刑不发")

if zhis[3]  in (shang_lu, shang_di) and  zhis[1]  in (shang_lu, shang_di):
    print("月支时支食伤当令：")
    print("- 日主无根，泄尽日主")
    print("- 凶象")
    
if ten_deities[shang].inverse['建'] in zhis and options.n:
    print("女命地支伤官禄：婚姻难以承受贫穷")        


print("\n```")

# if all_ges or jus:
#     output = []
#     if all_ges:
#         output.append(f"格 {all_ges}")
#     if jus:
#         output.append(f"局 {jus}")
#     print(" ".join(output))


# if me+zhis.month in months:
#     print("\n\n《穷通宝鉴》")    
#     print("=========================")      
#     print(months[me+zhis.month])


# sum_index = ''.join([me, '日', *zhus[3]])
# if sum_index in summarys:
#     print("\n\n《三命通会》")    
#     print("=========================")      
#     print(summarys[sum_index])

if not options.b:
    print("\n## 大运\n")
    print("| 年龄 | 年份 | 干支 | 星运 | 纳音 | 天干 | 地支 | 地支藏干 | 空亡 | 地支关系 | 备注 |")
    print("|------|------|------|------|------|------|------|----------|------|----------|------|")
    for dayun in yun.getDaYun()[1:]:
        gan_ = dayun.getGanZhi()[0]
        zhi_ = dayun.getGanZhi()[1]
        fu = '*' if (gan_, zhi_) in zhus else " "
        zhi5_ = ''.join([f"{gan}{ten_deities[me][gan]}　" for gan in zhi5[zhi_]])
        
        zhi__ = set() # 大运地支关系
        for item in zhis:
            for type_ in zhi_atts[zhi_]:
                if item in zhi_atts[zhi_][type_]:
                    zhi__.add(f"{type_}:{item}")
        zhi__ = '  '.join(zhi__)
        
        empty = '空' if zhi_ in empties[zhus[2]] else ''
        
        jia = ""
        if gan_ in gans:
            for i in range(4):
                if gan_ == gans[i]:
                    if abs(Zhi.index(zhi_) - Zhi.index(zhis[i])) == 2:
                        jia += f"  --夹：{Zhi[(Zhi.index(zhi_) + Zhi.index(zhis[i]))//2]}"
                    if abs(Zhi.index(zhi_) - Zhi.index(zhis[i])) == 10:
                        jia += f"  --夹：{Zhi[(Zhi.index(zhi_) + Zhi.index(zhis[i]))%12]}"
        
        out = f"| {dayun.getStartAge():<4} | {'':<4} | {dayun.getGanZhi()} | {ten_deities[me][zhi_]} | {nayins[(gan_, zhi_)]} | {ten_deities[me][gan_]}:{gan_} | {zhi_} | {zhi5_} | {empty} | {zhi__} | {fu}{jia}{get_shens(gans, zhis, gan_, zhi_)} |"
        
        print(out)
        zhis2 = list(zhis) + [zhi_]
        gans2 = list(gans) + [gan_]
        for liunian in dayun.getLiuNian():
            gan2_ = liunian.getGanZhi()[0]
            zhi2_ = liunian.getGanZhi()[1]
            fu2 = '*' if (gan2_, zhi2_) in zhus else " "
            
            zhi6_ = ''.join([f"{gan}{ten_deities[me][gan]}　" for gan in zhi5[zhi2_]])
            
            zhi__ = set() # 大运地支关系
            for item in zhis2:
                for type_ in zhi_atts[zhi2_]:
                    if type_ != '破' and item in zhi_atts[zhi2_][type_]:
                        zhi__.add(f"{type_}:{item}")
            zhi__ = '  '.join(zhi__)
            
            empty = '空' if zhi2_ in empties[zhus[2]] else ''
            
            jia = ""
            if gan2_ in gans2:
                for i in range(5):
                    if gan2_ == gans2[i]:
                        zhi1 = zhis2[i]
                        if abs(Zhi.index(zhi2_) - Zhi.index(zhis2[i])) == 2:
                            jia += f"  --夹：{Zhi[(Zhi.index(zhi2_) + Zhi.index(zhis2[i]))//2]}"
                        if abs(Zhi.index(zhi2_) - Zhi.index(zhis2[i])) == 10:
                            jia += f"  --夹：{Zhi[(Zhi.index(zhi2_) + Zhi.index(zhis2[i]))%12]}"
                        if (zhi1 + zhi2_ in gong_he) and (gong_he[zhi1 + zhi2_] not in zhis):
                            jia += f"  --拱：{gong_he[zhi1 + zhi2_]}"
            
            all_zhis = set(zhis2) | {zhi2_}
            special_combos = []
            if set('戌亥辰巳').issubset(all_zhis):
                special_combos.append("天罗地网：戌亥辰巳")
            if set('寅申巳亥').issubset(all_zhis) and len(set('寅申巳亥') & set(zhis)) == 2:
                special_combos.append("四生：寅申巳亥")
            if set('子午卯酉').issubset(all_zhis) and len(set('子午卯酉') & set(zhis)) == 2:
                special_combos.append("四败：子午卯酉")
            if set('辰戌丑未').issubset(all_zhis) and len(set('辰戌丑未') & set(zhis)) == 2:
                special_combos.append("四库：辰戌丑未")
            
            out = f"| {liunian.getAge():>3} | {liunian.getYear():<4} | {gan2_+zhi2_} | {ten_deities[me][zhi2_]} | {nayins[(gan2_, zhi2_)]} | {ten_deities[me][gan2_]}:{gan2_} | {zhi2_} | {zhi6_} | {empty} | {zhi__} | {fu2}{jia}{get_shens(gans, zhis, gan2_, zhi2_)} {' '.join(special_combos)} |"
            print(out)
    
    # 计算星宿
    d2 = datetime.date(1, 1, 4)
    print(f"\n星宿: {lunar.getXiu()}, {lunar.getXiuSong()}")
    
    # # 计算建除
    # seq = 12 - Zhi.index(zhis.month)
    # print(f"\n建除: {jianchus[(Zhi.index(zhis.day) + seq)%12]}")
# 检查三会 三合的拱合
result = ''
#for i in range(2):
    #result += check_gong(zhis, i*2, i*2+1, me, gong_he)
    #result += check_gong(zhis, i*2, i*2+1, me, gong_hui, '三会拱')

result += check_gong(zhis, 1, 2, me, gong_he)
result += check_gong(zhis, 1, 2, me, gong_hui, '三会拱')
    
# if result:
#     print(result)

# print("="*120)   



# 格局分析

ge = ''
if (me, zhis.month) in jianlus:
    print(jianlu_desc)
    print(jianlus[(me, zhis.month)]) 
    ge = '建'
#elif (me == '丙' and ('丙','申') in zhus) or (me == '甲' and ('己','巳') in zhus):
    #print("格局：专财. 运行官旺 财神不背,大发财官。忌行伤官、劫财、冲刑、破禄之运。喜身财俱旺")
elif (me, zhis.month) in (('甲','卯'), ('庚','酉'), ('壬','子')):
    ge = '月刃'
else:
    zhi = zhis[1]
    if zhi in wuhangs['土'] or (me, zhis.month) in (('乙','寅'), ('丙','午'),  ('丁','巳'), ('戊','午'), ('己','巳'), ('辛','申'), ('癸','亥')):
        for item in zhi5[zhi]:
            if item in gans[:2] + gans[3:]:
                ge = ten_deities[me][item]
    else:
        d = zhi5[zhi]
        ge = ten_deities[me][max(d, key=d.get)]

# 天乙贵人
flag = False
for items in tianyis[me]:
    for item in items:
        if item in zhis:
            if not flag:
                print("| 天乙贵人：", end=' ')
                flag = True
            print(item, end=' ')
            
# 玉堂贵人
flag = False
for items in yutangs[me]:
    for item in items:
        if item in zhis:
            if not flag:
                print("| 玉堂贵人：", end=' ')
                flag = True
            print(item, end=' ')            

# 天罗
if  nayins[zhus[0]][-1] == '火':			
    if zhis.day in '戌亥':
        print("| 天罗：{}".format(zhis.day), end=' ') 

# 地网		
if  nayins[zhus[0]][-1] in '水土':			
    if zhis.day in '辰巳':
        print("| 地网：{}".format(zhis.day), end=' ') 		



# 学堂分析
for seq, item in enumerate(statuses):
    if item == '长':
        print("\n学堂:", zhis[seq], "\t", end=' ')
        if  nayins[zhus[seq]][-1] == ten_deities[me]['本']:
            print("\n正学堂:", nayins[zhus[seq]], "\t", end=' ')


#xuetang = xuetangs[ten_deities[me]['本']][1]
#if xuetang in zhis:
    #print("学堂:", xuetang, "\t\t", end=' ')
    #if xuetangs[ten_deities[me]['本']] in zhus:
        #print("正学堂:", xuetangs[ten_deities[me]['本']], "\t\t", end=' ')

# 学堂分析

for seq, item in enumerate(statuses):
    if item == '建':
        print("| 词馆:", zhis[seq], end=' ')
        if  nayins[zhus[seq]][-1] == ten_deities[me]['本']:
            print("- 正词馆:", nayins[zhus[seq]], end=' ')


ku = ten_deities[me]['库'][0]    
if ku in zhis:
    print("库：",ku, end=' ')

    for item in zhus: 
        if ku != zhus[1]:
            continue
        if nayins[item][-1] == ten_deities[me]['克']:
            print("库中有财，其人必丰厚")
        if nayins[item][-1] == ten_deities[me]['被克']:
            print(item, ten_deities[me]['被克'])
            print("绝处无依，其人必滞")    


print("\n## 日主分析\n")
print("```")

# 天元分析
# for item in zhi5[zhis[2]]:    
#     name = ten_deities[me][item]
#     print(self_zuo[name])


# 出身分析
cai = ten_deities[me].inverse['财']
guan = ten_deities[me].inverse['官']
jie = ten_deities[me].inverse['劫']
# births = tuple(gans[:2])
# if cai in births and guan in births:
#     birth = '不错'
#elif cai in births or guan in births:
    #birth = '较好'
# else:
#     birth = '一般'
# print("## 出身分析\n")
# print("出身:", birth)    

guan_num = shens.count("官")
sha_num = shens.count("杀")
cai_num = shens.count("财")
piancai_num = shens.count("才")
jie_num = shens.count("劫")
bi_num = shens.count("比")
yin_num = shens.count("印")
ge = all_ges[0]

# print("\n## 格局分析\n")
# print(all_ges)


if all_ges or jus:
    print("\n## 格局分析\n")

    output = []
    if all_ges:
        output.append(f"格 {all_ges}")
    if jus:
        output.append(f"局 {jus}")
    print(" ".join(output))



# 食神分析
if ge == '食':
    print("\n****食神分析****")
    print("食神格特点：聪明、乐观、优雅、多才多艺。")
    print("有利条件：日主旺、食神旺、无冲破、有财辅助。")
    print("不利条件：日主弱、比劫多、偏印(倒食)。")
    print("建议：")
    print("- 宜发展财运")
    print("- 月令建禄最佳，时令次之")
    print("- 喜见贵人")

    shi_num = shens.count("食")
    if shi_num > 2:
        print("食神过多提醒：")
        print("- 可能少子或子女性格倔强")
        print("- 建议行印运来中和")
    if set(('财','食')) in set(gan_shens[:2] + zhi_shens[:2]):
        print("家庭背景：祖上可能有好的基业") 
    if set(('财','食')) in set(gan_shens[2:] + zhi_shens[2:]):
        print("婚姻提醒：配偶可能获福，但要注意与母亲的关系")
    if cai_num >1:
        print("财运提醒：财源可能较多，但要注意管理")

    for seq, item in enumerate(gan_shens):
        if item == '食':
            if ten_deities[gans[seq]][zhis[seq]] == '墓':
                print("健康提醒：食神入墓，要注意饮食健康")  

    for seq, item in enumerate(gan_shens):
        if item == '食' or zhi_shens[seq] == '食':
            if get_empty(zhus[2],zhis[seq]):
                print("事业提醒：食神遇空亡，可能从事医药、艺术等行业，但要避免官非")                     

    # 倒食分析
    if '枭' in shens and (me not in ['庚', '辛','壬']) and ten_deities[me] != '建':
        flag = True
        for item in zhi5[zhis.day]:
            if ten_deities[me]['合'] == item:
                flag = False
                break
        if flag:
            print("性格提醒：可能较为犹豫不决，做事有始无终")
            print("人际关系：可能与长辈或权威人士关系较差")
            print("建议：增强自信，提高做事的决断力和持续性")
    print()

# 伤官分析
if ge == '伤':
    print("\n****伤官分析****")
    print("伤官格特点：多才多艺，个性较强，有创新能力")
    print("有利条件：日主旺、有财星、有印绶")
    print("不利条件：日主弱、无财、刑冲、枭印过旺")
    print("建议：")
    print("- 日主旺时宜用财，日主弱时宜用印")
    print("- 用印时不忌讳官煞，但要去财")

    if '财' in shens or '才' in shens:
        print("财运提醒：伤官生财，财运较好")
    else:
        print("财运提醒：伤官无财，需要注意理财")
        
    if '印' in shens or '枭' in shens:
        print("性格特点：较为温和，有才华")   
        if '财' in shens or '才' in shens:
            print("事业发展：财印并济，有利于事业发展")
    if ('官' in shens) :
        print("官运提醒：金水配合较好，但需要财印辅助")
    if ('杀' in shens) :
        print("事业发展：有制衡，较为顺利，但要避免过于刚烈")
    if gan_shens[0] == '伤':
        print("人生格局：基础较好，但要注意培养良好的人际关系")

    for seq, item in enumerate(gan_shens):
        if item == '伤':
            if ten_deities[gans[seq]][zhis[seq]] == '墓':
                print("健康提醒：伤官入墓，要注意饮食健康")  

    for seq, item in enumerate(gan_shens):
        if item == '食' or zhi_shens[seq] == '食':
            if get_empty(zhus[2],zhis[seq]):
                print("事业提醒：伤官遇空亡，可能从事艺术、设计等创新行业，但要注意稳定性")                     
    print()

# 劫财分析
if ge == '劫':
    print("\n****劫财(阳刃)分析****")
    print("特点：个性强烈，有领导能力，但易冲动")
    print("提醒：阳刃与大运、流年相冲，可能带来突发事件，需谨慎")

    shi_num = shens.count("食")
    print("建议：培养耐心，增强自我控制能力")

# 财分析

if ge == '财' or ge == '才':
    print("\n****财分析****")
    print("财格特点：善于理财，有经商才能")
    print("有利条件：日主旺、有印、有食神、有官星")
    print("不利条件：比劫多、羊刃、空绝、冲合")
    print("建议：")
    print("- 财星喜根深，不宜太露")
    print("- 透出一位财星最佳，太多则不佳")
    
    if gan_shens.count('财') + gan_shens.count('才') > 1:
        print("财运提醒：财源较多，但要注意合理分配")
    if '伤' in gan_shens:
        print("事业发展：创新能力强，但要注意稳健发展")    
    if '食' in shens:
        print("人际关系：人缘较好，善于社交")     
        if '印' in shens or '枭' in 'shens':
            print("性格特点：内外有别，注意平衡")  
    if '比' in shens:
        print("竞争提醒：可能面临竞争，需要提高自身实力")   
    if '杀' in shens:
        print("事业发展：有冲劲，但要注意控制脾气")          
    
    if "财" == zhi_shens[0]:
        print("家庭背景：祖上可能有好的基业")
    if "财" == zhi_shens[3]:
        print("婚姻提醒：可能娶贤妻，得外来财运")      
    if "财" == zhi_shens[2] and (me not in ('壬','癸')):
        print("个人特质：理财能力强")              
    if ('官' not in shens) and ('伤' not in shens) and ('食' not in shens):
        print("事业发展：可能在商业方面有成就")

    if cai_num > 2 and ('劫' not in shens) and ('比' not in shens) \
       and ('比' not in shens) and ('印' not in shens):
        print("财运提醒：财多身弱，需要注意节制开支")

    if '印' in shens:
        print("事业发展：先理财后受益，发展较为稳健")      
    if '官' in gan_shens:
        print("事业成就：财官双全，有望获得较高成就")          
    if '财' in gan_shens and (('劫' not in shens) and ('比' not in shens)):
        print("理财建议：不宜过于炫耀财富")  
    for seq, item in enumerate(gan_shens):
        if item == '财':
            if ten_deities[gans[seq]][zhis[seq]] == '墓':
                print("婚姻提醒：财星入墓，婚姻可能较晚或有波折")  
            if ten_deities[gans[seq]][zhis[seq]] == '长':   
                print("财运提醒：财运旺盛，可能拥有较多资产")  

    if ('官' not in shens) and (('劫' in shens) or ('比' in shens)):
        print("事业提醒：可能面临竞争，需要提高专业能力")

    if bi_num + jie_num > 1:
        print("人际关系：兄弟姐妹可能较多，要注意协调关系")        

    for seq, item in enumerate(zhi_shens):
        if item == '才' or ten_deities[me][zhis[seq]] == '才':
            if get_empty(zhus[2],zhis[seq]):
                print("事业提醒：财运可能不稳定，需要谨慎投资")  

print("\n## 财库分析\n")

# 财库分析
if ten_deities[ten_deities[me].inverse["财"]]['库'][-1] in zhis or ('才' in zhi_shens[1] or '财' in zhi_shens[1]) :
    print("财运提醒：财库较深厚，但要善于开发利用")
else :  
# if cai_num < 2 and (('劫' in shens) or ('比' in shens)):
    print("财运提醒：财少身强，需要努力开源节流")   

# 官分析
if ge == "官":
    print("\n****官分析****")
    print("官格特点：正直守规，适合从事公职或管理工作")
    print("有利条件：日主旺、有财印")
    print("不利条件：日主弱、偏官、伤官、刑冲、泄气、贪合、入墓")
    print("建议：")
    print("- 财旺印衰时宜印，忌食伤生财")
    print("- 旺印财衰时宜财，喜食伤生财")
    print("- 带伤食用印制")
    print("- 带煞伤食不碍")
    
    if guan_num > 1:
        print("官星提醒：官星过多，要注意平衡")
    if "财" in shens and "印" in shens and ("伤" not in shens) and ("杀" not in shens):
        print("事业发展：官星得到财、印扶持，发展前景较好")
    if "财" in shens or '才' in shens:
        print("财运提醒：财运较好，有助于事业发展")       
    if "印" in shens or "枭" in shens:
        print("个人能力：学识渊博，有利于事业发展")   
    if "食" in shens:
        print("人际关系：人缘较好，有利于事业发展")    
    if "伤" in shens:
        print("创新能力：有创新思维，但要注意稳健发展")         
    if "杀" in shens:
        print("领导能力：有决断力，但要注意平和处事")        

    if zhi_shens[2] in ("财","印"):
        print("个人特质：能力突出，容易得到赏识")           
    if zhi_shens[2] in ("伤","杀"):
        print("健康提醒：要注意身体健康，避免过度劳累")   

    # 检查天福贵人
    if (guan, ten_deities[guan].inverse['建']) in zhus:
        print("事业发展：有望获得较高成就")

    # 天元坐禄    
    if guan in zhi5[zhis[2]]:
        print("事业发展：官运亨通，有望获得较高成就")

    # 岁德正官
    if gan_shens[0] == '官' or zhi_shens[0] == '官':
        print("家庭背景：可能出身较好，或有长辈提携")    

    # 时上正官
    if gan_shens[0] == '官' or zhi_shens[0] == '官':
        print("晚年运势：晚年较为顺遂")        

    print()
# 官库分析
if ten_deities[ten_deities[me].inverse["官"]]['库'][-1] in zhis:
    print("官运提醒：官运较好，但要善于把握机会")   
    if lu_ku_cai[me] in zhis:
        print("事业发展：官印禄库俱全，发展前景较好")

# 杀(偏官)分析
if ge == "杀":
    print("\n****杀(偏官)分析****")
    print("偏官格特点：个性强烈，有领导才能，但易冲动")
    print("有利条件：日主旺、印绶、合煞、食制、羊刃、比劫")
    print("不利条件：日主弱、财星、正官、刑冲、入墓")
    print("建议：")
    print("- 培养耐心和自制力")
    print("- 注意调和人际关系")
    print("- 避免过于激进")
    
    if "财" in shens:
        print("财运提醒：财运较好，但要注意合理使用")
    if "比" in shens:
        print("竞争提醒：可能面临竞争，需要提高自身实力")        
    if "食" in shens:
        print("事业发展：有创新能力，利于事业发展")   
        if "财" in shens or "印" in shens or '才' in shens or "枭" in shens:
            print("事业发展：多方面发展，前景较好")   
    if "劫" in shens:
        print("个人特质：有冲劲，但要注意控制脾气")    
    if "印" in shens:
        print("个人能力：学识渊博，有利于事业发展")           
    if sha_num > 1:
        print("性格特点：个性较为强烈，要学会控制情绪") 
        if weak:
            print("事业发展：可能需要在异乡发展，要注意适应环境")
            
    if "杀" == zhi_shens[2]:
        print("性格特点：性格急躁，要学会耐心和包容")      
    if "杀" == zhi_shens[3] or "杀" == gan_shens[3]:
        print("晚年运势：晚年较为劳累，要注意休息")   
        
    if "杀" == zhi_shens[0]:
        print("家庭背景：可能出身较为普通，但有后天发展机会")   
        
    if ('官' in shens) :
        print("事业发展：有领导才能，但要注意团队协作")

    for seq, item in enumerate(gan_shens):
        if item == '杀':
            if ten_deities[gans[seq]][zhis[seq]] == '长':   
                print("婚姻提醒：女命可能嫁给地位较高的人")  
    print()

# 印分析
if ge == "印":
    print("\n****印分析****")
    print("印格特点：学识渊博，性格温和")
    print("有利条件：食神、天月德、七煞")
    print("不利条件：刑冲、伤官、死墓")
    print("建议：")
    print("- 发展学术或文化相关事业")
    print("- 注意平衡事业和家庭")
    
    if "官" in shens:
        print("事业发展：官印相生，有利于仕途发展")      
    if "杀" in shens:
        print("个人能力：有决断力，但要注意温和处事")    
    if "伤" in shens or "食" in shens:
        print("创新能力：有创新思维，利于事业发展")     
    if "财" in shens or "才" in shens:
        print("财运提醒：财印并济，要注意平衡发展")             

    if yin_num > 1:
        print("个人特质：性格清高，但可能人际关系较淡")  
    if "劫" in shens:
        print("事业发展：可能需要改变方向，寻找新的机会")              
    
# 偏印分析
if ge == "枭":
    print("\n****偏印分析****")
    print("偏印格特点：聪明灵活，有独特见解")
    print("有利条件：食神、天月德、七煞")
    print("不利条件：刑冲、伤官、死墓")
    print("建议：")
    print("- 发展专业技能或特殊才能")
    print("- 注意与他人的沟通和协作")
    
    if "官" in shens:
        print("事业发展：官印相生，有利于专业发展")      
    if "杀" in shens:
        print("个人能力：有独特见解，但要注意与他人协调")    
    if "伤" in shens or "食" in shens:
        print("创新能力：有创新思维，适合从事创新工作")     
    if "财" in shens or "才" in shens:
        print("事业发展：可能需要改变方向，追求更高目标")             

    if yin_num > 1:
        print("个人特质：才华横溢，但可能较为孤傲")  
    if "劫" in shens:
        print("事业发展：可能面临变动，要善于把握机会")              


gan_ = tuple(gans)
for item in Gan:
    if gan_.count(item) == 3:
        print("三字干：", item, "--", gan3[item])
        break

gan_ = tuple(gans)
for item in Gan:
    if gan_.count(item) == 4:
        print("四字干：", item, "--", gan4[item])
        break    

zhi_ = tuple(zhis)
for item in Zhi:
    if zhi_.count(item) > 2:
        print("三字支：", item, "--", zhi3[item])
        break

# print("="*120)  
# print("你属:", me, "特点：--", gan_desc[me],"\n")
# print("年份:", zhis[0], "特点：--", zhi_desc[zhis[0]],"\n")





# 羊刃分析
key = '帝' if Gan.index(me)%2 == 0 else '冠'

if ten_deities[me].inverse[key] in zhis:
    print("\n羊刃分析:")
    print(f"您的命局中存在羊刃：{me} {ten_deities[me].inverse[key]}")
    if ten_deities[me].inverse['冠']:
        print("羊刃与禄相重，预示富贵双全。若有官星或印星相助，更是福气深厚。")
    else:
        print("羊刃单独出现，可能预示人生道路较为艰辛，需要付出更多努力。")

# 将星分析
me_zhi = zhis[2]
other_zhis = zhis[:2] + zhis[3:]
flag = False
tmp_list = []
if me_zhi in ("申", "子", "辰") and "子" in other_zhis:
    flag = True
    tmp_list.append((me_zhi, '子'))
elif me_zhi in ("丑", "巳", "酉") and "酉" in other_zhis:
    flag = True   
    tmp_list.append((me_zhi, '酉'))
elif me_zhi in ("寅", "午", "戌") and "午" in other_zhis:
    flag = True     
    tmp_list.append((me_zhi, '午'))
elif me_zhi in ("亥", "卯", "未") and "卯" in other_zhis:
    flag = True   
    tmp_list.append((me_zhi, '卯'))

if flag:
    print("\n将星分析:")
    print("您的命局中存在将星，这通常预示着领导才能和卓越成就。")
    print("将星最好与吉星相伴，若有贵人相助，更能成就非凡。")
    print(f"您的将星组合：{tmp_list}")

# 华盖分析
flag = False
if (me_zhi in ("申", "子", "辰") and "辰" in other_zhis) or \
   (me_zhi in ("丑", "巳", "酉") and "丑" in other_zhis) or \
   (me_zhi in ("寅", "午", "戌") and "戌" in other_zhis) or \
   (me_zhi in ("亥", "卯", "未") and "未" in other_zhis):
    flag = True   

if flag:
    print("\n华盖分析:")
    print("您的命局中存在华盖，这可能意味着您具有独特的才能或思维方式。")
    print("华盖虽然象征才华，但也可能带来一定的孤独感。")
    print("建议：发展个人特长，同时注意培养人际关系。")

# 咸池（桃花）分析
flag = False
taohuas = []
year_zhi = zhis[0]
if (me_zhi in ("申", "子", "辰") or year_zhi in ("申", "子", "辰")) and "酉" in zhis:
    flag = True
    taohuas.append("酉")
elif (me_zhi in ("丑", "巳", "酉") or year_zhi in ("丑", "巳", "酉")) and "午" in other_zhis:
    flag = True   
    taohuas.append("午")
elif (me_zhi in ("寅", "午", "戌") or year_zhi in ("寅", "午", "戌")) and "卯" in other_zhis:
    flag = True    
    taohuas.append("卯")
elif (me_zhi in ("亥", "卯", "未") or year_zhi in ("亥", "卯", "未")) and "子" in other_zhis:
    flag = True   
    taohuas.append("子")

if flag:
    print("\n咸池（桃花）分析:")
    print("您的命局中存在咸池（桃花），这可能影响您的感情和人际关系。")
    print("优点：魅力十足，容易得到异性青睐。")
    print("注意事项：谨慎处理感情问题，避免因感情而影响事业或家庭。")
    print(f"您的桃花位于：{taohuas}")

# 禄分析
flag = False
for item in zhus:
    if item in lu_types[me]:
        if not flag:
            print("\n禄分析:")
            flag = True
        print(f"禄在{item}，含义：{lu_types[me][item]}")

# 文星贵人
if wenxing[me] in zhis:
    print("\n文星贵人:")
    print(f"您命中有文星贵人：{me} {wenxing[me]}")
    print("这预示您在学术、文化或艺术方面可能有特殊才能。")

# 天印贵人
if tianyin[me] in zhis:
    print("\n天印贵人:")
    print(f"您命中有天印贵人：{me} {tianyin[me]}")
    print("这是一个吉祥之兆，预示您可能会得到上级的赏识和提拔。")


# short = min(scores, key=scores.get)
# print("\n\n五行缺{}的建议参见 http://t.cn/E6zwOMq".format(short))    
# print("\n\n五行缺{}   ".format(scores))    
ShengChen(datetime.datetime(lunar.getYear(), lunar.getMonth(), lunar.getDay(),lunar.getHour(), 0, 0, 0)).calculate()
    
print("\n```")
 


if '杀' in shens:
    if yinyang(me) == '+':
        print("阳杀:话多,热情外向,异性缘好")
    else:
        print("阴杀:话少,性格柔和")
if '印' in shens and '才' in shens and '官' in shens:
    print("印,偏财,官:三奇 怕正财")
if '才' in shens and '杀' in shens:
    print("男:因女致祸、因色致祸; 女:赔货")
    
if '才' in shens and '枭' in shens:
    print("偏印因偏财而不懒！")    
    

print("\n## 命理解读\n")

print("### 流年分析\n")

# 获取当前年份
current_year = datetime.datetime.now().year

# 找到当前所在的大运
current_dayun = None
for dayun in yun.getDaYun()[1:]:
    if dayun.getStartYear() <= current_year < dayun.getStartYear() + 10:
        current_dayun = dayun
        break

# 获取本年二十四节气日期
a = cnlunar.Lunar(datetime.datetime(current_year, 3, 1), godType='8char')

if current_dayun:
    print(f"所在大运：{current_dayun.getGanZhi()} ({current_dayun.getStartYear()}-{current_dayun.getStartYear()+9})")
    print(f"\n当前年份(流年)：{current_year}({a.year8Char})")
print("\n### 大运与流年分析\n")


user_bazi = f"{gans.year}{zhis.year} {gans.month}{zhis.month} {gans.day}{zhis.day} {gans.time}{zhis.time}"
# 流年干支
liunian_gz = a.year8Char
# 分析大运与八字的关系
dayun_gz = current_dayun.getGanZhi()
dayun_gan, dayun_zhi = dayun_gz[0], dayun_gz[1]

print(f"大运干支：{dayun_gz}")
print(f"用户八字：{user_bazi}\n")

# 分析天干
gan_analysis = ten_deities[me][dayun_gan]

# 分析地支
zhi_analysis = ''
for gan in zhi5[dayun_zhi]:
    zhi_analysis += f"{gan}{gan5[gan]}{zhi5[dayun_zhi][gan]}{ten_deities[me][gan]} "

print(f" 天干：{gan_analysis}，地支：{zhi_analysis}")
he_analysis = ten_deities[me]['合']
cong_analysis = ten_deities[me]['冲']
print(f" 合：{he_analysis}，冲：{cong_analysis}")


ten_deities = {
    '甲':bidict({'甲':'比', "乙":'劫', "丙":'食', "丁":'伤', "戊":'才',
                  "己":'财', "庚":'杀', "辛":'官', "壬":'枭', "癸":'印', "子":'沐', 
                  "丑":'冠', "寅":'建', "卯":'帝', "辰":'衰', "巳":'病', "午":'死', 
                  "未":'墓', "申":'绝', "酉":'胎', "戌":'养', "亥":'长', '库':'未_', 
                  '本':'木', '克':'土', '被克':'金', '生我':'水', '生':'火','合':'己','冲':'庚'}),
    '乙':bidict({'甲':'劫', "乙":'比', "丙":'伤', "丁":'食', "戊":'财',
                  "己":'才', "庚":'官', "辛":'杀', "壬":'印',"癸":'枭', "子":'病', 
                  "丑":'衰', "寅":'帝', "卯":'建', "辰":'冠', "巳":'沐', "午":'长',
                  "未":'养', "申":'胎', "酉":'绝', "戌":'墓', "亥":'死', '库':'未_',
                  '本':'木', '克':'土', '被克':'金', '生我':'水', '生':'火','合':'庚','冲':'辛'}),
    '丙':bidict({'丙':'比', "丁":'劫', "戊":'食', "己":'伤', "庚":'才',
                  "辛":'财', "壬":'杀', "癸":'官', "甲":'枭', "乙":'印',"子":'胎', 
                  "丑":'养', "寅":'长', "卯":'沐', "辰":'冠', "巳":'建', "午":'帝',
                  "未":'衰', "申":'病', "酉":'死', "戌":'墓', "亥":'绝', '库':'戌_',
                  '本':'火', '克':'金', '被克':'水', '生我':'木', '生':'土','合':'辛','冲':'壬'}),
    '丁':bidict({'丙':'劫', "丁":'比', "戊":'伤', "己":'食', "庚":'财',
                  "辛":'才', "壬":'官', "癸":'杀', "甲":'印',"乙":'枭', "子":'绝', 
                  "丑":'墓', "寅":'死', "卯":'病', "辰":'衰', "巳":'帝', "午":'建',
                  "未":'冠', "申":'沐', "酉":'长', "戌":'养', "亥":'胎', '库':'戌_',
                  '本':'火', '克':'金', '被克':'水', '生我':'木', '生':'土','合':'壬','冲':'癸'}),
    '戊':bidict({'戊':'比', "己":'劫', "庚":'食', "辛":'伤', "壬":'才',
                  "癸":'财', "甲":'杀', "乙":'官', "丙":'枭', "丁":'印',"子":'胎', 
                  "丑":'养', "寅":'长', "卯":'沐', "辰":'冠', "巳":'建', "午":'帝',
                  "未":'衰', "申":'病', "酉":'死', "戌":'墓', "亥":'绝', '库':'辰_',
                  '本':'土', '克':'水', '被克':'木', '生我':'火', '生':'金','合':'癸','冲':''}),
    '己':bidict({'戊':'劫', "己":'比', "庚":'伤', "辛":'食', "壬":'财',
                  "癸":'才', "甲":'官', "乙":'杀', "丙":'印',"丁":'枭',"子":'绝', 
                  "丑":'墓', "寅":'死', "卯":'病', "辰":'衰', "巳":'帝', "午":'建',
                  "未":'冠', "申":'沐', "酉":'长', "戌":'养', "亥":'胎', '库':'辰_',
                  '本':'土', '克':'水', '被克':'木', '生我':'火', '生':'金','合':'甲','冲':''}),
    '庚':bidict({'庚':'比', "辛":'劫', "壬":'食', "癸":'伤', "甲":'才',
                  "乙":'财', "丙":'杀', "丁":'官', "戊":'枭', "己":'印',"子":'死', 
                  "丑":'墓', "寅":'绝', "卯":'胎', "辰":'养', "巳":'长', "午":'沐',
                  "未":'冠', "申":'建', "酉":'帝', "戌":'衰', "亥":'病', '库':'丑_',
                  '本':'金', '克':'木', '被克':'火', '生我':'土', '生':'水','合':'乙','冲':'甲'}), 
    '辛':bidict({'庚':'劫', "辛":'比', "壬":'伤', "癸":'食', "甲":'财',
                  "乙":'才', "丙":'官', "丁":'杀', "戊":'印', "己":'枭', "子":'长', 
                  "丑":'养', "寅":'胎', "卯":'绝', "辰":'墓', "巳":'死', "午":'病',
                  "未":'衰', "申":'帝', "酉":'建', "戌":'冠', "亥":'沐', '库':'丑_',
                  '本':'金', '克':'木', '被克':'火', '生我':'土', '生':'水','合':'丙','冲':'乙'}),
    '壬':bidict({'壬':'比', "癸":'劫', "甲":'食', "乙":'伤', "丙":'才',
                  "丁":'财', "戊":'杀', "己":'官', "庚":'枭', "辛":'印',"子":'帝', 
                  "丑":'衰', "寅":'病', "卯":'死', "辰":'墓', "巳":'绝', "午":'胎',
                  "未":'养', "申":'长', "酉":'沐', "戌":'冠', "亥":'建', '库':'辰_',
                  '本':'水', '克':'火', '被克':'土', '生我':'金', '生':'木','合':'丁','冲':'丙'}),
    '癸':bidict({'壬':'劫', "癸":'比', "甲":'伤', "乙":'食', "丙":'财',
                  "丁":'才', "戊":'官', "己":'杀', "庚":'印',"辛":'枭', "子":'建', 
                  "丑":'冠', "寅":'沐', "卯":'长', "辰":'养', "巳":'胎', "午":'绝',
                  "未":'墓', "申":'死', "酉":'病', "戌":'衰', "亥":'帝', '库':'辰_',
                  '本':'水', '克':'火', '被克':'土', '生我':'金', '生':'木','合':'戊','冲':'丁'}), 

}


zhi_atts = {
    "子":{"冲":"午", "刑":"卯", "被刑":"卯", "合":("申","辰"), "会":("亥","丑"), '害':'未', '破':'酉', "六":"丑","暗":"",},
    "丑":{"冲":"未", "刑":"戌", "被刑":"未", "合":("巳","酉"), "会":("子","亥"), '害':'午', '破':'辰', "六":"子","暗":"寅",},
    "寅":{"冲":"申", "刑":"巳", "被刑":"申", "合":("午","戌"), "会":("卯","辰"), '害':'巳', '破':'亥', "六":"亥","暗":"丑",},
    "卯":{"冲":"酉", "刑":"子", "被刑":"子", "合":("未","亥"), "会":("寅","辰"), '害':'辰', '破':'午', "六":"戌","暗":"申",},
    "辰":{"冲":"戌", "刑":"辰", "被刑":"辰", "合":("子","申"), "会":("寅","卯"), '害':'卯', '破':'丑', "六":"酉","暗":"",},
    "巳":{"冲":"亥", "刑":"申", "被刑":"寅", "合":("酉","丑"), "会":("午","未"), '害':'寅', '破':'申', "六":"申","暗":"",},
    "午":{"冲":"子", "刑":"午", "被刑":"午", "合":("寅","戌"), "会":("巳","未"), '害':'丑', '破':'卯', "六":"未","暗":"亥",},
    "未":{"冲":"丑", "刑":"丑", "被刑":"戌", "合":("卯","亥"), "会":("巳","午"), '害':'子', '破':'戌', "六":"午","暗":"",},
    "申":{"冲":"寅", "刑":"寅", "被刑":"巳", "合":("子","辰"), "会":("酉","戌"), '害':'亥', '破':'巳', "六":"巳","暗":"卯",},
    "酉":{"冲":"卯", "刑":"酉", "被刑":"酉", "合":("巳","丑"), "会":("申","戌"), '害':'戌', '破':'子', "六":"辰","暗":"",},
    "戌":{"冲":"辰", "刑":"未", "被刑":"丑", "合":("午","寅"), "会":("申","酉"), '害':'酉', '破':'未', "六":"卯","暗":"",},
    "亥":{"冲":"巳", "刑":"亥", "被刑":"亥", "合":("卯","未"), "会":("子","丑"), '害':'申', '破':'寅', "六":"寅","暗":"午",},
}

def analyze_bazi_dayun(user_bazi, dayun_gz,liunian_gz):
    user_gans = user_bazi.split()[0][0] + user_bazi.split()[1][0] + user_bazi.split()[2][0] + user_bazi.split()[3][0]
    user_zhis = user_bazi.split()[0][1] + user_bazi.split()[1][1] + user_bazi.split()[2][1] + user_bazi.split()[3][1]
    dayun_gan, dayun_zhi = dayun_gz[0], dayun_gz[1]
    liunian_gan, liunian_zhi = liunian_gz[0], liunian_gz[1]
    
    print("\n八字与大运关系分析：")
    print(f"大运天干{dayun_gan}与日主关系：{ten_deities[me][dayun_gan]}")
    print(f"流年天干{liunian_gan}与日主关系：{ten_deities[me][liunian_gan]}")
    
    for i, gan in enumerate(user_gans):
        if ten_deities[gan]['合'] == dayun_gan:
            print(f"{dayun_gan}{gan}相合")
        if ten_deities[gan]['冲'] == dayun_gan:
            print(f"{dayun_gan}{gan}相冲")
        if ten_deities[gan]['合'] == liunian_gan:
            print(f"{liunian_gan}{gan}相合")
        if ten_deities[gan]['冲'] == liunian_gan:
            print(f"{liunian_gan}{gan}相冲")
    
    for i, zhi in enumerate(user_zhis):
        if dayun_zhi in zhi_atts[zhi]['合']:
            print(f"{dayun_zhi}{zhi}相合")
        if zhi_atts[zhi]['冲'] == dayun_zhi:
            print(f"{dayun_zhi}{zhi}相冲")
        if zhi_atts[zhi]['刑'] == dayun_zhi or zhi_atts[zhi]['被刑'] == dayun_zhi:
            print(f"{dayun_zhi}{zhi}相刑")
        if zhi_atts[zhi]['害'] == dayun_zhi:
            print(f"{dayun_zhi}{zhi}相害")
        if dayun_zhi in zhi_atts[zhi]['会']:
            print(f"{dayun_zhi}{zhi}相会")
        if zhi_atts[zhi]['破'] == dayun_zhi:
            print(f"{dayun_zhi}{zhi}相破")
        if liunian_zhi in zhi_atts[zhi]['合']:
            print(f"{liunian_zhi}{zhi}相合")
        if zhi_atts[zhi]['冲'] == liunian_zhi:
            print(f"{liunian_zhi}{zhi}相冲")
        if zhi_atts[zhi]['刑'] == liunian_zhi or zhi_atts[zhi]['被刑'] == liunian_zhi:
            print(f"{liunian_zhi}{zhi}相刑")
        if zhi_atts[zhi]['害'] == liunian_zhi:
            print(f"{liunian_zhi}{zhi}相害")
        if liunian_zhi in zhi_atts[zhi]['会']:
            print(f"{liunian_zhi}{zhi}相会")
        if zhi_atts[zhi]['破'] == liunian_zhi:
            print(f"{liunian_zhi}{zhi}相破")

analyze_bazi_dayun(user_bazi, dayun_gz, liunian_gz)

def analyze_bazi_liuyue(user_bazi, liuyue_gz):
    user_gans = user_bazi.split()[0][0] + user_bazi.split()[1][0] + user_bazi.split()[2][0] + user_bazi.split()[3][0]
    user_zhis = user_bazi.split()[0][1] + user_bazi.split()[1][1] + user_bazi.split()[2][1] + user_bazi.split()[3][1]
    liuyue_gan, liuyue_zhi = liuyue_gz[0], liuyue_gz[1]
    
    result = f"流月天干{liuyue_gan}与日主关系：{ten_deities[me][liuyue_gan]}<br>"
    
    for i, gan in enumerate(user_gans):
        if ten_deities[gan]['合'] == liuyue_gan:
            result += f"{liuyue_gan}{gan}相合<br>"
        if ten_deities[gan]['冲'] == liuyue_gan:
            result += f"{liuyue_gan}{gan}相冲<br>"
    
    for i, zhi in enumerate(user_zhis):
        if liuyue_zhi in zhi_atts[zhi]['合']:
            result += f"{liuyue_zhi}{zhi}相合<br>"
        if zhi_atts[zhi]['冲'] == liuyue_zhi:
            result += f"{liuyue_zhi}{zhi}相冲<br>"
        if zhi_atts[zhi]['刑'] == liuyue_zhi or zhi_atts[zhi]['被刑'] == liuyue_zhi:
            result += f"{liuyue_zhi}{zhi}相刑<br>"
        if zhi_atts[zhi]['害'] == liuyue_zhi:
            result += f"{liuyue_zhi}{zhi}相害<br>"
        if liuyue_zhi in zhi_atts[zhi]['会']:
            result += f"{liuyue_zhi}{zhi}相会<br>"
        if zhi_atts[zhi]['破'] == liuyue_zhi:
            result += f"{liuyue_zhi}{zhi}相破<br>"
    
    return result.rstrip('<br>')

print("\n### 本年二十四节气与月份干支\n")

# 定义二十四节气
solar_terms = [
    "立春", "雨水", "惊蛰", "春分", "清明", "谷雨",
    "立夏", "小满", "芒种", "夏至", "小暑", "大暑",
    "立秋", "处暑", "白露", "秋分", "寒露", "霜降",
    "立冬", "小雪", "大雪", "冬至", "小寒", "大寒"
]

jieqi = a.thisYearSolarTermsDic

# 获取本年立春日期
lichun_date = datetime.datetime(current_year, jieqi['立春'][0], jieqi['立春'][1])

# 获取下一年立春日期
next_year = current_year + 1
next_lichun_date = datetime.datetime(next_year, cnlunar.Lunar(datetime.datetime(next_year, 1, 1), godType='8char').thisYearSolarTermsDic['立春'][0], cnlunar.Lunar(datetime.datetime(next_year, 1, 1), godType='8char').thisYearSolarTermsDic['立春'][1])

# 定义月份备注
month_notes = {
    2: "春节前后",
    3: "春暖花开",
    4: "春意盎然",
    5: "初夏时节",
    6: "夏至将至",
    7: "炎炎夏日",
    8: "秋意渐浓",
    9: "秋高气爽",
    10: "金秋十月",
    11: "深秋时节",
    12: "冬季来临",
    1: "寒冬腊月"
}

print("| 月份 | 干支 | 节气 | 日期 | 季节 | 每月注意事项 | 流月与八字关系 |")
print("|------|------|------|------|------|------|------|")

# 遍历从本年立春到下一年立春前的月份
current_date = lichun_date
while current_date < next_lichun_date:
    a = cnlunar.Lunar(current_date, godType='8char')
    month_gz = a.month8Char
    # 分析月份干支
    month_gan = month_gz[0]
    month_zhi = month_gz[1]
    
    # 分析天干
    gan_analysis = ten_deities[me][month_gan]
    
    # 分析地支
    zhi_analysis = ''
    for gan in zhi5[month_zhi]:
        zhi_analysis += f"{gan}{gan5[gan]}{zhi5[month_zhi][gan]}{ten_deities[me][gan]} "
    
    # 添加分析结果到注意事项
    # 获取当前月份的两个节气
    month = current_date.month
    year = current_date.year
    jieqi1_name = list(jieqi.keys())[2*month-2] if year == current_year else list(cnlunar.Lunar(datetime.datetime(year, 1, 1), godType='8char').thisYearSolarTermsDic.keys())[2*month-2]
    jieqi2_name = list(jieqi.keys())[2*month-1] if year == current_year else list(cnlunar.Lunar(datetime.datetime(year, 1, 1), godType='8char').thisYearSolarTermsDic.keys())[2*month-1]
    
    jieqi1_date = f"{year}-{a.thisYearSolarTermsDic[jieqi1_name][0]:02d}-{a.thisYearSolarTermsDic[jieqi1_name][1]:02d}"
    jieqi2_date = f"{year}-{a.thisYearSolarTermsDic[jieqi2_name][0]:02d}-{a.thisYearSolarTermsDic[jieqi2_name][1]:02d}"
    
    season = a.lunarSeason
    note = month_notes[month]
    note += f" 天干：{gan_analysis}，地支：{zhi_analysis}"
    
    # 调用analyze_bazi_liuyue函数
    liuyue_analysis = analyze_bazi_liuyue(user_bazi, month_gz)
    
    print(f"| {month:02d}月 | {month_gz} | {jieqi1_name} | {jieqi1_date} | {season} | {note} | {liuyue_analysis} |")
    print(f"|      |      | {jieqi2_name} | {jieqi2_date} |      |      |      |")
    
    # 移动到下一个月
    current_date = current_date + datetime.timedelta(days=32)
    current_date = current_date.replace(day=1)

print("\n注：月份干支以节气为界，可能与实际日历有1-2天的误差。")


sys.stdout = original_stdout
output_file.close()
print("输出已保存到 bazi_output.md 文件中。")