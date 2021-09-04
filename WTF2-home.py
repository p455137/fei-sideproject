from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask import Flask,render_template,request,redirect
import sqlite3
import pandas as pd
import os
from flask import url_for
from flask import  send_file
from flask import make_response
from io import BytesIO
from urllib.parse import quote
app = Flask(__name__)






@app.route('/user/<name>')
def home(name):
    return render_template('cla舊.html',name=name)

@app.route('/user/<name>/commit')
def index1(name):
    return render_template('cla3.html',name=name)

@app.route('/user/<name>/commit',methods=['POST','GET'])
def index2(name):
	if request.method =='POST':
		if request.values['send']=='送出':
                    try:       
                            
                            conn = sqlite3.connect('委託清單.sqlite')

                            
                            conn.execute('CREATE TABLE if not EXISTS test1 ("編號" TEXT, "業務" TEXT, "箱號" TEXT, "name" TEXT,\
                                         "委託出貨日" text,"件數" text,"內容物" text,"公斤" TEXT, "運送地區" TEXT, "提貨安排" TEXT, "出口報關" TEXT,\
                                         "單價" text,"首重" text,"派件費" text,"其他費用總和" text,"報價備註" text,"清關價" text)')
                            
                            conn.close()
                        
                            a1=str.upper(request.form["date"]+request.form["boxnu"])  
                            a2=name
                            a3=str.upper(request.form["boxnu"])
                            a4=request.form["user"]
                            a5=request.form["date"]
                            a6=request.form["no"]
                            a7=request.form["index"]  
                            a8=request.form["weight"]
                            a9=request.form["location"]
                            a10=request.form["take"]
                            a11=request.form["invoice"]
                            a12=request.form["price"]
                            a13=request.form["firstprice"]
                            a14=request.form["sendingprice"]
                            a15=request.form["otherprice"]
                            a16=request.form["noteprice"]
                            a17=request.form["saleprice"]
                            
                            with sqlite3.connect("委託清單.sqlite") as con:
                                cur = con.cursor()
                                cur.execute('''INSERT INTO test1 VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',(a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13,a14,a15,a16,a17))
                                con.commit()
                                msg = "Record successfully added"
                                
                                
                                with sqlite3.connect("委託清單.sqlite") as con:
                                 cur = con.cursor()
                                 cur=cur.execute('''select * from test1 where 編號="'''+a1+'''"''')
                                 con.commit()
                                 index= cur.fetchall()
        
                                
                                return render_template('finda.html',name=name, index=index)
                    except :
                            con.rollback()
                            msg="error in insert operation"
               
                    finally:
                        
                                     
                            return render_template('finda.html',name=name, index=index,msg=msg)
                            con.close()
@app.route('/user/<name>/contract')
def contract(name):
    return render_template('contract.html',name=name)

@app.route('/user/<name>/contract',methods=['POST','GET'])
def contract2(name):
	if request.method =='POST':
		if request.values['send']=='送出':
                    try:       
                       
                                msg = "待開發"
                                return render_template("cla舊.html")
                    except :
                            
                            msg="error in insert operation"
               
                    finally:
                            return render_template('cla2.html',name=name, msg = msg)
                            

@app.route('/user/<name>/upload')
def upload(name):
    return render_template('upload.html',name=name)



@app.route('/user/<name>/upload',methods=['POST','GET'])
def upload_file(name):
	if request.method =='POST':
		if request.values['submit']=='submit':
                    try:       
                           
                             f = request.files['file']
                             df = pd.read_excel(f)
                             b=df.drop([0,1,2,3,4,5])
                             
                             data=pd.DataFrame(b.values,columns=["編號","箱號( C / NO )","箱數","外包裝型式",\
                                                   "託運貨物準確品名","入箱數( PCS / 箱 )",\
                                                   "外箱尺寸(長*寬*高)","裝箱數量","物品單位","每PCS淨重( KG / PCS )","總淨重( N.W )","總毛重( G.W )",\
                                                   "飛特過磅","材積重量( V.W )","計價重量",\
                                                   "材質組成(物品)成分標示(食品)","生產日期","有效期限","品牌","製造商名稱",\
                                                   "產地","物品用途","貨物成本價值(NT$/PCS)","收件人","收件電話","收件地址","備註",])
                            
                             conn=sqlite3.connect("託運清單.sqlite")
                             cursor=conn.cursor()
                             data.to_sql("test1", conn,if_exists='append', index=False)
                             conn.commit()
                             conn.close()
                             msg = "Record successfully added"
                    except :
                            conn.rollback() 
                            msg="error in insert operation"
               
                    finally:
                            
                            return render_template('cla2.html',name=name, msg = msg)
                            conn.close()

@app.route('/user/<name>/findsomething')
def findsome(name):
    return render_template('findsomething.html',name=name)



@app.route('/user/<name>/logistic/<date>/<path>/<wood>')
def path(name,date,path,wood):
    return render_template('logistic.html',name=name,date=date,path=path,wood=wood)

@app.route('/user/<name>/logistic/<date>/<path>/<wood>',methods=['POST','GET'])
def path1(name,date,path,wood):
    if request.method =='POST':
    		if request.values['send']=='送出':
                    try:
                        a6=request.form["boxnu"]
                        conn1=sqlite3.connect("委託清單.sqlite")
                        cursor1=conn1.cursor()
                        us_df1 = pd.read_sql("SELECT * FROM test1" , conn1)
                        us_df1=us_df1.groupby("編號").get_group(a6)
                        
                        conn2=sqlite3.connect("託運清單.sqlite")
                        cursor2=conn2.cursor()
                        us_df2 = pd.read_sql("SELECT * FROM test1" , conn2)
                        us_df2=us_df2.groupby("編號").get_group(a6)
                    
                    
                        df_inner = us_df1.merge(us_df2, how='outer', on="編號")
                        df_inner.insert(0,column="後段",value="")
                        df_inner.insert(0,column="板號",value=wood)
                        df_inner.insert(0,column="航線",value=path)
                        df_inner.insert(0,column="出貨日",value=date)
                        cursor1.execute('''DELETE from test1 WHERE 編號="'''+a6+'''"''')
                        cursor2.execute('''DELETE from test1 WHERE 編號="'''+a6+'''"''')
                        conn1.commit()
                        conn1.close()
                        conn2.commit()
                        conn2.close()
                        
                        
                        conn=sqlite3.connect(date+"出貨清單.sqlite")
                        cursor=conn.cursor()
                        df_inner.to_sql("test1", conn,if_exists='append', index=False)
                     
                        
                        conn.commit()
                      
                        
                        msg = "Record successfully added"
                        return render_template('logistic.html',name=name,date=date,path=path,wood=wood,msg=msg)
                    except:
                         conn.rollback() 
                         msg="error in insert operation"
                    finally:
                                               
                            return render_template('logistic.html',name=name ,path=path,date=date,wood=wood,msg=msg)
                            conn.close()  


@app.route('/user/<name>/rearch')
def re(name):
    return render_template('cla3.html',name=name)

@app.route('/user/<name>/rearch',methods=['POST','GET'])
def re2(name):
	if request.method =='POST':
		if request.values['send2']=='查詢':
                  return render_template('update.html',name=name)
                            
  
    
@app.route('/user/<name>/update')
def up(name):
    return render_template('cla3.html',name=name)

@app.route('/user/<name>/update',methods=['POST','GET'])
def up2(name):
	if request.method =='POST':
		if request.values['send2']=="查詢":
                    try:
                        b=str.upper(request.form["indax"])
                        a=str.upper(request.form["take"])
                            
                        with sqlite3.connect("委託清單.sqlite") as con:
                                cur = con.cursor()
                                cur=cur.execute('''select * from test1 where '''+a+''' like"%'''+b+'''%"''')
                                con.commit()
                                index= cur.fetchall()

                        
                        return render_template('update.html',name=name, index=index,b=b)
                      
                    except :
                            con.rollback()
                            msg="error in insert operation"
               
                    finally:
                            
                            return render_template('update.html',name=name, index=index,b=b)
                            con.close()
@app.route('/user/<name>/updatenext')
def upne(name):
    return render_template('update.html',name=name)

@app.route('/user/<name>/updatenext',methods=['POST','GET'])
def upne2(name):
	if request.method =='POST':
		if request.values['send4']=='送出':
                    try:
                        a=request.form["take"]
                        c=request.form["indax"]
                        b=str.upper(request.form["number"])
                       
                        with sqlite3.connect("委託清單.sqlite") as con:
                         cur = con.cursor()
                         cur=cur.execute('''UPDATE test1 set "'''+a+'''" =" '''+c+'''" WHERE 編號 = "'''+b+'''"''')
                         con.commit()
                         cursor=con.cursor()
                         us_df=pd.read_sql("SELECT * FROM test1" , con)
                         cur=cursor.execute("SELECT * FROM test1")
                         index= cur.fetchall()   
                        
                       
                      
                         msg="委託清單"
                         con.commit()
                        
                        return render_template('finda.html',name=name, msg = msg, index=index)

                        
                        return render_template('finda.html',name=name,b=b)
                      
                    except :
                            con.rollback()
                            msg="error in insert operation"
               
                    finally:
                               
                            return render_template('finda.html',name=name, msg = msg, index=index)
                            con.close()   
@app.route('/user/<name>/delete')
def delete(name):
    return render_template('cla3.html',name=name)


@app.route('/user/<name>/delete',methods=['POST','GET'])
def delete2(name):
	if request.method =='POST':
		if request.values['send3']=='刪除':
                    try:
                        b=str.upper(request.form["number"])
                        with sqlite3.connect("委託清單.sqlite") as con:
                         cur = con.cursor()
                         e=cur.execute('''DELETE from test1 where 編號="'''+b+'''"''')
                         con.commit()
                        
                         msg = "delete successfully "
                         return render_template("cla舊.html")
                      
                    except :
                            con.rollback()
                            msg="error in insert operation"
               
                    finally:
                     
                            
                            return render_template('cla2.html',name=name, msg = msg)
                            con.close() 
@app.route('/user/<name>/deletes')
def deletes(name):
    return render_template('cla3.html',name=name)


@app.route('/user/<name>/deletes',methods=['POST','GET'])
def deletes2(name):
	if request.method =='POST':
		if request.values['send3']=='刪除':
                    try:
                        b=str.upper(request.form["number"])
                        with sqlite3.connect("託運清單.sqlite") as con:
                         cur = con.cursor()
                         e=cur.execute('''DELETE from test1 where 編號="'''+b+'''"''')
                         con.commit()
                        
                         msg = "delete successfully "
                         return render_template("cla舊.html")
                      
                    except :
                            con.rollback()
                            msg="error in insert operation"
               
                    finally:
                         
                            
                            return render_template('cla2.html',name=name, msg = msg)
                            con.close() 

        
        
@app.route('/user/<name>/print')
def pri(name):
    return render_template('cla3.html',name=name)


@app.route('/user/<name>/print',methods=['POST','GET'])
def pri2(name):
	if request.method =='POST':
		if request.values['send4']=='print':
                    try:
                        with sqlite3.connect("委託清單.sqlite") as con:
                            cursor=con.cursor()
                            us_df=pd.read_sql("SELECT * FROM test1" , con)
                            cur=cursor.execute("SELECT * FROM test1")
                            index= cur.fetchall()
                            
                           
                          
                            msg="委託清單"
                            con.commit()
                            
                            return render_template('finda.html',name=name, msg = msg, index=index)
                            
                      
                    except :
                            con.rollback()
                            msg="error in insert operation"
               
                    finally:
                            
                            return render_template('finda.html',name=name, msg = msg,index=index)
                            con.close() 

@app.route('/user/<name>/finda')
def finda(name):
   with sqlite3.connect("委託清單.sqlite") as con:
        try:
            cursor=con.cursor()
            us_df=pd.read_sql("SELECT * FROM test1" , con)
            cur=cursor.execute("SELECT * FROM test1")
            index= cur.fetchall()   
            
           
          
            msg="委託清單"
            con.commit()
            
            return render_template('finda.html',name=name, msg = msg, index=index)
            
  
        except :
                con.rollback()
                msg="error in insert operation"
           
        finally:
               
                return render_template('finda.html',name=name, msg = msg,index=index)
                con.close()  
@app.route('/user/<name>/findb')
def findb(name):
   with sqlite3.connect("託運清單.sqlite") as con:
        try:
            cursor=con.cursor()
            us_df=pd.read_sql("SELECT * FROM test1" , con)
            cur=cursor.execute("SELECT * FROM test1")
            index= cur.fetchall()   
            
           
          
            msg="託運清單"
            con.commit()
            
            return render_template('findb.html',name=name, msg = msg, index=index)
            
  
        except :
                con.rollback()
                msg="error in insert operation"
           
        finally:                
                return render_template('findb.html',name=name, msg = msg,index=index)
                con.close()  

@app.route('/user/<name>/findcc')
def findcc(name):
    return render_template('findcc.html',name=name)
@app.route('/user/<name>/findcc',methods=['POST','GET'])
def findc(name):
   
    if request.method =='POST':
    		if request.values['send']=='送出':
                     try:
                            b=str.upper(request.form["indax"])
                         
                            
                            with sqlite3.connect("委託清單.sqlite") as con:
                                    cur = con.cursor()
                                    cur=cur.execute('''select * from test1 where 編號 like"%'''+b+'''%"''')
                                    con.commit()
                                    index= cur.fetchall()
                                 
                            with sqlite3.connect("託運清單.sqlite") as conn:
                               
                                    cur1 = conn.cursor()
                                    cur1=cur1.execute('''select * from test1 where 編號 like"%'''+b+'''%"''')
                                    conn.commit()
                                    index2= cur1.fetchall()
                                
                            
                            
                            msg = "successfully "
                            return render_template('findc.html',name=name, index=index, index2=index2, msg=msg)
                     except :
                            con.rollback()
                            msg="check list"             
                     finally:
                           
                            return render_template('findc.html',name=name, index=index, index2=index2, msg=msg)
                            con.close() 
                            conn.close() 
                    


if __name__ == '__main__':
 
    app.run() 