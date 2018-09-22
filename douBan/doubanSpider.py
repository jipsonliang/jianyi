import requests#请求库
from lxml import etree#解析库
#import json



class  Spider:
	def __init__(self):
		self.url = 'https://movie.douban.com/review/best/?start='
		#self.url ='https://www.douban.com/accounts/login?redir=https%3A%2F%2Fmovie.douban.com%2Freview%2Fbest%2F'
		self.headers = {"User-Agent" : "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;"}
		
		

	def douban_spider(self):
		for num in range(0,3):
			page = num*20
			
			#拼接完整的url
			fullurl = self.url + str(page)
			#发起请求
			#content = requests.get(fullurl,proxies = self.proxies,headers = self.headers).text
			content = requests.get(fullurl,headers = self.headers).text
			#print(content)
			#创建lxml对象
			html = etree.HTML(content)
			#每个电影分块
			node_list = html.xpath('//div[@class="review-list chart "]/div[@typeof="v:Review"]')

			#存放每个电影的结构/名称 推荐指数 影评 时间
			movie_body = []
			for items in node_list:

				#获取电影名
				litle = items.xpath(".//img/@title")[0]

				#推荐指数
				star = items.xpath(".//span/@title")
				if star == ['力荐']:
					nominate = '5'
				elif star == ['推荐']:
					nominate ='4'
				elif star == ['还行']:
					nominate = '3'
				elif star == ['较差']:
					nominate = '2'
				elif star == ['很差']:
					nominate = '1'
				else:
					nominate = '0'


				#有完整影评内容的链接
				content_url = items.xpath('.//div[@class="main-bd"]//h2//a/@href')[0]
				response= requests.get(content_url,headers = self.headers).text
				html = etree.HTML(response)

				#返回一个列表
				#content_list = html.xpath('//div[@class="review-content clearfix"]/p')[0].text
				content_list = html.xpath('//div[@class="review-content clearfix"]/p/text()')
				content = '\n'.join(content_list)

				#影评时间
				time = items.xpath('.//span[@property="v:dtreviewed"]')[0].text

				#影评结构
				movie_body =[litle,nominate,content,time]


				#print(litle )
				#print(type(nominate))
				#print(content_list)
				#print(time)
				self.writedata(movie_body)
				print('正在采集评论....')
		print('采集程序结束!')


	#把数据写入文档
	def writedata(self,movie_body):
		with open("D:/WebSpider/douban/movie.txt", "a",encoding='utf-8') as f:
			for temp in movie_body:
				if temp == movie_body[0]:
					new_temp ='电影名称: '+ temp +'\n'*2
				elif temp == movie_body[1]:
					new_temp = '推荐指数: '+ temp +'\n'*2
				elif temp == movie_body[2]:
					new_temp = '影评内容: \n' +temp +'\n'*2
				elif temp == movie_body[3]:
					new_temp = '评论时间: ' +temp +'\n'*3+'='*30+'\n'
				f.writelines(new_temp)

		'''
				movie_dict = {
					'①电影名称' : litle,
					'②推荐指数' : nominate,
					'③电影评论' : content_list,
					'④评论时间' : time
				}  
				print(movie_dict)
				with open("豆瓣影评.json", "a") as f:
					f.write(json.dumps(movie_dict, ensure_ascii= False).encode("utf-8")+ "\n")  '''


if __name__ == '__main__':
	spider_obj = Spider()
	spider_obj.douban_spider()
