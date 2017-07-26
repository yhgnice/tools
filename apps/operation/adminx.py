#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/7/26 18:54
# @Author  : Nice
# @Site    :
import xadmin
from .models import CourseComments, UserProfile, UserAsk, UserCourse, UserFavorite, UserMessage


class CourseCommentsAdmin(object):
	list_display = ['user', 'course', 'comments', 'add_time']
	search_fields = ['user', 'course', 'comments', ]
	list_filter = ['user', 'course', 'comments', 'add_time']


class UserProfileAdmin(object):
	list_display = ['nick_name', 'birday', 'gender', 'address', 'mobile', 'image']
	search_fields = ['nick_name', 'birday', 'gender', 'address', 'mobile']
	list_filter = ['nick_name', 'birday', 'gender', 'address', 'mobile', ]


class UserAskAdmin(object):
	list_display = ['name', 'mobile', 'course_name', 'add_time']
	search_fields = ['name', 'mobile', 'course_name']
	list_filter = ['name', 'mobile', 'course_name', 'add_time']


class UserCourseAdmin(object):
	list_display = ['user', 'course', 'add_time']
	search_fieldks = ['user', 'course']
	list_filter = ['user', 'course', 'add_time']


class UserFavoriteAdmin(object):
	list_display = ['user', 'fav_id', 'fav_type', 'add_time']
	search_fields = ['user', 'fav_id', 'fav_type']
	list_filter = ['user', 'fav_id', 'fav_type', 'add_time']


class UserMessageAdmin(object):
	list_display = ['user', 'message', 'has_read', 'add_time']
	search_fields = ['user', 'message', 'has_read']
	list_filter = ['user', 'message', 'has_read', 'add_time']


xadmin.site.register(CourseComments, CourseCommentsAdmin)
# xadmin.site.register(UserProfile, UserProfileAdmin)
xadmin.site.register(UserAsk, UserAskAdmin)
xadmin.site.register(UserCourse, UserCourseAdmin)
xadmin.site.register(UserFavorite, UserFavoriteAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)
