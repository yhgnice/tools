#!/usr/bin/env python
# -*- coding: utf-8 -*-
# version 1.0

import sys
import os
import xlrd
import MySQLdb
import configparser

reload(sys)
sys.setdefaultencoding('utf-8')

"""
功能：将Excel数据导入到MySQL数据库
version: i18n 去除
"""


def open_excel(file):
	try:
		data = xlrd.open_workbook(file)
		return data
	except Exception, e:
		print str(e)


def excel_table_byindex(file, colnameindex=0, by_index=0):
	try:
		data = open_excel(file)
		table = data.sheets()[by_index]
		nrows = table.nrows  # 行数
		data = []
		for rownum in range(3, nrows):
			row = table.row_values(rownum)
			if row:
				data.append(row)
			# break  # kill
		return data
	except Exception, e:
		print e


def getSchema(file, colnameindex=0, by_index=0):
	try:
		tableDic = {}
		t_ilsts = []
		data = open_excel(file)
		table = data.sheets()[by_index]
		row = table.row_values(0)  # 读取第一行数据标头
		if row:
			for line in row:
				t_ilsts.append(str(line).lower())
				tableDic[str(line).lower()] = []
				tableDic['yhglist'] = t_ilsts
		return tableDic
	except Exception, e:
		print e


def writesql(data):
	with open('dataErr.txt', 'a') as f:
		f.write(data)
		f.write('\n')
		f.close()


def getTableInfo(table_info):
	try:
		database = MySQLdb.connect(host=db_host, user=db_user, port=db_port, passwd=db_pwd, db=db_name,
		                           charset='utf8')
		cursor = database.cursor()
		sql = 'delete from  %s' % table_info

		# sql = 'truncate  %s;' % table_info
		descsql = 'desc %s ;' % table_info

		cursor.execute(sql)
		cursor.execute('commit')
		cursor.execute(descsql)
		result = cursor.fetchall()
		return result
		cursor.close()
		database.close()
	except Exception, e:
		print e


def getTable(table_info):
	tablledic = {}
	for line in table_info:
		if 'int' in line[1]:
			tablledic[str(line[0]).lower()] = [1, 0]
		else:
			tablledic[str(line[0]).lower()] = [0, 0]
	return tablledic


def insertData(table, sql):
	sqlinsert = 'replace  into %s set ' % table
	# sqlinsert = 'replace  into %s set ' % table
	sqlinsert += sql + ';'

	return sqlinsert


def dataDic(dataSc, data, tableSc, table, i18ndata):
	try:
		database = MySQLdb.connect(host=db_host, user=db_user, port=db_port, passwd=db_pwd, db=db_name,
		                           charset='utf8')
		cursor = database.cursor()

		result = {'Success': 0, 'Error': 0}
		for line in data:
			'''遍历数据'''

			for xline in range(len(line)):
				if dataSc['yhglist'][xline] in tableSc.keys():
					tableSc[dataSc['yhglist'][xline]][1] = (line[xline])
				# print len(tableSc.keys())

			sqlcommand = insertData(table=table, sql=sqlData(tableSc))

			try:
				res = cursor.execute(sqlcommand)
				
				cursor.execute('commit')
				if str(res) == '1':
					result['Success'] += 1
				elif str(res) == '2':
					result['Success'] += 1
				else:
					print res
			except Exception, e:
				writesql(sqlcommand)
				result['Error'] += 1
				print e
		
		if len(i18ndata) != 0:
			for tname in i18ndata:
				A_table = str(tname).split('_i18n')[0]
				sql = "update {0} set  {1}={2};".format(table, tname, A_table)
				cursor.execute(sql)
				cursor.execute('commit;')
		cursor.close()
		database.close()
	except Exception, e:
		return e
	finally:
		return result


def safe(s):
	return MySQLdb.escape_string(s)


