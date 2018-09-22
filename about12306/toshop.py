#_*_coding:utf-8_*_
import requests
import re
import os
import json
import datetime
import time
from PIL import Image
from json import loads
import urllib.request
from urllib import parse
import getpass
from Search import search_tickets
import http.cookiejar as cookielib
from city import station_names
import random

 
class LoginTic(object):
    def __init__(self):
        self.headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36",
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': 'https://kyfw.12306.cn',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept': 'application/json, text/javascript, */*; q=0.01'
        }
        # 创建一个网络请求session实现登录验证
        self.session = requests.session()
        self.cookies = {}
        self.secret_key = {}
        self.cookie = {}
        self.loginInfo = ""
        self.tk = ""
        self.uamtk = ""
        self.reSubmitTk = ""
        self.leftTicketStr = ""
        self.keyIsChange = ""
        self.passengerAllInfoList = []
        self.passengerNameList = []
        self.passengerIdList = []
        self.passengerPhoneList = []

        self.train_date = ""
        self.from_station = ""
        self.to_station = ""
        self.from_code = ""
        self.to_code = ""
        self.seak = ""
        self.secret_key = {}
        self.train_location = {}
        self.train_no = {}
 
    # 获取验证码图片
    def getImg(self):
        url = "https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand"
        response = self.session.get(url=url,headers=self.headers,cookies=self.cookies,verify=False)
        # 把验证码图片保存到本地
        with open('img.jpg','wb') as f:
            f.write(response.content)
        # 用pillow模块打开并解析验证码,这里是假的，自动解析以后学会了再实现
        try:
            im = Image.open('img.jpg')
            # 展示验证码图片，会调用系统自带的图片浏览器打开图片，线程阻塞
            im.show()
            # 关闭，只是代码关闭，实际上图片浏览器没有关闭，但是终端已经可以进行交互了(结束阻塞)
            im.close()
        except:
            print('请输入验证码')
        #=======================================================================
        # 根据打开的图片识别验证码后手动输入，输入正确验证码对应的位置，例如：2,5
        # ---------------------------------------
        #         |         |         |
        #    0    |    1    |    2    |     3
        #         |         |         |
        # ---------------------------------------
        #         |         |         |
        #    4    |    5    |    6    |     7
        #         |         |         |
        # ---------------------------------------
        #=======================================================================
        captcha_solution = input('请输入验证码位置，以","分割[例如2,5]:')
        return captcha_solution
 
    # 验证结果
    def checkYanZheng(self,solution):
        # 分割用户输入的验证码位置
        soList = solution.split(',')
        # 由于12306官方验证码是验证正确验证码的坐标范围,我们取每个验证码中点的坐标(大约值)
        yanSol = ['35,35','105,35','175,35','245,35','35,105','105,105','175,105','245,105']
        yanList = []
        for item in soList:
            print(item)
            yanList.append(yanSol[int(item)])
        # 正确验证码的坐标拼接成字符串，作为网络请求时的参数
        yanStr = ','.join(yanList)
        checkUrl = "https://kyfw.12306.cn/passport/captcha/captcha-check"
        data = {
            'login_site':'E',           #固定的
            'rand':'sjrand',            #固定的
            'answer':yanStr    #验证码对应的坐标，两个为一组，跟选择顺序有关,有几个正确的，输入几个
        }
        # 发送验证
        cont = self.session.post(url=checkUrl,data=data,headers=self.headers,cookies=self.cookies,verify=False)
        # 返回json格式的字符串，用json模块解析
        dic = loads(cont.content)
        code = dic['result_code']
        # 取出验证结果，4：成功  5：验证失败  7：过期
        if str(code) == '4':
            return True
        else:
            return False
 
    # 发送登录请求的方法
    def loginTo(self):
        # 用户输入用户名，这里可以直接给定字符串
        userName = input('Please input your userName:')
        # 用户输入密码，这里也可以直接给定
        # pwd = raw_input('Please input your password:')
        # 输入的内容不显示，但是会接收，一般用于密码隐藏
        pwd = getpass.getpass('Please input your password:')
        loginUrl = "https://kyfw.12306.cn/passport/web/login"
        data = {
            'username':userName,
            'password':pwd,
            'appid':'otn'
        }
        result = self.session.post(url=loginUrl,data=data,headers=self.headers,cookies=self.cookies,verify=False)
        dic = loads(result.content)
        print(result.content)
        mes = dic['result_message']
        # 结果的编码方式是Unicode编码，所以对比的时候字符串前面加u,或者mes.encode('utf-8') == '登录成功'进行判断，否则报错
        if mes == '登录成功':
            print('恭喜你，登录成功，可以购票!')
        else:
            print('对不起，登录失败，请检查登录信息!')
            return False
        if 'uamtk' in dic.keys():
            self.uamtk = dic['uamtk']

        url2 = 'https://kyfw.12306.cn/passport/web/auth/uamtk'
        data2 = {
            "appid": "otn",
            '_json_att':""
        }
        # Func12306.cookies['uamtk'] = Func12306.uamtk
        response2 = self.session.post(url=url2, data=data2, headers=self.headers,cookies=self.cookies,verify=False)
        print("url:uamtk",self.session.cookies)
        try:
            dic2 = loads(response2.content)
        except:
            return "NetWorkError"
        resultCode2 = dic['result_code']
        resultMsg2 = dic['result_message']
        self.loginInfo = resultMsg2
        if resultCode2 == 0:
            print('验证通过')
        else:
            return "authFail"

        if 'newapptk' in dic2.keys():
            self.tk = dic2["newapptk"]
            # Func12306.cookies.pop('uamtk')
            # Func12306.cookies['tk'] = Func12306.tk

        url3 = 'https://kyfw.12306.cn/otn/uamauthclient'
        data3 = {
            "tk": self.tk,
            '_json_att': "",
        }
        response3 = self.session.post(url=url3, data=data3, headers=self.headers,cookies=self.cookies,verify=False)
        try:
            dic3 = loads(response3.content)
        except:
            return "NetWorkError"
        resultCode3 = dic3['result_code']
        resultMsg3 = dic3['result_message']
        self.loginInfo = resultMsg3
        if resultCode3 == 0:
            print("LoginSuccessful")
            return True
        else:
            return False

    def check_user(self):
        url = 'https://kyfw.12306.cn/otn/login/checkUser'
        data = {
            "_json_att": ""
        }
        self.headers["Cache-Control"] = "no-cache"
        self.headers["If-Modified-Since"] = "0"
        self.headers["Referer"] = "https://kyfw.12306.cn/otn/leftTicket/init"
        self.headers['Host'] = "kyfw.12306.cn"
        self.headers['Origin'] = "https://kyfw.12306.cn"
        response = self.session.post(url=url, data=data, headers=self.headers,cookies=self.cookies,verify=False)
        try:
            dic = loads(response.text)
        except:
            return "NetWorkError"
        if dic['data']['flag'] == True:
            print("用户在线验证成功")
            return True
        else:
            print(dic['data']['flag'])
            print('检查到用户不在线，请重新登陆')
            return False
    # 获取 REPEAT_SUBMIT_TOKEN
    def confirm_passenger(self):
        url = 'https://kyfw.12306.cn/otn/confirmPassenger/initDc'
        data = {"_json_att": ''}
        response = self.session.post(url=url, data=data, headers=self.headers,cookies=self.cookies,verify=False)
        try:
            self.reSubmitTk = re.findall('globalRepeatSubmitToken = \'(\S+?)\'',response.text)[0]
            self.keyIsChange = re.findall('key_check_isChange\':\'(\S+?)\'',response.text)[0]
            self.leftTicketStr = re.findall('leftTicketStr\':\'(\S+?)\'',response.text)[0]
        except:
            print("获取KEY失败")
            return False
        return True
    def get_passenger_info(self):
        url = 'https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs'
        data = {
            "_json_att": "",
            "REPEAT_SUBMIT_TOKEN": self.reSubmitTk
        }

        response = self.session.post(url=url, data=data, headers=self.headers,cookies=self.cookies,verify=False)

        try:
            dic = loads(response.content)
        except:
            print("NetWorkError")
            return False

        if dic['messages'] != []:
            if dic['messages'][0] == '系统忙，请稍后重试':
                print("系统繁忙，请稍后再试")
                return False
        self.passengerAllInfoList = dic['data']['normal_passengers']
        for a in self.passengerAllInfoList:
            self.passengerNameList.append(a['passenger_name'])
            self.passengerIdList.append(a['passenger_id_no'])
            self.passengerPhoneList.append(a['mobile_no'])
        return True     

    def submit_order(self,seak):
        url = 'https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest'
        data = {"secretStr": parse.unquote(self.secret_key[seak]),
                 "train_date": self.train_date,
                 "back_train_date": self.train_date,
                 "tour_flag": "dc",
                 "purpose_codes": "ADULT",
                 "query_from_station_name": self.from_station,
                 "query_to_station_name": self.to_station,
                 "undefined": ""
                 }
        response = self.session.post(url=url, data=data, headers=self.headers,cookies=self.cookies, verify=False)
        try:
            dic = loads(response.content)
            print(dic)
        except:
            return "NetWorkError"

        if dic['status']:
            print('提交订单成功')
            return True
        elif dic['messages'] != []:
            if dic['messages'][0] == "车票信息已过期，请重新查询最新车票信息":
                print('车票信息已过期，请重新查询最新车票信息')
                return False
        else:
            print("提交失败")
            return False

    def check_order(self, passengersList):
        url = 'https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo'
        passengerTicketStr = ""
        oldPassengerStr = ""
        for a in passengersList:
            passengerTicketStr += "1,0,1,{},1,{},{},N_".format(self.passengerNameList[a], self.passengerIdList[a], self.passengerPhoneList[a])
            oldPassengerStr += "{},1,{},1_".format(self.passengerNameList[a], self.passengerIdList[a])
        data = {
            "cancel_flag": "2",
            "bed_level_order_num": "000000000000000000000000000000",
            "passengerTicketStr": passengerTicketStr,
            "oldPassengerStr": oldPassengerStr,
            "tour_flag": "dc",
            "randCode": "",
            "whatsSelect": "1",
            "_json_att": "",
            "REPEAT_SUBMIT_TOKEN": self.reSubmitTk
        }
        response = self.session.post(url=url, data=data, headers=self.headers,cookies=self.cookies, verify=False)
        try:
            dic = loads(response.content)
        except:
            print("NetWorkError")
            return False
        if dic['data']['submitStatus'] is True:
            if dic['data']['ifShowPassCode'] == 'N':
                return 'N'
            if dic['data']['ifShowPassCode'] == 'Y':
                print("需要验证")
                captcha_solution2 = self.get_buy_image()
                return captcha_solution2
        else:
            print(dic['data']['errMsg'])
            print("验证身份信息错误")
            return False

    # 购买时的验证码  
    def get_buy_image(self):
        url = 'https://kyfw.12306.cn/otn/passcodeNew/getPassCodeNew?module=passenger&rand=randp'+random.random()
        response = self.session.get(url=url, headers=self.headers,cookies=self.cookies, verify=False)
        path = os.path.abspath('..')
        with open(path + "\\img.jpg", 'wb') as f:
            f.write(response.content)
        # 用pillow模块打开并解析验证码,这里是假的，自动解析以后学会了再实现
        try:
            im = Image.open('img.jpg')
            # 展示验证码图片，会调用系统自带的图片浏览器打开图片，线程阻塞
            im.show()
            # 关闭，只是代码关闭，实际上图片浏览器没有关闭，但是终端已经可以进行交互了(结束阻塞)
            im.close()
        except:
            print('请输入验证码')
        captcha_solution = input('请输入验证码位置，以","分割[例如2,5]:')
        return captcha_solution

    # 进入购票队列
    def get_queue_count(self,from_code,to_code,seak):
        url = 'https://kyfw.12306.cn/otn/confirmPassenger/getQueueCount'
        thatdaydata = datetime.datetime.strptime(self.train_date, "%Y-%m-%d")
        train_date = "{} {} {} {} 00:00:00 GMT+0800 (中国标准时间)".format(thatdaydata.strftime('%a'),
                                                                     thatdaydata.strftime('%b'), self.train_date.split('-')[2],
                                                                     self.train_date.split('-')[0])
        data = {
            "train_date": train_date,
            "train_no": self.train_no[seak],
            "stationTrainCode": seak,
            "seatType": "1",
            "fromStationTelecode": from_code,
            "toStationTelecode": to_code,
            "leftTicket": self.leftTicketStr,
            "purpose_codes": "00",
            "train_location": self.train_location[seak],
            "_json_att": "",
            "REPEAT_SUBMIT_TOKEN": self.reSubmitTk
        }
        response = self.session.post(url=url, data=data, headers=self.headers,cookies=self.cookies, verify=False)
        try:
            dic = loads(response.content)
        except:
            print("NetWorkError")
            return  False
        if dic['status']:
            print("进入队列成功")
            print(train_date)
            return True
        else:
            print("进入队列失败")
            return False    
    # 单人队列
    def confirm_single_for_queue(self, passengersList, clickList = ""):

        url = 'https://kyfw.12306.cn/otn/confirmPassenger/confirmSingleForQueue'
        passengerTicketStr = ""
        oldPassengerStr = ""
        for a in passengersList:
            # O二等座  1硬座   2 软座
            passengerTicketStr += "1,0,1,{},1,{},{},N_".format(self.passengerNameList[a], self.passengerIdList[a], self.passengerPhoneList[a])
            oldPassengerStr += "{},1,{},1_".format(self.passengerNameList[a], self.passengerIdList[a])
        if clickList is not None:
            code = ['35,35', '105,35', '175,35', '245,35', '35,105', '105,105', '175,105', '245,105']
            verifyList = []
            for a in clickList:
                verifyList.append(code[int(a)])
            codeList = ','.join(verifyList)
            print(codeList)
        else:
            codeList = ''

        data = {
            "passengerTicketStr": passengerTicketStr,
            "oldPassengerStr": oldPassengerStr,
            "randCode": "",
            "purpose_codes": "00",
            "key_check_isChange": self.keyIsChange,
            "leftTicketStr": self.leftTicketStr,
            "train_location": self.train_location[seak],
            "choose_seats": "",
            "seatDetailType": "000",
            "whatsSelect": "1",
            "roomType": "00",
            "dwAll": "N",
            "_json_att": "",
            "REPEAT_SUBMIT_TOKEN": self.reSubmitTk
        }
        response = self.session.post(url=url, data=data, headers=self.headers,cookies=self.cookies, verify=False)
        try:
            dic = loads(response.content)
            print(dic)
        except:
            print("NetWorkError")
            return False

        if 'data' in dic.keys():
            if dic['data']['submitStatus'] is True:
                print("提交订单成功")
                return True
            elif dic['data']['errMsg'] == "验证码输入错误！":
                print(dic['data']['errMsg'])
                return False

        else:
            print("提交订单失败")
            return False
    def wait_time(self):
        url = 'https://kyfw.12306.cn/otn/confirmPassenger/queryOrderWaitTime?random={}&tourFlag=dc&_json_att=&REPEAT_SUBMIT_TOKEN={}'.format(round(time.time()*1000),self.reSubmitTk)
        response2 = self.session.get(url=url, headers=self.headers,cookies=self.cookies,verify=False)
        time.sleep(2)
        response = self.session.get(url=url, headers=self.headers,cookies=self.cookies,verify=False)
        try:
            dic = loads(response.content)
            print(dic)
        except:
            print("NetWorkError")
        if dic['status']:
            if dic['data']['queryOrderWaitTimeStatus']:
                if dic['data']['waitTime'] > 0 :
                    return dic['data']['waitTime']
                elif dic['data']['waitTime'] == -1:
                    self.orderId = ''
                    self.orderId = dic['data']['orderId']
                    return dic['data']['waitTime']
                else:
                    return False
            else:
                return False
        else:
            return False
    def get_page(self,train_date,from_code,to_code,seak,from_station,to_station):
        seak = int(seak)
        param = {
            'leftTicketDTO.train_date':train_date,
            'leftTicketDTO.from_station':from_code,
            'leftTicketDTO.to_station':to_code,
            'purpose_codes':'ADULT'
        }
        try:
            self.cookies['_jc_save_fromDate'] = train_date
            self.cookies['_jc_save_fromStation'] = (parse.quote(from_station.encode('unicode_escape').decode('latin-1') + ',' + from_code).replace('\\','%')).upper().replace('%5CU', '%u')
            self.cookies['_jc_save_toDate'] = train_date
            self.cookies['_jc_save_toStation'] = (parse.quote(to_station.encode('unicode_escape').decode('latin-1') + ',' + to_code).replace('\\','%')).upper().replace('%5CU', '%u')
            self.cookies['_jc_save_wfdc_flag'] = "dc"
            self.cookies[' _jc_save_showIns']="true"
            print(self.cookies)
        except:
            return False
        try:
            url1 = 'https://kyfw.12306.cn/otn/leftTicket/log?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT'.format(train_date, from_code, to_code)
        except:
            return "wrongtype"
        response1 = self.session.get(url=url1, headers=self.headers,cookies=self.cookies, verify=False)
        try:
            dic1 = loads(response1.content)
        except:
            return False
        if dic1['status']:
            print("OK")
        else:
            return False
        url ='https://kyfw.12306.cn/otn/leftTicket/query?' + urllib.parse.urlencode(param)
        response =self.session.get(url,headers=self.headers,cookies=self.cookies)
        result = json.loads(response.text)
        result_list = result.get('data').get('result')
        tikie = []
        
        for lis in result_list:
            a = lis.split('|')
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
            return False
        else:
            return True   
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
        return self.get_page(self.train_date,self.from_code,self.to_code,self.seak,self.from_station,self.to_station)
