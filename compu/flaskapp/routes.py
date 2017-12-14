# coding=utf-8
from __future__ import print_function 
import sys 
import re
import time
from pymongo import MongoClient
import urllib2
import numpy

from flask_table import *# Table, Col#cuidado hay que instalar flask_table (pip install flask_table)
from flask import Flask, render_template,request

from beebotte import *

API_KEY='a93b1bad738918ea136ce730d0cc3e50'
SECRET_KEY='92170be95492026d25d73e06b55d8800aff7a85daa04def015ef9ff04eb5cf2b'
bclient = BBT(API_KEY, SECRET_KEY)


class ItemTable(Table): #definimos la clase para la tabla
    #num = Col('num')
    num=Col('num')
    num.__init__('num', None, None, True, True,None, {"width":100,"align":"center"},None)
    day = Col('day')
    day.__init__('day', None, None, True, True,None, {"width":100,"align":"center"},None)	
    month = Col('month')	
    month.__init__('month', None, None, True, True,None, {"width":100,"align":"center"},None)	
    year=Col('year')
    year.__init__('year', None, None, True, True,None, {"width":100,"align":"center"},None)
    

class Item(object):
    def __init__(self, num, day,month,year):
        self.num = num
        self.day = day
	self.month=month
	self.year=year


client=MongoClient()
db=client.numeros

app = Flask(__name__)      

ceil='0'
floor='0'

def media_mongo():
	E=0
	idx=0
	query=db.numeros.find()
	for read in query:
		idx=idx+1	
		E=E+read['num']
	print(E)
	if idx==0 :
		res= 0
 	else :
		res=E/idx
	return res

def media_beebotte():
	E=0
	idx=0
	query=bclient.read("C_E_R","num")
	for read in query:
		print(read)
		idx=idx+1	
		E=E+read["data"]
	if idx==0 :
		res= 0
 	else :
		res=E/idx
	return res

def last_read():
	E=0
	idx=0
	query=bclient.read("C_E_R","num",limit=1)
	print(query)
	for read in query:
		idx=idx+1
		E=E+read["data"]
	if idx==0 :
		res= 0
 	else :
		res=E
	return res

def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False


			
@app.route('/')
def home():
  print('web_main recargada') 
  media=media_mongo()	
  lst_read=last_read()
  return render_template('web_main.html',max_val=ceil,min_val=floor,selected_bbt="",selected_mongo="selected",avg=media,last_r=lst_read,db="Mongodb")




@app.route('/', methods=['POST'])
def top_value_post(): # hemos definido la funcion
 ceil=request.form['ceil']  
 floor=request.form['floor']
 selected_db=request.form['fuente']
 print("fuente:{}".format(selected_db))		
 
 tab_elem=[]		 
 aux=[]

 if isfloat(ceil) and isfloat(floor) : 
  
	num_ceil=float(ceil)
	num_floor=float(floor)
 	print ('valores de busqueda')
  	print ('maximo:{}'.format(num_ceil))
  	print ('minimo:{}'.format(num_floor))
  	print ('busca en la base de datos')
  	resultado=db.numeros.find({"$and": [{"num":{"$lt":num_ceil}},{"num":{"$gt":num_floor}}]})
  	print('busqueda en la base de datos finalizada')
	
	for items in resultado:
		#print (items)
		nums=items['num']
		days=items['day']
		months=items['month']
		years=items['year']
    		#print('el numero es {}'.format(items['num']))
		aux+=[Item(nums,days,months,years)]
		
  	#print(nums)

 tab_elem=aux
 tab = ItemTable(tab_elem)


	
 media=media_mongo()	 		 
 media_bbt=media_beebotte()
 l_read=last_read()	
 print('media beebotte{}'.format(media_bbt))
 if selected_db=="Mongodb":		
 	return render_template('web_main.html',max_val=ceil,min_val=floor,table=tab,avg=media,db='Mongodb',last_r=l_read,selected_bbt="",selected_mongo="selected")
 elif selected_db=="Beebotte":
	return render_template('web_main.html',max_val=ceil,min_val=floor,table=tab,avg=media_bbt,db='Beebotte',last_r=l_read,selected_bbt="selected",selected_mongo="")
	

if __name__ == '__main__':
  app.run(debug=True)#comentar
  #app.run(host='192.168.17.190', port=5000)	