def sqlData(resData):
	'''转换为sql语句'''
	# print resData
	tmplist = []
	try:
		for k, v in resData.items():
			if len(str(v[1])) != 0:
				if v[0] == 1:
					if not str(v[1]).isspace():
						tmp = "%s=%s" % (str(k), v[1])
						tmplist.append(' ' + tmp + ' ')
				else:
					if str(v[1]).endswith('.0') and str(v[1]).split('.0')[0].isdigit():
						tmp = "%s='%s'" % (str(k), str(v[1]).split('.0')[0])
						tmplist.append(' ' + tmp + ' ')
					else:
						if not str(v[1]).isspace():
							tmp = "%s='%s'" % (str(k), v[1])
							tmplist.append(' ' + tmp + ' ')

		return (','.join(tmplist))
	except Exception, e:
		print e


def config(cfgfile):
	cf = configparser.ConfigParser()
	cf.read(cfgfile)
	db_host = cf.get("database", "host")
	db_port = cf.getint("database", "port")
	db_user = cf.get("database", "user")
	db_pwd = cf.get("database", "password")
	db_name = cf.get("database", "name")
	db_charset = cf.get("database", "charset")
	return db_host, db_port, db_user, db_pwd, db_name, db_charset


def main(table):
	data = excel_table_byindex(file=table)  # excel data
	# 获取数据获取第一行数据表头
	excelSchema = getSchema(file=table)  # dict head
	table = os.path.basename(table).split('.')[0]
	# print excelSchema

	print  '{table}\ttotal data:'.format(table=table), len(data)
	# 获取数据库表结构信息
	table_info = getTableInfo(table)

	schemaTable = getTable(table_info=table_info)
 
	i18ndata = i18nfun(schemaTable)

	diff_col(table,excelSchema, schemaTable)
 
	result = dataDic(dataSc=excelSchema, data=data, tableSc=schemaTable, table=table, i18ndata=i18ndata)
	print  '{table}\tSuccess:'.format(table=table), result['Success'], 'Error:', result['Error']

	if result['Error'] > 0:
		print '\nPlease View the dataErr.txt file error message!!!'
	print '-' * 10, '{table} import is complete'.format(table=table), '-' * 10 + '\n'


def i18nfun(schemaTable):
	i18_list = []
	for vkeys in schemaTable.keys():
		if '_i18n' in vkeys:
			i18_list.append(vkeys)
	return i18_list


def diff_col(table,excelSchema, schemaTable):
	try:
		A = excelSchema.copy()
		B = schemaTable
		del A['yhglist']
		c = A.keys()
		d = B.keys()
		# print c,'\n',d
		for line in c:
			if line not in d:
				if not str(line).endswith('i18n'):
					info = '%s:数据库 不匹配:%s' % (table, line)
					writesql(info)
		for dx in d:
			if dx not in c:
				if not str(dx).endswith('i18n'):
					info = '%s:  excel 不匹配:%s' % (table, dx)
					writesql(info)
	except Exception, e:
		print e


def files(file):
	for xxy in file.split():
		xx = os.path.basename(xxy)
		while not os.path.isfile(xx.strip()):
			print ('No files found :{table}').format(table=xx)
			nxx = raw_input('please enter again tables:\n')
			if os.path.isfile(nxx.strip()):
				# print ' error ssss'
				main(table=nxx)
				xx = nxx
		main(table=xx)


def readfile():
	try:
		with open('tables.txt') as f:
			for line in f.readlines():
				if len(line.split()) == 0:
					continue

				if '.xls' in line.strip():
					file = os.path.join(filepath, os.path.join(dirc, line.strip()))
					main(file)
	except Exception, e:
		print e


def allFile():
	for line in os.listdir(dirc):
		if '.xls' in line:
			file = os.path.join(filepath, os.path.join(dirc, line))
			print file
			main(file)


if __name__ == '__main__':
	filepath = os.getcwd()
	# dirc = unicode('配置表目录').encode('utf-8')
	dirc = 'aj_chsz'
	dirup = u'文档'
 

	print filepath
	db_host, db_port, db_user, db_pwd, db_name, db_charset = config('db.conf')
	print (db_host, db_port, db_user, db_pwd, db_name, db_charset)

	if os.path.isfile('dataErr.txt'):
		os.remove('dataErr.txt')

	if os.path.isfile('tables.txt'):
		readfile()
	else:
		allFile()
