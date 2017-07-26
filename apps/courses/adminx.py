#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/7/26 17:30
# @Author  : Nice
# @Site    :
import xadmin
from .models import Course, CourseResource, Lession, Video


class CourseAdmin(object):
	list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums']
	search_fields = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums']
	list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums']


class LessionAdmin(object):
	list_display = ['course', 'name', 'add_time']
	search_fields = ['course', 'name']
	# 外键名称搜索 __双下划线
	list_filter = ['course__name', 'name', 'add_time']


class VideoAdmin(object):
	list_display = ['lesson', 'name', 'add_time']
	search_fields = ['lesson', 'name']
	list_filter = ['lesson', 'name', 'add_time']


class CourseResourceAdmin(object):
	list_display = ['course', 'name', 'download', 'add_time']
	search_fields = ['name', 'desc', 'download', ]
	search_fields = ['name', 'desc', 'download', 'add_time']


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lession, LessionAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
