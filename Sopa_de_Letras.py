# -*- coding: utf-8 -*-


import PySimpleGUI as sg
import os
import json
from datetime import datetime
import time
from modulos_sopa import configuracion_valida as cv
from modulos_sopa import juego_sopa as js
from modulos_sopa import Configurar_juego as cj
from modulos_sopa import reporte_juego as rj
ruta_app = os.getcwd()


if __name__ == '__main__':
	if not os.path.exists(os.path.join(ruta_app,'configuracion anterior')):
		os.mkdir(os.path.join(ruta_app,'configuracion anterior'))
	try:
		archconfig=open(os.path.join(ruta_app,'configuracion anterior','config.json'),'r+')
	except FileNotFoundError:
		archconfig=open(os.path.join(ruta_app,'configuracion anterior','config.json'),'w+')
	try:
		dic_config=json.load(archconfig)
		archconfig.seek(0)
	except json.decoder.JSONDecodeError:
		dic_config={}
	json.dump(dic_config,archconfig)	
	archconfig.close()
	valido,config_juego=cv.config_valida(dic_config)
	reporte_pantalla={'No encontrado':'','No coinciden':''}
	layout_menu=[
		[sg.Button('Configuración',size=(20,2))],
		[sg.Button('Jugar',size=(20,2),disabled=not valido,key='Jugar')],
		[sg.Button('Reporte',size=(20,2),disabled=True,key='Reporte')],
		[sg.Button('Salir',size=(20,2))],
		]
	ventana_menu=sg.Window('Menú',margins=(30,30)).Layout(layout_menu)
	while True:
		event_menu = ventana_menu.Read()
		if event_menu[0]==None:
			break
		else:
			ventana_menu.Hide()
			if event_menu[0]=='Salir':
				break
			elif event_menu[0]=='Configuración':
				config=cj.Configurar(reporte_pantalla,dic_config)
				if reporte_pantalla['No encontrado']!='' or reporte_pantalla['No coinciden']!='':
					ventana_menu.FindElement('Reporte').Update(disabled=False)
					if config==None:
						config={'tipografia titulo':'Times ','tipografia cuerpo':'Times '}
				if config!=None:
					valido,config_intermedia=cv.config_valida(config)
					if valido:
						config_juego=config_intermedia
						dic_config=config
						if not os.path.exists(os.path.join(ruta_app,'configuracion anterior')):
							os.mkdir(os.path.join(ruta_app,'configuracion anterior'))
						archconfig=open(os.path.join(ruta_app,'configuracion anterior','config.json'),'w+')
						json.dump(dic_config,archconfig)	
						archconfig.close()
						ventana_menu.FindElement('Jugar').Update(disabled=False)
					else:
						sg.Popup('La configuracion establecida no es valida.\nSe usará una anterior en caso de estar disponible')
			elif event_menu[0]=='Reporte':
				rj.reporte(reporte_pantalla,config['tipografia titulo'],config['tipografia cuerpo'])
			elif event_menu[0]=='Jugar':
				js.juego(config_juego)
			ventana_menu.UnHide()
	ventana_menu.Close()
