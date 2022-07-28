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
import hashlib
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

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

@app.route('/Question12', methods=['GET', 'POST'])
def Question12():
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
    print( r.exists("sai"+num1+num2))
    query_str = "select b.id, b.net, b.place, a.nst from [ds-2] a join [dsi-1] b on a.id = b.id where a.nst >="+num1+" and a.nst <= "+num2
    hashvalue = hashlib.sha224(query_str.encode('utf-8')).hexdigest()
    redis_key = "redis_cache:" + hashvalue
    for i in range(0,t):
        if( r.exists(redis_key) != 1):
            print("not coming")
            starttime = timeit.default_timer()            
            cursor.execute(query_str)    
            data = cursor.fetchall()
            r.set(redis_key, pickle.dumps(data))
            time = timeit.default_timer() - starttime
            timeList1.append(time)
            sum = sum + time
        else:
            starttime = timeit.default_timer()
            data = pickle.loads(r.get(redis_key))
            time = timeit.default_timer() - starttime
            timeList1.append(time)
            sum = sum + time

    # off = str(random.randint(0,9))
    query_str = "select top "+n+" * from (select b.id, b.net, b.place, a.nst from [ds-2] a join [dsi-1] b on a.id = b.id where b.net = '"+net+"' ORDER BY b.id OFFSET "+off+" ROWS) a1"
    hashvalue = hashlib.sha224(query_str.encode('utf-8')).hexdigest()
    redis_key = "redis_cache:" + hashvalue
    for i in range(0,t):
        if( r.exists(redis_key) != 1):
            print("not coming")
            starttime = timeit.default_timer()
            
            cursor.execute(query_str)    
            data = cursor.fetchall()
            r.set(redis_key,pickle.dumps(data))
            time = timeit.default_timer() - starttime
            timeList2.append(time)
            sum = sum + time
        else:
            starttime = timeit.default_timer()
            data = pickle.loads(r.get(redis_key))
            time = timeit.default_timer() - starttime
            timeList2.append(time)
            sum = sum + time

    return render_template('Question11.html', time1 = timeList1, time2= timeList2, total = sum)  

# @app.route('/Question13', methods=['GET', 'POST'])
# def plot_png():

#     cursor = connection.cursor()    
#     num1 = request.form.get("RangeStart")
#     num2 = request.form.get("RangeEnd")  
#     starttime = timeit.default_timer()
#     query_str = "select b.id, b.net, b.place, a.nst from [ds-2] a join [dsi-1] b on a.id = b.id where a.nst >="+num1+" and a.nst <= "+num2
#     cursor.execute(query_str)    
#     data = cursor.fetchall()
#     time = timeit.default_timer() - starttime
#     return render_template('Question10a.html', data = data, time  = time)  


#     fig = create_figure()
#     output = io.BytesIO()
#     FigureCanvas(fig).print_png(output)
#     return Response(output.getvalue(), mimetype='image/png')




if __name__ == '__main__':    
    app.run()

