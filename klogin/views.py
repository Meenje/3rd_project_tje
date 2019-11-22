# Create your views here.
from django.conf import settings

from django.shortcuts import *

# Create your views here.
from django.views.generic import *

from klogin.models import *

from klogin.db_work.crawling_stock_info import crawling_today

from datetime import datetime

import sqlite3


def main_view(request):
    return render(request, 'home/main.html')


def login(request):
    return render(request, 'home/login.html')


# class main_view2(ListView):
#     model = infostock
#     template_name = 'home/main.html'
#
#     # 005930삼성꺼만 갖고 온다
#     def get_queryset(self):
#         #present = crawling_today(self.kwargs['stock_code'])
#         #pre_dic = {list : present}
#         result = infostock.objects.filter(stock_code=self.kwargs['stock_code']).order_by('-date')[:500]
#         #print(result['QuerySet'])
#         return result


def main_view2(request, stock_code):
    if stock_code == 'like':
        data = request.POST
        check = data['check']
        code = data['stock_code']
        uid = find_uid(request.user.id)
        if check == 'insert':
            Favorite = favorite(uid=uid, stock_code=code)
            Favorite.save()
        else:
            favorite.objects.get(uid=uid, stock_code=code).delete()
        return HttpResponse()
    elif stock_code == 'write':
        uid = find_uid(request.user.id)
        data = request.POST
        text = data['text']
        yn = Note.objects.filter(uid=uid)
        if len(yn)==0:
            note = Note(uid=uid, text=text)
            note.save()
        else:
            note = Note.objects.get(uid=uid)
            note.text = text
            note.save()
        return HttpResponse()
    else:
        now = datetime.now()
        today = str(now.year) + str(now.month) + str(now.day)
        data = infostock.objects.filter(stock_code=stock_code).order_by('-date')[:500]
        names = scode.objects.filter(stock_code=stock_code)
        present = crawling_today(stock_code)
        all_names = scode.objects.all()
        predict = predicted_by_ts.objects.filter(stock_code=stock_code, date=today)
        uid = find_uid(request.user.id)
        exist = favorite.objects.filter(uid=uid, stock_code=stock_code)
        check = True
        if len(exist) == 0:
            check = False

        favorite_list = favorite.objects.filter(uid=uid)

        note = Note.objects.filter(uid=uid)

        news = naver_news(names[0].stock_name)

        list = {'stock_info': data, 'present': present, 'name': names, 'all': all_names, "predict": predict,
                "check": check, "favorite": favorite_list, "news":news, "note":note}

        return render(request, 'home/main.html', list)


def like(request):
    pass


def find_uid(id):
    conn = sqlite3.connect("C:\\Users\\Administrator\\PycharmProjects\\project_test_kakao_view1\\db.sqlite3")
    cur = conn.cursor()
    sql = "select uid from socialaccount_socialaccount where user_id = ?"
    cur.execute(sql, (id,))
    uid = cur.fetchone()[0]
    conn.commit()
    conn.close()
    return uid

## 네이버 api
import urllib.request

def naver_news(keyword):
    client_id = "GBu0Dm8nFSnJ2eno3DXh"
    client_secret = "UfXf6vZJWr"
    encText = urllib.parse.quote(keyword)
    url = "https://openapi.naver.com/v1/search/news?query=" + encText # json 결과
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()

    if(rescode==200):
        response_body = response.read()
        return eval(response_body.decode('utf-8'))
    else:
        return("Error Code:" + rescode)
