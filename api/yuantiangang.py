import datetime
from lunar_python import Lunar, Solar
# import pymysql
from commondata import *


class ShengChen:
    def __init__(self, date=datetime.datetime(1995, 6, 10, 2, 0, 0, 0)):
        self.date = date

        solar = Solar.fromYmdHms(date.year, date.month, date.day, date.hour, 0, 0)
        lunar = solar.getLunar()
        self.lunarData = lunar
        self.ba = lunar.getEightChar() 
    def hour_to_shichen(self):
        if self.date.hour not in range(0, 24):
            print('out of range')
            return False
        elif self.date.hour in [0, 23]:
            shichen = 0
        elif self.date.hour in [1, 2]:
            shichen = 1
        elif self.date.hour % 2 == 0:
            shichen = self.date.hour // 2
        else:
            shichen = (self.date.hour + 1) // 2
        return shichen

    def get_year_weight(self):
        for items in weight_of_year:
            if items["name"] == self.lunarData.getYearInGanZhiExact():
                return items["weight"]

    def get_month_weight(self):
        print()
        return weight_of_month[self.date.month - 1]

    def get_day_weight(self):
        return weight_of_day[self.date.day- 1]

    def get_hour_weight(self):
        return weight_of_hour[self.hour_to_shichen()]

    def get_total_weight(self):
        return self.get_hour_weight() + self.get_day_weight() + self.get_month_weight() + self.get_year_weight()


    def calculate(self):
        # print(self.lunarData.getYearInGanZhiExact())
        # print(self.lunarData.getMonthInGanZhiExact())
        # print(self.lunarData.getDayInGanZhiExact())
        # print(self.lunarData.getTimeInGanZhi())
        # print(self.get_total_weight())
        weight =  self.get_total_weight()
        lian = int(weight/10)
        qian = weight - lian *10
        print('袁天罡称骨：%d两%d钱' %(lian,qian))
        print(pizhu['{}两{}'.format(lian,qian)])
        # print('finish!')


if __name__ == '__main__':
    
    shengchen1 = ShengChen(datetime.datetime(1995, 10,29,8, 0, 0, 0)).calculate()
 