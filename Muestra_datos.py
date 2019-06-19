# -*- coding: utf-8 -*-

import time
from luma.led_matrix.device import max7219
from luna.core.interface.serial import spi, noop
from luna.core.render import canvas
from luna.core.virtual import viewport
from luna.core.legacy import text, show_masage
from luna.core.legacy.font import proportional, CP437_FONT,TINY_FONT,SINCLAIR_FONT,LCD_FONT
from Registro_ambiental import Temperatura
import RPi.GPIO as GPIO

class Sonido:
	def __init__(self,canal=22):
		self._canal=canal
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self._canal,GPIO.IN)
		GPIO.setwarnings(False)
		GPIO.add_event_detect(self._canal, GPIO.RISING)
	
	def evento_detectado(self, function):
		if GPIO.event_detected(self._canal):
			funcion()

class Matriz:
	def __init__(self,numero_matrices=1,orientacion=0,rotacion=0,ancho=8,alto=8):
		self.font=[CP437_FONT,TINY_FONT,SINCLAIR_FONT,LCD_FONT]
		self.serial=spi(port=0,device=0,gpio=noop())
		self.device=max7219(self.serial,width=ancho,height=alto,cascaded=numero_matrices,rotate=rotacion,block_orientation=orientacion)
		
	def mostrar_mensaje(self,msg,delay=0.1,font=1):
		show_message(self.device,msg,fill='white',font=proportional(self.font[font]),scroll_delay=delay)
	
def mostrar_temperatura()
	temp=Temperatura()
	matriz=Matriz(numero:matrices=2,ancho=16)
	datos=temp.datos_sensor()
	a_mostrar='Temperatura '+datos['temperatura']+'ºC'+' Humedad'+datos['humedad']+'%'
	matriz.mostrar_mensaje(a_mostrar,delay=0,05)
	
if __name__="__main__":
	sonido=Sonido()
	while True:
		time.sleep(0.5)
		sonido.evento_detectado(mostrar_temperatura)
	#Para resetear los puertos usados a modo input
	GPIO.cleanup()
