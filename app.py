import string
import time
import pyodbc
import os
import redis
import timeit
import hashlib
import pickle
from flask import Flask, Request, render_template, request, flash
import random

app = Flask(__name__, template_folder="templates")
connection = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};Server=tcp:adbsai.database.windows.net,1433;Database=adb;Uid=sainath;Pwd=Shiro@2018;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30')
cursor = connection.cursor()

r = redis.StrictRedis(host='adb-quiz3.redis.cache.windows.net', port=6380, db=0,
                      password='bGWVXkw0gkglji3NxJ2c4dapdnXSxI8dtAzCaKsPnF8=', ssl=True)



@app.route('/', methods=['POST', 'GET'])
def Hello():
    return render_template('index.html')


@app.route('/Question10a', methods=['GET', 'POST'])
def Question10a():
    cursor = connection.cursor()    
    num1 = request.form.get("RangeStart")
    num2 = request.form.get("RangeEnd")  
    starttime = timeit.default_timer()
    query_str = "select b.id, b.net, b.place, a.nst from [ds-2] a join [dsi-1] b on a.id = b.id where a.nst >="+num1+" and a.nst <= "+num2
    cursor.execute(query_str)    
    data = cursor.fetchall()
    time = timeit.default_timer() - starttime
    return render_template('Question10a.html', data = data, time  = time)  



@app.route('/Question10b', methods=['GET', 'POST'])
def Question10b():
    cursor = connection.cursor()    
    n = request.form.get("N")
    net = request.form.get("Net")  
    off = str(random.randint(0,9))
    starttime = timeit.default_timer()
    query_str = "select top "+n+" * from (select b.id, b.net, b.place, a.nst from [ds-2] a join [dsi-1] b on a.id = b.id where b.net = '"+net+"' ORDER BY b.id OFFSET "+off+" ROWS) a1"
    cursor.execute(query_str)    
    data = cursor.fetchall()
    time = timeit.default_timer() - starttime
    return render_template('Question10a.html', data = data, time = time)  


@app.route('/Question11', methods=['GET', 'POST'])
def Question11():
    cursor = connection.cursor()

    num1 = request.form.get("RangeStart")
    num2 = request.form.get("RangeEnd")  

    n = request.form.get("N")
    net = request.form.get("Net") 
    off = str(random.randint(0,9))

    t = int(request.form.get("T")) 
    timeList1 = []
    timeList2 = []
    sum = 0
    # 10a
    for i in range(0,t):
        starttime = timeit.default_timer()
        query_str = "select b.id, b.net, b.place, a.nst from [ds-2] a join [dsi-1] b on a.id = b.id where a.nst >="+num1+" and a.nst <= "+num2
        cursor.execute(query_str)    
        data = cursor.fetchall()
        time = timeit.default_timer() - starttime
        timeList1.append(time)
        sum = sum + time

    # off = str(random.randint(0,9))
    for i in range(0,t):
        starttime = timeit.default_timer()
        query_str = "select top "+n+" * from (select b.id, b.net, b.place, a.nst from [ds-2] a join [dsi-1] b on a.id = b.id where b.net = '"+net+"' ORDER BY b.id OFFSET "+off+" ROWS) a1"
        cursor.execute(query_str)    
        data = cursor.fetchall()
        time = timeit.default_timer() - starttime
        timeList2.append(time)
        sum = sum + time

    return render_template('Question11.html', time1 = timeList1, time2= timeList2, total = sum)  


@app.route('/ShowNLargest', methods=['GET', 'POST'])
def showDetails():
    cursor = connection.cursor()    
    num1 = request.form.get("RangeStart")
    num2 = request.form.get("RangeEnd")   
    n = request.form.get("N")

    
    starttime = timeit.default_timer()
    query_str = "select top "+n+" * from ds2b a where a.D <="+num2+" and a.D >="+num1    
    cursor.execute(query_str+" ORDER BY RAND()")
    data1 = cursor.fetchall()
    time1 = timeit.default_timer() - starttime


    starttime = timeit.default_timer()
    query_str = "select top "+n+" * from ds2b a where a.D <="+num2+" and a.D >="+num1    
    cursor.execute(query_str+" ORDER BY RAND()")
    data2 = cursor.fetchall()
    time2 = timeit.default_timer() - starttime


    starttime = timeit.default_timer()
    query_str = "select top "+n+" * from ds2b a where a.D <="+num2+" and a.D >="+num1    
    cursor.execute(query_str+" ORDER BY RAND()")
    data3 = cursor.fetchall()
    time3 = timeit.default_timer() - starttime


    starttime = timeit.default_timer()
    query_str = "select top "+n+" * from ds2b a where a.D <="+num2+" and a.D >="+num1    
    cursor.execute(query_str+" ORDER BY RAND()")
    data4 = cursor.fetchall()
    time4 = timeit.default_timer() - starttime

    starttime = timeit.default_timer()
    query_str = "select top "+n+" * from ds2b a where a.D <="+num2+" and a.D >="+num1    
    cursor.execute(query_str+" ORDER BY RAND()")
    data5 = cursor.fetchall()
    time5 = timeit.default_timer() - starttime

    times = [time1,time2,time3,time4, time5]
    
    return render_template('ShowNLargest.html',data1 = data1, data2 = data2, data3 = data3, data4 = data4, data5 = data5, time = times)  



