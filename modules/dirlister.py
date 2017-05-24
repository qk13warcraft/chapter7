 # -*- coding: utf-8 -*-
import os

def run(**args):
	"""
	列举当前目录下的所有文件，在开发的所有模块都应定义一个run函数并提供可变数量的参数
	好处：可使用相同的方法加载模块、提供充分的可拓展能力
	"""
	print "[*] In dirlister module."
	files = os.listdir(".")
	return str(files)
