#-*-coding:utf8 -*-
from django.shortcuts import render
from django.db import connection,transaction
import time
import os
from django.http import HttpResponseRedirect,HttpResponse
from django.core.context_processors import csrf

# Create your views here.




def signin(request):
    username = request.POST['user']
    password = request.POST['password']
    cursor = connection.cursor()
    sql = '''insert into webUser(username,password,createdt) 
    values (%s,%s,%s)'''
    print time.strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute(sql, [username,password,time.strftime('''%Y-%m-%d' %H:%M:%S''')])
    transaction.commit_unless_managed()
    ctx = {}
    ctx.update(csrf(request))
    return HttpResponseRedirect('/')

#文件上传
@transaction.commit_on_success
def fileUp(request):
    file_object = request.FILES.get('inputImage',None)
    nickname = request.POST['nick'] 
    headpath = request.POST['head']
    openid = request.POST['openid']
    describetion = request.POST['describe']
    print nickname,headpath,openid,describetion
    file_name = str(time.strftime('%Y-%m-%d %H:%M:%S'))+openid+"."+file_object.name.split('.')[-1]
	
    #sae文件代码上传
    from os import environ
    online = environ.get("APP_NAME", "") 
    if online:
        print "sae upload"
        import sae.const 
        print sae.const	
        access_key = sae.const.ACCESS_KEY  
        secret_key = sae.const.SECRET_KEY  
        appname = sae.const.APP_NAME  
        domain_name = "photofile"  #刚申请的domain            
        import sae.storage  
        s = sae.storage.Client()  
        ob = sae.storage.Object(file_object.read())  
        inputimage = s.put(domain_name, file_name, ob)   #文件上传路径 
    else:
        #本地上传
        print "local upload"
        file_path = os.path.join('/home/lpj/svn/photome/23/static/img/photo',file_name)
        inputimage = str('img/photo/')+file_name
        with open(file_path,'wb+') as file_head:
            file_head.write(file_object.read())	
		
    #execute sql
    cursor = connection.cursor()
    sql_webUser = '''insert into webUser (nickname,openid,headpath) values
          (%s,%s,%s)'''
    sql_photo = '''insert into photoInfo (webuserid,inputimage,describetion) values
                (%s,%s,%s)'''
    cursor.execute(sql_webUser,[nickname,openid,headpath])
    cursor.execute(sql_photo,[int(cursor.lastrowid),inputimage,describetion])
    return HttpResponseRedirect('/')
    #return render(request,'index.html',{'pagenum':1})


#search photo
"""
  pagenum 当前页数
  pageLength  每页显示的记录数量
  totalResult 总的结果集
  totalPageNum 需要显示的总页数
  prepage     上一页
  nextpage    下一页
"""
def index(request,pagenum=1):
    cursor = connection.cursor()
    print pagenum
    sqlCount = '''select count(*) from webUser w left join photoInfo p 
    on w.id = p.webuserid 
    '''
    #每页显示的记录数量,默认张图片
    pageLength = 4
    #获取总的集合
    cursor.execute(sqlCount)
    #print '总的集合',int(cursor.fetchone()[0])
    totalResult = int(cursor.fetchone()[0])
    totalPageNum = totalResult/pageLength+1

    prepage = int(pagenum) - 1
    nextpage = int(pagenum) + 1
    if nextpage>totalPageNum:nextpage=-1
    sql = '''select w.id,w.nickname,w.openid,w.headpath,p.inputimage,p.describetion,
    p.uploadDate from webUser w left join photoInfo p 
    on w.id = p.webuserid order by p.uploadDate desc limit %s,%s'''
    
    cursor.execute(sql,[(int(pagenum)-1)*pageLength,pageLength])

    #cursor.execute(sql)
    photo_list = []
    for item in cursor.fetchall():
        dic_list = {}
        dic_list['id'] = item[0]
        dic_list['nickname'] = item[1]
        dic_list['openid'] = item[2]
        dic_list['headpath'] = item[3]
        dic_list['inputimage'] = item[4]
        dic_list['describetion'] = item[5]
        dic_list['uploadDate'] = item[6]
        photo_list.append(dic_list)
    totalPageNumlist = []
    for i in xrange(totalPageNum):
        totalPageNumlist.append(i+1)

    return render(request,'index.html',
        {'photo_list':photo_list,'nextpage':nextpage,'prepage':prepage,'totalPageNumlist':totalPageNumlist,'pagenum':int(pagenum)})



def fileDownload(request,filepath):
    import urllib
    f = urllib.urlopen(filepath)
    data = f.read()
    f.close()
    
    response = HttpResponse(data,mimetype='application/octet-stream') 
    response['Content-Disposition'] = 'attachment; filename=%s' %filepath.split('/')[-1]
    return response





    




    
     
