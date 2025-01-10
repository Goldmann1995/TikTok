from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import collections
import datetime
import sys
import cnlunar
from lunar_python import Lunar, Solar
from colorama import init
from yuantiangang import ShengChen
from datas import *
from sizi import summarys
from common import *
from yue import months
from gradio_client import Client
import re
import random
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/bazi', methods=['POST'])
def analyze_bazi():
    try:
        # 获取原始数据并解析
        raw_data = request.get_data().decode('utf-8')  # 解码二进制数据
        
        data = json.loads(raw_data)

        # 验证必需的字段
        required_fields = ['year', 'month', 'day', 'hour', 'name', 'gender']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    "success": False,
                    "error": f"Missing required field: {field}"
                }), 400

        # 获取参数
        year = str(data.get('year'))
        month = str(data.get('month'))
        day = str(data.get('day'))
        hour = str(data.get('hour'))
        name = data.get('name', '')
        is_female = data.get('gender') == 'female'
        
        # 性别
        sex = '女' if is_female else '男'
        
        # 使用公历
        solar = Solar.fromYmdHms(int(year), int(month), int(day), int(hour), 0, 0)
        lunar = solar.getLunar()
        
        # 获取今日的农历日期
        today = datetime.datetime.now()
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

        # 计算大运
        seq = Gan.index(gans.year)
        if is_female:
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

        # 获取运势起始时间
        yun = ba.getYun(not is_female)
        # 计算起运年龄
        start_age = yun.getStartSolar().getYear() - solar.getYear()
        # 计算当前年龄
        current_year = datetime.datetime.now().year
        current_age = current_year - solar.getYear()  # 使用实际出生年份
        # 找出当前所在大运
        current_dayun = None
        for i, item in enumerate(dayuns):
            dayun_start_age = start_age + i * 10
            dayun_end_age = dayun_start_age + 9
            if dayun_start_age <= current_age <= dayun_end_age:
                current_dayun = item
                break
        
        # 计算八字强弱
        bazi_strength = calculate_bazi_strength(me, zhis, lunar)
        # 根据八字强弱确定喜用神
        if bazi_strength == "强":
            xi_yong = [ten_deities[me]['被克'], ten_deities[me]['生']]
            ji_yong = [ten_deities[me]['本'], ten_deities[me]['生我']]
        else:
            xi_yong = [ten_deities[me]['本'], ten_deities[me]['生我']]
            ji_yong = [ten_deities[me]['克'], ten_deities[me]['被克']]

        # 判断对应的十神
        shens = {}
        for gan in Gan:
            shens[gan] = ten_deities[me][gan]
        for zhi in Zhi:
            shens[zhi] = ten_deities[me][max(zhi5[zhi], key=zhi5[zhi].get)]
        
        # 获取今日的幸运颜色、幸运数字和幸运方向
        today_direction = today_cnlunar.get_luckyGodsDirection()
        if bazi_strength == "强":
            bazi_strength = "身强"
            today_direction = [item for item in today_direction if "阳贵" not in item]
        else:
            today_direction = [item for item in today_direction if "阴贵" not in item]
        
        direction_dict = {}
        for item in today_direction:
            if '神' in item:
                god = item[:2]  # 取前两个字符（如"喜神"）
                direction = item[2:]  # 取剩余部分作为方向
            else:  # 处理"阳贵"和"阴贵"的情况
                god = item[:2]  # 取前两个字符（如"阳贵"）
                direction = item[2:]  # 取剩余部分作为方向
            direction_dict[god] = direction
        keys_to_update = [key for key in direction_dict.keys() if "阳贵" in key or "阴贵" in key]
        for key in keys_to_update:
            if "阳贵" in key:
                direction_dict[key.replace("阳贵", "贵人")] = direction_dict.pop(key)
            elif "阴贵" in key:
                direction_dict[key.replace("阴贵", "贵人")] = direction_dict.pop(key)

        today_direction = direction_dict
        today_good = random.sample(today_cnlunar.goodThing, min(3, len(today_cnlunar.goodThing)))
        today_bad = random.sample(today_cnlunar.badThing, min(3, len(today_cnlunar.badThing)))
        
        # 读取颜色数据
        with open('../public/colors.json', 'r', encoding='utf-8') as f:
            colors_data = json.load(f)

        # 获取幸运色和幸运数字
        lucky_color = get_lucky_color(colors_data, scores)
        lucky_numbers = get_lucky_numbers(gans, zhis, today_gans, today_zhis)
        
        # 构建返回结果
        result = {
            "success": True,
            "data": {
                "basic": {
                    "name": name,
                    "gender": sex,
                    "solar_date": f"{solar.getYear()}年{solar.getMonth()}月{solar.getDay()}日",
                    "lunar_date": f"{lunar}",
                    "birth_time": f"{zhis.time}时",
                    "start_age": start_age,
                    "current_age": current_age,
                    "current_dayun": current_dayun,
                    "bazi_strength": bazi_strength,
                    "喜用": xi_yong,
                    "忌用": ji_yong,
                    "命局特点": f"您的八字中日主为{me}{ten_deities[me]['本']}，生于{zhis[1]}月，{zhi_wuhangs[zhis[1]]}旺则身{bazi_strength}"
                },
                "bazi": {
                    "year": {
                        "gan": gans.year,
                        "zhi": zhis.year,
                        "shen": gan_shens[0],
                        "canggan": zhi5[zhis.year],
                        "zhi_shens": zhi_shens[0]
                    },
                    "month": {
                        "gan": gans.month,
                        "zhi": zhis.month,
                        "shen": gan_shens[1],
                        "canggan": zhi5[zhis.month],
                        "zhi_shens": zhi_shens[1]
                    },
                    "day": {
                        "gan": gans.day,
                        "zhi": zhis.day,
                        "shen": "元女" if is_female else "元男",
                        "canggan": zhi5[zhis.day],
                        "zhi_shens": zhi_shens[2]
                    },
                    "time": {
                        "gan": gans.time,
                        "zhi": zhis.time,
                        "shen": gan_shens[3],
                        "canggan": zhi5[zhis.time],
                        "zhi_shens": zhi_shens[3]
                    }
                },
                "analysis": {
                    "wuxing_scores": scores,
                    "dayuns": dayuns,
                    "起运时间": yun.getStartSolar().toFullString(),
                    "十神": shens
                },
                "daily_fortune": {
                    "scores": new_relations,
                    "lucky": {
                        "color": lucky_color,
                        "numbers": lucky_numbers,
                        "direction": today_direction
                    },
                    "activities": {
                        "good": today_good,
                        "bad": today_bad
                    }
                }
            }
        }
        return jsonify(result)
        
    except Exception as e:
        print("错误:", str(e))
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/generate_report', methods=['POST'])
def generate_report():
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                "success": False,
                "error": "无效的请求数据"
            }), 400

        # 连接 Qwen 模型
        client = Client("Qwen/Qwen2.5-72B-Instruct")


        shi_shen = {
            "正财": {
                "含义": "代表正当的财富来源，如工资、奖金等。正财多表示收入稳定，但也可能意味着花费较大。对于女性而言，正财还象征着丈夫。",
                "喜用神": "正财能够制衡日主，增加财富和稳定感，适合从事金融和商业类工作。",
                "忌神": "正财过多可能导致财务压力，影响健康和情绪。"
            },
            "偏财": {
                "含义": "指非固定的、偶然性的收入，如投资收益、彩票中奖等。偏财旺盛通常意味着财源广进，但同时也容易出现破财的风险。男性命中的偏财有时也代表异性缘。",
                "喜用神": "偏财能够增加意外之财，适合从事投资和投机类工作。",
                "忌神": "偏财过多可能导致财务风险，容易破财。"
            },
            "正官": {
                "含义": "象征权力、地位和规范，与职业、工作有关。正官多的人往往责任感强，适合从事公务员、教师等行业。对于女性来说，正官还代表父亲或权威人物。",
                "喜用神": "正官能够制衡日主，增加权威和责任感，适合从事公务员和教育类工作。",
                "忌神": "正官过多可能导致压力过大，影响心理健康。"
            },
            "七杀": {
                "含义": "表示竞争、挑战和压力。七杀重者性格刚烈，喜欢冒险，适合创业或从事需要强烈斗志的职业。在某些情况下，七杀也可能带来困扰甚至灾祸。",
                "喜用神": "七杀能够增加竞争力和挑战精神，适合从事创业和竞争激烈的工作。",
                "忌神": "七杀过多可能导致危险和灾祸，影响身体健康。"
            },
            "食神": {
                "含义": "代表享受、创造和个人才能。食神旺的人通常有艺术天赋，生活充满乐趣。此外，食神还与健康状况相关联。",
                "喜用神": "食神能够生助日主，增强体质和智慧，适合从事创意和艺术类工作。",
                "忌神": "食神过多可能导致贪吃懒做，缺乏进取心。"
            },
            "伤官": {
                "含义": "表示反叛、创新和破坏力。伤官重者思维敏捷，富有创造力，但有时也会因过于直言不讳而得罪他人。在极端情况下，伤官可能造成健康问题。",
                "喜用神": "伤官能够生助日主，增强创造力和领导力，适合从事科研和管理类工作。",
                "忌神": "伤官过多可能导致叛逆和不稳定，容易与人发生冲突。"
            },
            "劫财": {
                "含义": "象征兄弟姐妹、同辈朋友或者竞争者。劫财多的人容易与人争执，钱财不易积累。同时，劫财也有助于锻炼人的合作精神和社会交往能力。",
                "喜用神": "劫财能够生助日主，增加兄弟姐妹的支持，适合从事团队合作类工作。",
                "忌神": "劫财过多可能导致争执和矛盾，影响个人发展。"
            },
            "比肩": {
                "含义": "类似于劫财，但比肩更侧重于同类、伙伴的概念。比肩旺者个性独立，善于团结他人共同奋斗。在事业上，比肩有助于形成团队合作。",
                "喜用神": "比肩能够生助日主，增加自信和竞争力，适合从事领导和管理类工作。",
                "忌神": "比肩过多可能导致竞争激烈，影响团队合作。"
            },
            "偏印": {
                "含义": "代表母亲、长辈或导师。偏印旺的人通常得到家庭的支持，学业顺利。然而，过多的偏印也可能导致过分依赖他人。",
                "喜用神": "偏印能够生助日主，增加智慧和保护，适合从事艺术和创意类工作。",
                "忌神": "偏印过多可能导致固执和偏激，影响人际关系。"
            },
            "正印": {
                "含义": "象征智慧、学问和庇护。正印多的人聪明好学，有较强的求知欲。正印还能带来精神上的安慰和支持。",
                "喜用神": "正印能够生助日主，增加智慧和保护，适合从事学术和研究类工作。",
                "忌神": "正印过多可能导致依赖性强，缺乏独立性。"
            }
        }
        requestData = {
            '用户八字信息': data.get('reportData'),
            '十神分析字典': shi_shen
        }
        
        prompts = data.get('prompts')
        specialQuestion = data.get('specialQuestion')
        topic = data.get('topic')
        # 准备提示词
        current = datetime.datetime.now()
        solar = Solar.fromYmdHms(int(current.year), int(current.month), int(current.day), int(current.hour), 0, 0)
        lunar = solar.getLunar()
        a = cnlunar.Lunar(datetime.datetime(current.year + 1, 3, 1), godType='8char')
        jieqi = a.thisYearSolarTermsDic
        nian = lunar.getYear()
        # 获取本年立春日期
        lichun_date = datetime.datetime(nian + 1, jieqi['立春'][0], jieqi['立春'][1])

        # 获取下一年立春日期
        next_lichun_date = datetime.datetime(nian +2, cnlunar.Lunar(datetime.datetime(nian +2, 1, 1), godType='8char').thisYearSolarTermsDic['立春'][0], cnlunar.Lunar(datetime.datetime(nian +2, 1, 1), godType='8char').thisYearSolarTermsDic['立春'][1])
        # 获取后一个立春日期
        after_next_lichun_date = datetime.datetime(nian +3, cnlunar.Lunar(datetime.datetime(nian +3, 1, 1), godType='8char').thisYearSolarTermsDic['立春'][0], cnlunar.Lunar(datetime.datetime(nian +3, 1, 1), godType='8char').thisYearSolarTermsDic['立春'][1])
        
        def get_month_gan_zhi(lichun_date, after_next_lichun_date):
            current_date = lichun_date
            month_gan_zhi = []
            while current_date < after_next_lichun_date:
                a = cnlunar.Lunar(current_date, godType='8char')
                month_gz = a.month8Char
                month_gan_zhi.append(month_gz)
                current_date = current_date + datetime.timedelta(days=32)
                current_date = current_date.replace(day=1)
            month_gan_zhi = list(dict.fromkeys(month_gan_zhi))
            return month_gan_zhi
        #今年
        month_gan_zhi_nian = get_month_gan_zhi(lichun_date, next_lichun_date)
        month_gan_zhi_nian = list(dict.fromkeys(month_gan_zhi_nian))
        month_gan_zhi_nian = {f"{nian+1}年流月": list(dict.fromkeys(month_gan_zhi_nian))}
        #明年
        # month_gan_zhi_nian1 = get_month_gan_zhi(next_lichun_date, after_next_lichun_date)
        # month_gan_zhi_nian1 = list(dict.fromkeys(month_gan_zhi_nian1))
        # month_gan_zhi_nian1 = {f"{nian+2}年流月": list(dict.fromkeys(month_gan_zhi_nian1))}
        # 获取本年立春日期
        if topic == 'profession':
            system_prompt = f"""
            你是一个专业的命理分析师，请根据以下用户信息生成详细的命理分析报告：
            1.开头需要简要阐述用户信息，姓名，八字，性别，命局特点都可以在query中解析获取。
            2.针对命局特点，喜用神，忌用神，进行简略讲解，并给出建议。
            3.今年和明年流月信息如下：
            {month_gan_zhi_nian}
            4.当前时间是{current}，农历日期是{lunar}，请基于天干地支分析今年和明年的命理趋势。请先提供今年的分析，再分析明年的命理情况。

            请根据今年的流月{month_gan_zhi_nian}来进行详细分析。你可以参考类似的格式进行呈现：
            月份+节气+注意事项
            你可以把注意事项写的更加具体一些。
            你将使用我提供的数据中的八字十神信息，并结合天干地支来进行命理分析。请注意以下几点：
            1. 第一部分数据包含客户信息，第二部分数据是参考的十神分析字典。请结合字典中的内容进行分析，但不要简单照抄。
            2. 增加你对每项分析的个人理解和见解，不要重复原文中的内容。
            3. 请确保你的回答用中文表达，且富有专业性和易于理解。            
            4.特殊问题的回答应该在基本信息下面
            5.文档最下方不要出现“希望这份命理分析报告对您有所帮助，祝您生活幸福、事业顺利！”
            6.文档最后应该写“当前内容仅供娱乐中探索，不等于专业测评，不代表价值评判，无任何现实教导意义。若有需求，请点击右下角contact。”
            """
        else:
            system_prompt = f"""
            你是一个专业的命理分析师，请根据以下用户信息生成详细的命理分析报告：
            1.开头需要简要阐述用户信息，姓名，八字，性别，命局特点都可以在query中解析获取。
            2.针对命局特点，喜用神，忌用神，进行简略讲解，并给出建议。
        
            你将使用我提供的数据中的八字十神信息，并结合天干地支来进行命理分析。请注意以下几点：
            1. 第一部分数据包含客户信息，第二部分数据是参考的十神分析字典。请结合字典中的内容进行分析，但不要简单照抄。
            2. 增加你对{topic}分析的个人理解和见解，不要重复原文中的内容。
            3. 请确保你的回答用中文表达，且富有专业性,但是易于没有命理知识的人的理解。
            4.特殊问题的回答应该在基本信息下面
            5. 总结内容中包括以下内容{prompts}
            6.文档最下方不要出现“希望这份命理分析报告对您有所帮助，祝您生活幸福、事业顺利！”
            7.文档最后应该写“当前内容仅供娱乐中探索，不等于专业测评，不代表价值评判，无任何现实教导意义。若有需求，请点击右下角contact。”
            """
        
        if specialQuestion:
            system_prompt = f"""
            你是一个专业的命理分析师，请根据以下用户信息生成详细的命理分析报告,
            你将使用我提供的数据中的八字十神信息，并结合天干地支来进行命理分析。请注意以下几点：
            1.开头需要简要阐述用户信息，姓名，八字，性别，命局特点都可以在query中解析获取。
            2.针对命局特点，喜用神，忌用神，进行简略讲解，并给出建议。
            3.特殊问题的回答应该在基本信息下面
            4.文档最下方不要出现“希望这份命理分析报告对您有所帮助，祝您生活幸福、事业顺利！”
            5.文档最后应该写“当前内容仅供娱乐中探索，不等于专业测评，不代表价值评判，无任何现实教导意义。若有需求，请点击右下角contact。”
            同时，请参考以下特殊问题（如果有）来进一步结合当天的天干地支分析命理情况详细分析，当前时间是{current}，农历日期是{lunar}：{specialQuestion}
            """
        
        # 调用模型生成报告
        report_sections = client.predict(
            query=json.dumps(requestData, ensure_ascii=False),  # 用户数据
            history=[],  # 历史对话
            system=system_prompt,  # 系统提示词
            api_name="/model_chat"
        )


        return jsonify({
            "success": True,
            "data": {
                "sections": report_sections,
                "timestamp": datetime.datetime.now().isoformat()
            }
        })

    except Exception as e:
        print("生成报告错误:", str(e))
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500





if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)