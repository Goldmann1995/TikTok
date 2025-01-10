import datetime
from lunar_python import Solar, Lunar
import collections
import cnlunar
from ganzhi import *
import json

# 使用公历
solar = Solar.fromYmdHms(int(1995), int(6), int(10), int(2), 0, 0)
lunar = solar.getLunar()

# 获取今日的农历日期
today = datetime.datetime.now()+datetime.timedelta(days=19)
today_solar = Solar.fromYmdHms(today.year, today.month, today.day, today.hour, 0, 0)
today_lunar = today_solar.getLunar()
today_cnlunar = cnlunar.Lunar(today, godType='8char')
# 获取八字
day = lunar
ba = lunar.getEightChar()
today_ba = today_lunar.getEightChar()
# 获取干支
gans = collections.namedtuple("Gans", "year month day time")(
year=ba.getYearGan(), 
month=ba.getMonthGan(),
day=ba.getDayGan(),
time=ba.getTimeGan()
)

zhis = collections.namedtuple("Zhis", "year month day time")(
year=ba.getYearZhi(),
month=ba.getMonthZhi(),
day=ba.getDayZhi(),
time=ba.getTimeZhi()
)

today_gans = collections.namedtuple("Gans", "year month day time")(
year=today_ba.getYearGan(), 
month=today_ba.getMonthGan(),
day=today_ba.getDayGan(),
time=today_ba.getTimeGan()
)
today_zhis = collections.namedtuple("Zhis", "year month day time")(
year=today_ba.getYearZhi(),
month=today_ba.getMonthZhi(),
day=today_ba.getDayZhi(),
time=today_ba.getTimeZhi()
)
# 获取运势信息
me = gans.day

month = zhis.month
alls = list(gans) + list(zhis)
zhus = [item for item in zip(gans, zhis)]

# 计算神煞
gan_shens = []
for seq, item in enumerate(gans):    
    if seq == 2:
        gan_shens.append('--')
    else:
        gan_shens.append(ten_deities[me][item])

# 地支神煞
zhi_shens = []
for item in zhis:
    d = zhi5[item]
    zhi_shens.append(ten_deities[me][max(d, key=d.get)])

# 计算五行分数
scores = {"金":0, "木":0, "水":0, "火":0, "土":0}
for item in gans:  
    scores[gan5[item]] += 5

for item in list(zhis) + [zhis.month]:  
    for gan in zhi5[item]:
        scores[gan5[gan]] += zhi5[item][gan]

total_score = sum(scores.values())
for key in scores:
    scores[key] /= total_score

today_scores = {"金":0, "木":0, "水":0, "火":0, "土":0}
# 计算今日的五行分数
for item in today_gans:  
    today_scores[gan5[item]] += 5

for item in list(today_zhis) + [today_zhis.month]:  
    for gan in zhi5[item]:
        today_scores[gan5[gan]] += zhi5[item][gan]

# 归一化五行分数
total_score = sum(today_scores.values())
for key in today_scores:
    today_scores[key] /= total_score

scores = {k: (today_scores.get(k, 0) + scores.get(k, 0)) * 100 for k in set(today_scores) | set(scores)}

new_relations = {}
for key in scores.keys():
    relation_name = wu_xing_relations[ten_deities[me].inverse[key]]  # 获取关系名称
    new_relations[relation_name] = int(scores[key])  # 使用关系名称作为新的key

print(new_relations)