if  __name__ == '__main__':
    # checkYanZheng('0,3')
    login = LoginTic()
    yan = login.getImg()
    search = search_tickets()
    chek = False
    #只有验证成功后才能执行登录操作
    while not chek:
        chek = login.checkYanZheng(yan)
        if chek:
            print('验证通过!')
        else:
            print('验证失败，请重新验证!')
            yan = login.getImg()
    result = login.loginTo()
    if result:
        info = login.main()
        if info:
            print("开始验证用户信息")
            is_user = login.check_user()
            # 我的账号已经保存有三个人的信息，所以默认为三张牌
            a = [0]
            if  is_user:
                seak = input("请选择您要购买的车次：")
                print("开始提交订单")
                msg1 = login.submit_order(seak)
                if msg1:
                    print("开始获取submitTK")
                    msg2 = login.confirm_passenger()
                    if msg2:
                        print("开始确认联系人")
                        msg3 = login.get_passenger_info()
                        if msg3:
                            print("开始确认订单")
                            status = login.check_order(a)
                            if status :
                                if status =='N':
                                    clickList = None
                                else:
                                    clickList = status
                                print("开始进入购票队列")
                                from_code = login.from_code
                                to_code = login.to_code
                                queue = login.get_queue_count(from_code,to_code,seak)
                                if queue :
                                    print("开始确认单人队列")
                                    single = login.confirm_single_for_queue(a,clickList)
                                    if single:
                                        result = login.wait_time()
                                        print(result)
                                        while result != -1 and result:
                                            time.sleep(1)
                                            result = login.wait_time()
                                            print(result)
                                        print("恭喜你购票成功，请在30分钟内前往官网完成付款！")
            else:
                print("用户信息验证失败,请重新登录")
    else:
        print("错误")
