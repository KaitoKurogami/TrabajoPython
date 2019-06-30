import PySimpleGUI as sg
import os
from datetime import datetime
import time
ruta_app = os.getcwd()
from buscar_palabras import palabras_datos as pd


def Ingresar_palabras(datos,reporte_pantalla):
	'''
	Recibe un diccionario con palabras (y sus datos) al cual agregará o quitará elementos
	y un diccionario con los dos tipos de reporte que podrá verse modificado si se 
	agregan palabras y ocurren ciertos casos
	'''
	formato = '%d-%m-%y'
	hoy=datetime.fromtimestamp(time.time()).strftime(formato)
	if not os.path.exists(os.path.join(ruta_app,'log')):
			os.mkdir(os.path.join(ruta_app,'log'))
	lista_eliminar=['-Eliminar-']
	lista_eliminar.extend(list(datos.keys()))
	lista_eliminar.sort()
	lista_esta_vacia=len(lista_eliminar)==1
	layout_ingreso=[
		[sg.Button('Agregar',size=(10,1)),sg.InputText(default_text='',size=(17,1),key='elem_agregar')],
		[sg.Button('Eliminar',key='Eliminar',disabled=lista_esta_vacia,size=(10,1)),sg.InputCombo(lista_eliminar,size=(20,1),key='lista_eliminar')],
		[sg.Button('Terminar',size=(30,1))],
		]
	ventana_ingreso=sg.Window('Ingreso de palabras',margins=(10,30)).Layout(layout_ingreso)
	fin=False
	while not fin:
		event_ingre,values_ingre=ventana_ingreso.Read()
		if event_ingre=='Agregar':
			ventana_ingreso.Hide()
			palabra=values_ingre['elem_agregar'].lower()
			llamar_funcion=True
			if palabra in lista_eliminar:
				llamar_funcion=sg.PopupYesNo('La palabra ya fue ingresada anteriormente\n¿Desea eliminarla y agregarla nuevamente?')=='yes'
			if llamar_funcion:
				datos_palabra=pd.obtener_datos(palabra,reporte_pantalla,hoy)
				if datos_palabra!=None:
					datos[palabra]=datos_palabra
					lista_eliminar.append(palabra)
					lista_eliminar.sort()
					ventana_ingreso.FindElement('lista_eliminar').Update(values=lista_eliminar)
					ventana_ingreso.FindElement('Eliminar').Update(disabled=False)
			ventana_ingreso.UnHide()
		elif event_ingre=='Eliminar':
			if values_ingre['lista_eliminar']!='-Eliminar-':
				if sg.PopupYesNo('Seguro que desea eliminar la palabra:'+values_ingre['lista_eliminar']+'?')=='Yes':
					lista_eliminar.remove(values_ingre['lista_eliminar'])
					del datos[values_ingre['lista_eliminar']]
					ventana_ingreso.FindElement('lista_eliminar').Update(values=lista_eliminar)
					ventana_ingreso.FindElement('Eliminar').Update(disabled=len(lista_eliminar)==1)
		elif event_ingre=='Terminar' or event_ingre==None:
			fin=True
	ventana_ingreso.Close()
