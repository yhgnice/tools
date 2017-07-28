#!coding:utf-8
from django.shortcuts import render

from django.views.generic import View
from .models import CourseOrg, CityDict


# Create your views here.


class OrgView(View):
	"""课程机构"""
	
	def get(self, request):
		all_orgs = CourseOrg.objects.all()  # 课程机构
		all_city = CityDict.objects.all()  # 城市
		org_nums = all_orgs.count()
		
		return render(request, "org-list.html", {
			'all_orgs': all_orgs,
			'all_citys': all_city,
			'org_nums': org_nums,
		})
