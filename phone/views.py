#-*-coding:utf-8-*-

from django.shortcuts import render
from django.db import connection,transaction
# Create your views here.
def first_phone(request):
   return render(request,'phone.html')

#查询所有的手机项目
def all(request):
   cursor = connection.cursor()  #获得一个游标
   cursor.execute("select name from phone") #执行sql语句
   #transaction.commit_unless_managed()  #提交事务作增删的时候用
   phone_list = [raw[0] for raw in cursor.fetchall()]
   return render(request,'phone.html',{'phone_list':phone_list,'end':'手机列表'})


def signin(request):
    username = request.POST['user']
    password = request.POST['password']
    cursor = connection.cursor()
    cursor.execute('''insert into webUser (username,password,createdt) 
    values (%s,%s,%s)''' %(username,password,datetime.datetime.now()))
    transaction.commit_unless_managed()
    return render(request,'index.html',{'result':'success'})
