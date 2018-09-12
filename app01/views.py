from django.shortcuts import render
from django.db.models import F,Q
from app01 import models

# Create your views here.


def rank(requset):
    if requset.method == "GET":

        #从数据库拉取用户的答题记录，根据胜率作排名，展现于前端页面。
        rank_list = models.Examination_Record.objects.order_by(F('pass_count')/F('examination_count'))
        return render(requset,"rank.html",{"rank_list":rank_list})