"""
reference: https://zhuanlan.zhihu.com/p/32715324
"""

import json, re, os
import requests
from bs4 import BeautifulSoup
import pandas as pd 


if not os.path.exists('singer_info'):
	os.mkdir('singer_info')

if not os.path.exists('lyrics'):
	os.mkdir('lyrics')

headers = {
	"Accept": "application/json",
	"Accept-Encoding": "gzip, deflate, sdch, br",
	"Accept-Language": "en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,ja;q=0.2",
	"Cache-Control": "no-cache",
	"Connection": "keep-alive",
	"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36",
	##"X-Requested-With": "XMLHttpRequest",
}


def get_lyrics(singer_name, song_id):
	url = "https://music.163.com/api/song/lyric?id={}&lv=1&kv=1&tv=-1".format(song_id)
	json_response = requests.get(url, headers = headers)
	content = json_response.content
	text = json.loads(content.decode('utf-8'))["lrc"]["lyric"]
	
	patterns = [r"\[\d{2}:\d{2}.\d{2,3}\]", ".*\uff1a.*", ".*:.*"]
	for p in patterns:
		text = re.sub(p, '', text)
	
	with open("lyrics/{0}_{1}.txt".format(singer_name, song_id), 'w') as f:
		f.write(text.strip())


def get_song_ids_by_singer_id(singer_id, singer_name):
	url = "http://music.163.com/artist?id={}".format(singer_id)
	json_response = requests.get(url, headers = headers)
	html = json_response.text
	soup = BeautifulSoup(html)
	song_list = soup.find('ul', class_ = 'f-hide').find_all('a')
	with open("singer_info/{}.csv".format(singer_name), "w") as f:
		f.writelines("song_id,song_name\n")
		for ele in song_list:
			id_ = ele.get("href").split("=")[-1]
			name = ele.text
			f.writelines(",".join([id_, name]))
			f.writelines('\n')


def search_song_ids_by_singer_name(singer_name):
	url = "https://music.163.com/#/search/m/?s={}".format(singer_name)


def scrape_lyrics_by_singer(singer_name, singer_id):
	csv_file = "singer_info/{}.csv".format(singer_name)
	if not os.path.exists(csv_file):
		get_song_ids_by_singer_id(singer_id=singer_id, singer_name=singer_name)

	song_id = pd.read_csv(csv_file)["song_id"]
	for sid in song_id:
		try:
			get_lyrics(singer_name=singer_name, song_id=sid)
			print("success: {}".format(sid))
		except Exception as err:
			print("fail: {0}, err msg: {1}".format(sid, err))


# args = {"singer_id": 1050282, "singer_name": "房东的猫"}
# args = {"singer_id": 12138269, "singer_name": "毛不易"}
args = {"singer_id":5781, "singer_name":"薛之谦"}

scrape_lyrics_by_singer(**args)




