#_*_coding:utf-8_*_
import urllib.request
import json
from city import station_names
import requests

class search_tickets:     
    def __init__(self):
        self.train_date = ""
        self.from_station = ""
        self.to_station = ""
        self.from_code = ""
        self.to_code = ""
        self.seak = ""
        self.secret_key = {}
        self.train_location = {}
        self.train_no = {}

        self.headers = {
            'Referer':'https://kyfw.12306.cn/otn/leftTicket/init',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36'
        }

    def get_page(self,train_date,from_code,to_code,seak):
        seak = int(seak)
        param = {
            'leftTicketDTO.train_date':train_date,
            'leftTicketDTO.from_station':from_code,
            'leftTicketDTO.to_station':to_code,
            'purpose_codes':'ADULT'
        }
        
        url ='https://kyfw.12306.cn/otn/leftTicket/query?' + urllib.parse.urlencode(param)
        response =requests.get(url,headers=self.headers)
        result = json.loads(response.text)
        result_list = result.get('data').get('result')
        tikie = []
        
        for lis in result_list:
            a = lis.split('|')
            print(a[2],a[15])
            self.secret_key.setdefault(a[3],a[0])
            self.train_location.setdefault(a[3],a[15])
            self.train_no.setdefault(a[3],a[2])
            if a[seak] =='无' or not a[seak]:
                continue
            else:
                tikie.append(a[3])
                if a[seak] != "有" and int(a[seak]) > 0:
                    print("有票的车次：",a[3]," 出发时间是:",a[8]," 到达时间:",a[9]," 历时:",a[10],"还有",a[seak],"张票")
                else:
                    print("有票的车次：",a[3]," 出发时间是:",a[8]," 到达时间:",a[9]," 历时:",a[10],"余票充足")
        if tikie == None or not tikie:
            print("符合您要求的车次暂时无票")   
        '''
        【1】列车信息：列车停运 [3]车次，【4】出发的车站，【5】到达的车站，【8】出发时间，【9】到达时间，【10】历时，【31】一等座 【30】二等座  【26】无座 【33】动卧 【29】硬座 【28】硬卧
        '''
    def main(self):
        # self.session = sessions
        city = {}
        for i in station_names.split('@'):
            if i:
                city[i.split('|')[1]] = i.split('|')[2]
        self.train_date = input("请输入出发日期：例2018-08-06 ：")
        self.from_station = input("请输入出发城市:例茂名 ：")
        self.to_station = input("请输入目的地城市：例梅州 ：")
        self.seak = input("请输入座位类型：例【31】一等座 【30】二等座  【26】无座 【33】动卧 【29】硬座 【28】硬卧 ：")
        # 找出城市对应的字母编码
        if self.from_station in city.keys():
            self.from_code = city[self.from_station]
        if self.to_station in city.keys():
            self.to_code = city[self.to_station]
        self.get_page(self.train_date,self.from_code,self.to_code,self.seak)

if __name__ == '__main__':
    t = search_tickets()
    t.main()