@app.route('/ShowNLargestCache', methods=['GET', 'POST'])
def showDetailsCache():
    cursor = connection.cursor()    
    num1 = request.form.get("RangeStart")
    num2 = request.form.get("RangeEnd")   
    n = request.form.get("N")

    if( not r.get(n+num1+num2)):
        starttime = timeit.default_timer()
        query_str = "select top "+n+" * from ds2b a where a.D <="+num2+" and a.D >="+num1    
        cursor.execute(query_str+" ORDER BY RAND()")
        data1 = cursor.fetchall()
        time1 = timeit.default_timer() - starttime
        r.set(n+num1+num2, pickle.dumps(data1))
    else:
        starttime = timeit.default_timer()
        data1 = pickle.loads(r.get(n+num1+num2))
        time1 = timeit.default_timer() - starttime

    if( not r.get(n+num1+num2)):
        starttime = timeit.default_timer()
        query_str = "select top "+n+" * from ds2b a where a.D <="+num2+" and a.D >="+num1    
        cursor.execute(query_str+" ORDER BY RAND()")
        data2 = cursor.fetchall()
        r.set(n+num1+num2, pickle.dumps(data2))
        time2 = timeit.default_timer() - starttime
    else:
        starttime = timeit.default_timer()
        data2 = pickle.loads(r.get(n+num1+num2))
        time2 = timeit.default_timer() - starttime

    if( not r.get(n+num1+num2)):
        starttime = timeit.default_timer()
        query_str = "select top "+n+" * from ds2b a where a.D <="+num2+" and a.D >="+num1    
        cursor.execute(query_str+" ORDER BY RAND()")
        data3 = cursor.fetchall()
        r.set(n+num1+num2, pickle.dumps(data3))
        time3 = timeit.default_timer() - starttime
    else:
        starttime = timeit.default_timer()
        data3 = pickle.loads(r.get(n+num1+num2))
        time3 = timeit.default_timer() - starttime


    if( not r.get(n+num1+num2)):
        starttime = timeit.default_timer()
        query_str = "select top "+n+" * from ds2b a where a.D <="+num2+" and a.D >="+num1    
        cursor.execute(query_str+" ORDER BY RAND()")
        data4 = cursor.fetchall()
        r.set(n+num1+num2, pickle.dumps(data4))
        time4 = timeit.default_timer() - starttime
    else:
        starttime = timeit.default_timer()
        data4 = pickle.loads(r.get(n+num1+num2))
        time4 = timeit.default_timer() - starttime
    if( not r.get(n+num1+num2)):
        starttime = timeit.default_timer()
        query_str = "select top "+n+" * from ds2b a where a.D <="+num2+" and a.D >="+num1    
        cursor.execute(query_str+" ORDER BY RAND()")
        data5 = cursor.fetchall()
        r.set(n+num1+num2, pickle.dumps(data5))
        time5 = timeit.default_timer() - starttime
    else:
        starttime = timeit.default_timer()
        data5 = pickle.loads(r.get(n+num1+num2))
        time5 = timeit.default_timer() - starttime

    times = [time1,time2,time3,time4, time5]
    
    return render_template('ShowNLargestCache.html',data1 = data1, data2 = data2, data3 = data3, data4 = data4, data5 = data5, time = times)  

@app.route('/Question13', methods=['GET', 'POST'])
def ZTime():
    cursor = connection.cursor()   
    num1 = request.form.get("RangeStart")
    num2 = request.form.get("RangeEnd") 
    
    query_str = "select T, count(*) from ds2b where T<="+num2+" AND T>="+num1+"  group by T"
    cursor.execute(query_str)
    data1 = cursor.fetchall()

    newList = []
    # newList.append(['T', 'Count'])
    for i in data1:
        newList.append([i[0],i[1]])

    print("new List",newList)
    return render_template('pieChart.html', data = newList)  


 


# @app.route('/Question11', methods=['GET', 'POST'])
# def Question11():
#     cursor = connection.cursor()    
#     net = request.form.get("net")
#     min_mag = request.form.get("magMin")   
#     max_mag = request.form.get("magMax")
#     newMag = request.form.get("newMag")

#     query_str = "UPDATE  dbo.ds SET mag ="+newMag+" where id in (SELECT a.id from dbo.ds a join dbo.dsi b on a.id = b.id where b.net = '"+net+"' ) and mag <=" +max_mag+" and mag>="+min_mag 
#     cursor.execute(query_str)
#     rows_effected = cursor.rowcount
#     cursor.commit()
#     print("rows ",rows_effected)
#     return render_template('Question11.html', rows_count = rows_effected, net = net)  


@app.route('/searachquakebylat', methods=['GET', 'POST'])
def searachquakebylat():
    lat1 = request.form.get("lat1")
    lat2 = request.form.get("lat2")
    long1 = request.form.get("long1")
    long2 = request.form.get("long2")
    print("Incoming dates : ", lat1, lat2)
    cursor.execute("select * from ds inner join dsi on ds.id = dsi.id where latitude between '{}' and '{}' and longitude between '{}' and '{}' ;".format(lat1,lat2,long1,long2))
    result = cursor.fetchall()
    return render_template('searachquakebylat.html', list1= result)


if __name__ == '__main__':    
    app.run()

