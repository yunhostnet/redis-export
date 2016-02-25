#!/usr/bin/env python
#coding:utf8
#------------------------------------------------
#Redis Export Import
#Version:1.0.0
#Author zp
#Created 2016-01-06
#------------------------------------------------
Version="1.0.0"
from progressbar import *
import redis
from os import path
from optparse import OptionParser
from sys import exit,argv

class RDS(object):
	def __init__(self,ip,port,passwd,db):
		self.ip = ip
		self.port = port
		self.passwd = passwd
		self.db = db
		if (self.passwd==None)or(self.passwd=="")or(self.passwd=="None"):
			self.conn = redis.StrictRedis(host=self.ip,port=self.port,db=self.db)
		else:
			print self.passwd
			self.conn = redis.StrictRedis(host=self.ip,port=self.port,password=self.passwd,db=self.db)
	def Export(self,outfile):
		try:
			Keys = self.conn.keys()
			try:
				dict = {}
				KEYS = 0
				widgets = ['Processed:  ',Counter(),"/%s"%(len(Keys)),' Keys (',Timer(),')']
				pbar = ProgressBar(widgets=widgets)
				if path.exists(outfile):
					exis = raw_input("The '%s' file already exists.Do you want to overwrite it?(Y/N)"%outfile)
					if(exis=='y' or exis=='Y'):
						pass
					else:
						exit(0)
				staff = open(outfile,'w+')
				for i in pbar(Keys):
					lines = {}
					if(self.conn.type(i)=="hash"):
						values = self.conn.hgetall(i)
						lines[i] = values
						dict["hash_%s"%KEYS] = lines
					elif(self.conn.type(i)=="set"):
						value = [v for v in self.conn.smembers(i)]
						lines[i] = value
						dict["set_%s"%KEYS] = lines
					else:
						value = self.conn.get(i)
						lines[i] = value
						dict["string_%s"%KEYS] = lines
					KEYS += 1
				staff.write(str(dict))
				staff.close()
				print "\033[32;1mExport Suceess Total Keys:%s \033[0m"%(KEYS)
			except Exception,e:
				print "\033[31;1m[+ERROR]\033[0m:%s.\n\033[31;1m[+ERROR]\033[0m:key type only support ['hash','string','set']"%(str(e))
		except Exception,e:
			print "\033[31;1m[+ERROR]\033[0m:Please check Network and IP or Port.\nInfo:%s"%(str(e))
	def Import(self,infile):
		staff = open(infile,'rb')
		fileread = staff.read()
		try: 
			KEYS = 0
			widgets = ['Processed:  ',Counter(),' Keys (',Timer(),')']
			pbar = ProgressBar(widgets=widgets)
			for k,v in pbar(eval(fileread).items()):
				if(k.split('_')[0]=="hash"):
					key = ''.join(v.keys())
					value = v.values()[0]
					self.conn.hmset(key,value)
				elif(k.split('_')[0]=="set"):
					key =  v.keys()[0]
					for k in v.values()[0]:
						self.conn.sadd(key,k)
				else:
					key = v.keys()[0]
					value = v.values()[0]
					self.conn.set(key,value)
				KEYS += 1
			staff.close()
			print("\033[32;1mImport Suceess  Total keys:%s \033[0m"%(KEYS))
		except Exception,e:
			print("\033[31;1m[+ERROR]\033[0m:%s."%(str(e)))
	def Count(self):
		Keys = len(self.conn.keys())
		return Keys
if __name__ == '__main__':
	p = OptionParser(version=Version)
	p.add_option("-H","--host",dest="host",default="127.0.0.1",help='Server hostname (default: 127.0.0.1).')
	p.add_option("-P","--port",dest="port",default=6379,help='Server port (default: 6379).')
	p.add_option("-p","--passwd",dest="passwd",help='Password to use when connecting to the server.')
	p.add_option("-f","--file",dest="file",default="export.json",help='import and export file.')
	p.add_option("-t","--type",dest="type",help='import or export or count type.')
	p.add_option("-d","--db",dest="db",default=0,type=int,help='Database number (default: 0).')
	(option,args)=p.parse_args()
	try:
		P = RDS(ip=option.host,port=option.port,passwd=option.passwd,db=option.db)
		if(option.type == "export"):
			P.Export(outfile=option.file)
		elif(option.type == "import"):
			P.Import(infile=option.file)
		elif(option.type == "count"):
			print(P.Count())
		else:
			print(p.parse_args(['-h']))
			exit(1)
	except Exception,e:
		print("\033[31;1m %s \033[0m"%str(e))
		exit(1)
