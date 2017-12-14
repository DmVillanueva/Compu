# -*- coding: utf-8 -*-


import re
import time
from pymongo import MongoClient
import urllib2
from beebotte import *

API_KEY='a93b1bad738918ea136ce730d0cc3e50'
SECRET_KEY='92170be95492026d25d73e06b55d8800aff7a85daa04def015ef9ff04eb5cf2b'
bclient = BBT(API_KEY, SECRET_KEY)

client=MongoClient()
db=client.numeros
while True:


	url='http://www.numeroalazar.com.ar/'
	p = re.compile('ab*')

	response = urllib2.urlopen(url)#cargamos la pagina
	webContent= response.read()#webcontent es la pagina web en formato cadena de caracteres
	#print(webContent[0:300])
	
	#buscamos patrones con la expresión regular
	text=re.findall('<div\sclass=\"container\"\s\sid=\"numeros_generados\">[\s]*<h2>Números\sgenerados</h2>[\s\t\r\n]*[0-9\.<br>]*',webContent,flags=0)
	string=text[0].split("<br>")
	string1=string[0];
	string2=string1.split("</h2>")
	#print(string2[1])#es el número, pero tiene tres espacios delante, tenemos que eliminarlos
	num_sucio=string2[1];

	#print(num_sucio)
	#print 'longitud leida: {}'.format(len(num_sucio))
	a=0
	num_limpio=[0,0,0,0,0,0]
	for i in range(len(num_sucio)):
		if num_sucio[i]=="0":
	#		print(0)
			num_limpio[a]=0
			a=a+1
		elif num_sucio[i]=="1":
			num_limpio[a]=1
			a=a+1
	#		print(1)
		elif num_sucio[i]=="2":
			num_limpio[a]=2
			a=a+1
	#		print(2)
		elif num_sucio[i]=="3":
			num_limpio[a]=3
			a=a+1
	#		print(3)
		elif num_sucio[i]=="4":
			num_limpio[a]=4
			a=a+1
	#		print(4)
		elif num_sucio[i]=="5":
			num_limpio[a]=5
			a=a+1
		elif num_sucio[i]=="6":
			num_limpio[a]=6
			a=a+1
	#		print(6)
		elif num_sucio[i]=="7":
			num_limpio[a]=7
			a=a+1
	#		print(7)
		elif num_sucio[i]=="8":
			num_limpio[a]=8
			a=a+1
	#		print(8)
		elif num_sucio[i]=="9":
			num_limpio[a]=9
			a=a+1
	#		print(9)
		elif num_sucio[i]==".":
			num_limpio[a]="."
			a=a+1
	#		print(".")
	#print (num_limpio)
	#ahora hay que recuperar el valor decimal a partir del valor leido, hay que tener en cuenta que podría ser 100.00 en lugar de 99.990
	#vamos a leer la cadena para buscar el punto

	posicion_punto=0
	for i in range(5): #6 posiciones (de 0 a 5)
		if num_limpio[i] ==".":
			posicion_punto=i
	#print 'posicion del punto {}'.format(posicion_punto)
	#sabemos que la cadena tiene longitud 6 y la posición del punto, podemos calcular el peso de cada posición
	num=0
	#recorriendo los valores a la izquierda del punto
	for i in range(posicion_punto): # recorremos los valores sin llegar al punto
		num=num+num_limpio[i]*10**(posicion_punto-i-1)
	#ahora los valores a la derecha del punto
	rango=5-posicion_punto
	
	for i in range(rango):
		num=num+num_limpio[posicion_punto+1+i]*10**(-i-1)



	#ahora debemos obtener la fecha y la hora 
	localtime = time.localtime(time.time())
	#print (localtime)
	print 'el numero en decimal es {} el {} del {} de {} a las {}:{}:{}s'.format(num, localtime.tm_mday,localtime.tm_mon,localtime.tm_year,localtime.tm_hour,localtime.tm_min,localtime.tm_sec)
	#print (string1)
	#print(number)
	
	res_db=db.numeros.insert({'num': num , 'day': localtime.tm_mday, 'month': localtime.tm_mon, 'year':localtime.tm_year, 'hour': localtime.tm_hour, 'min':localtime.tm_min, 'sec': localtime.tm_sec})

	bclient.writeBulk("C_E_R",[{"resource": "num", "data": num},{"resource": "day", "data": localtime.tm_mday},{ "resource":'month', "data": localtime.tm_mon},{"resource":'year', "data":localtime.tm_year},{"resource":'hour',"data": localtime.tm_hour}, {"resource":'min',"data":localtime.tm_min},{"resource":'sec',"data":localtime.tm_sec}])
	del (res_db)
	del(string)
	del(string1)
	del(string2)
	del(num_sucio)
	del(num_limpio)
	del(i)
	del(a)
	time.sleep(5)

