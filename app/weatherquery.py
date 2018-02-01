# coding: utf-8
import requests
import sqlite3

# sql = """
# 	CREATE TABLE weather(
# 	id INTEGER NOT NULL,
#  	city VARCHAR(80),
# 	text_day VARCHAR(80),
# 	text_night VARCHAR(80),
# 	low VARCHAR(80),
# 	high VARCHAR(80)
# 	)
# """
# c.execute(sql)
# c.commit()

def get_weather(location):
	query_result = ''
	API = "https://api.seniverse.com/v3/weather/daily.json"
	LANGUAGE = "zh-Hans"
	KEY = "ygnfdic5sis9nfpt"
	UNIT = "c"
	we_da = {}
	result = requests.get(API, params={
	    'key': KEY,
	    'location': location,
	    'language': LANGUAGE,
	    'unit': UNIT
	}, timeout=5)
	if result.status_code == 200:
		rep_data = result.json()
		# print(result)
		# print(rep_data)
		results = rep_data.get('results')
		daily = results[0].get('daily')
		# print(daily)
		# 今天天气
		day = daily[0].get('date')
		weather = daily[0].get('text_day') # 今天天气情况,「0」表示今天
		# night0 = daily[0].get('text_night')
		low = daily[0].get('low')
		# high0 = daily[0].get('high')
		# wind = daily[0].get('wind_direction')

		# ins_data = [(1,location,day0,night0,low0,high0)]
		# c.executemany('INSERT INTO weather(id,city,text_day,text_night,low,high) VALUES(?,?,?,?,?,?)', ins_data)
		# conn.commit()
		# # today = "\n今天天气：\n"+location+"白天：{}\n夜晚：{}\n气温：{}～{}\n风向：{}".format(day0,night0,low0,high0,wind)
		# today = f"""今日：白天{day0}，夜晚{night0}，气温：{low0}~{high0}|"""
		# # 明天天气
		# day1 = daily[1].get('text_day')# 今天天气情况,「0」表示今天
		# night1 = daily[1].get('text_night')
		# low1 = daily[1].get('low')
		# high1 = daily[1].get('high')
		# wind = daily[1].get('wind_direction')
		# # tomorrow = "\n明天天气预报：\n"+location+"白天：{}\n夜晚：{}\n气温：{}～{}\n风向：{}".format(day1,night1,low1,high1,wind)
		# tomorrow = f"""明天：白天{day1}，夜晚{night1}，气温：{low1}~{high1}|"""
		# # 后日天气
		# day2 = daily[2].get('text_day')
		# night2 = daily[2].get('text_night')
		# low2 = daily[2].get('low')
		# high2 = daily[2].get('high')
		# wind = daily[2].get('wind_direction')
		# # after_tom = "\n后天天气预报：\n"+location+"白天：{}\n夜晚：{}\n气温：{}～{}\n风向：{}".format(day2,night2,low2,high2,wind)
		# after_tom = f"""后天：白天{day2}，夜晚{night2}，气温：{low2}~{high2}"""
		# query_result = today + tomorrow + after_tom
		weather_str = f"""{day},{location}:{weather},{low}"""
		print(day,location,weather,low)
		print(weather_str)
		return day,location,weather,low,weather_str
	else:
		weather_str = '查询不到该城市天气信息，请输入正确的城市名称'
		return weather_str
# get_weather("深圳")
