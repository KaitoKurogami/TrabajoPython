# -*- coding: utf-8 -*-

import os
import time
import json
from datetime import datetime
import Adafruit_DHT

class Temperatura:
	def __init__(self,pin=17,sensor=Adafruit_DHT.DHT11):
		self._sensor=sensor
		self._data:pin=pin
	
	def datos_sensor(self):
		humedad,temperatura=Adafruit.DHD.read_retry(self._sensor,self._data_pin)
		return{'temperatura':temperatura,'humedad':humedad}
		
if __name__="__main__":
	temp=Temperatura()
	oficina=input('ingrese oficina en la que se registrará la temperatura')
	if not os.path.exists(os.path.join(os.getcwd(),'oficinas')):
		os.mkdir(os.path.join(os.getcwd(),'oficinas'))
	try:
		arch=open(os.path.join(os.getcwd(),'oficinas','oficinas.json'),'r+')
	except FileNotFoundError:
		arch=open(os.path.join(os.getcwd(),'oficinas','oficinas.json'),'w+')
	try:
		oficinas=json.load(arch)
		arch.seek(0)
	except json.decoder.JSONDecodeError:
		oficinas={}
	if oficina not in oficinas.keys():
		oficinas[oficina]=[]
	for num in range(10)
		datos=temp.datos_sensor()
		oficinas[oficina].append({'temp':datos['temperatura'],'humedad':datos['humedad'],
		'fecha':datetime.fromtimestamp(time.time()).strftime('%a %d %b, %y')})
		time.sleep(60)
	json.dump(oficinas,arch)	
	arch.close()
