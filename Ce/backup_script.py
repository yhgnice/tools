#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2014/5/26 17:53
# @Author  : Nice
# @Site    :

import time
import os
import sys

date = time.strftime('%Y%m%d')
directory = '/data/upgrade'
d_dir = os.path.join(directory, date)
d_file = "system_backup.tar.gz"

s_dir = ['/etc/', '/opt/']

full_dir = os.path.join(d_dir, d_file)

print full_dir

if os.path.exists(d_dir) == False:
	os.makedirs(d_dir)
else:
	print "the dir %s is exists !" % d_dir

tar_cmd = 'tar -czvf %s %s' % (full_dir, ' '.join(s_dir))
# tar_cmd = 'zip   %s -r %s' % (full_dir, ' '.join(s_dir))
print tar_cmd

if os.system(tar_cmd) == 0:
	print 'This Backup System Files %s success !' % d_file
else:
	print 'This Backup System Files \033[32m %s   \033[0m Faild !' % d_file
