import PySimpleGUI as sg
import os
import json
ruta_app = os.getcwd()
from modulos_configurar import modulo_colores as mc
from modulos_configurar import modulo_palabras as mp
			
def Configurar(reporte_pantalla,dic_config):
	'''
	recibe un diccionario como estructura base para los reportes en pantalla
	y un diccionario con configuracion previa
	devuelve un diccionario con los datos de las palabras
	los colores a usar para cada tipo de palabra
	si se mostrará ayuda en pantalla
	la orientacion de las palabras
	si las letras serán mayusculas o minusculas
	la tipografia de los titulos y cuerpos del reporte a mostrar en pantalla
	y si el color del juego dependerá de las oficinas o será el neutro
	'''
	if dic_config=={} or dic_config==None:
		config_estandar={"ayuda": "sin", "orientacion": "horizontal", "cant_sustantivos": "3",
		 "cant_adjetivos": "3", "cant_verbos": "3", "MayusOMinus": "mayusculas",
		  "tipografia titulo": "Times ", "tipografia cuerpo": "Times ", "elegir estilo": "Sin",
		   "oficina": "Elegir","colores": {"Sustantivos": "red", "Adjetivos": "green", "Verbos": "yellow"}}
	else:
		config_estandar=dic_config
	if not os.path.exists(os.path.join(ruta_app,'palabras anteriores')):
		os.mkdir(os.path.join(ruta_app,'palabras anteriores'))
	try:
		archpalabras=open(os.path.join(ruta_app,'palabras anteriores','palabras.json'),'r+')
	except FileNotFoundError:
		archpalabras=open(os.path.join(ruta_app,'palabras anteriores','palabras.json'),'w+')
	try:
		dic_palabras=json.load(archpalabras)
	except json.decoder.JSONDecodeError:
		dic_palabras={}
	archpalabras.close()
	if not os.path.exists(os.path.join(ruta_app,'oficinas')):
		dic_oficinas={}
	else:
		try:
			archofice=open(os.path.join(ruta_app,'oficinas','oficinas.json'),'r+')
			dic_oficinas=json.load(archofice)
			archofice.close()
		except FileNotFoundError:
			dic_oficinas={}
	lista_oficinas=['Elegir']
	lista_oficinas.extend(list(dic_oficinas.keys()))
	fontsize='12'
	tipografia=config_estandar["tipografia titulo"]
	tipografia2=config_estandar["tipografia cuerpo"]
	colores={'Sustantivos':config_estandar['colores']["Sustantivos"],'Adjetivos':config_estandar['colores']["Adjetivos"]
	,'Verbos':config_estandar['colores']["Verbos"]}
	columna=[
		[sg.Text('Sustantivos',size=(11,1)),sg.InputText(default_text=config_estandar["cant_sustantivos"],key='cant_sustantivos',size=(4,1))],
		[sg.Text('Adjetivos',size=(11,1)),sg.InputText(default_text=config_estandar["cant_adjetivos"],key='cant_adjetivos',size=(4,1))],
		[sg.Text('Verbos',size=(11,1)),sg.InputText(default_text=config_estandar["cant_verbos"],key='cant_verbos',size=(4,1))],
		]
	layout_config=[
		[sg.Button('Ingresar Palabras',key='B1',size=(50,2))],
		[sg.Button('Elegir Colores',key='B2',size=(50,2))],
		[sg.Text('Ayuda ',size=(35,1)),sg.InputCombo(['sin','palabra','definicion','ambas'],
		default_value=config_estandar['ayuda'],key='ayuda',size=(10,1))],
		[sg.Text('Orientacion ',size=(35,1)),sg.InputCombo(['vertical','horizontal'],
		default_value=config_estandar['orientacion'],key='orientacion',size=(10,1))],
		[sg.Text('Cantidad de palabras',size=(28,1)),sg.Column(columna)],
		[sg.Text('Mayusculas/minusculas',size=(35,1)),sg.InputCombo(['mayusculas','minusculas'],
		default_value=config_estandar['MayusOMinus'],key='MayusOMinus',size=(10,1))],
		[sg.Text('Tipografia titulo',size=(11,2)),sg.InputCombo(['Courier ','Helvetica ','Times '],
		change_submits=True,key='tipografia titulo',size=(10,1),default_value=config_estandar['tipografia titulo']),
		sg.Text('Texto de Ejemplo',font=tipografia+fontsize,size=(20,1),key='ejemplo')],
		[sg.Text('Tipografia texto',size=(11,2)),sg.InputCombo(['Courier ','Helvetica ','Times '],
		change_submits=True,key='tipografia cuerpo',size=(10,1),default_value=config_estandar['tipografia cuerpo']),
		sg.Text('Texto de Ejemplo',font=tipografia2+fontsize,size=(20,1),key='ejemplo2')],
		[sg.Text('Estilo',size=(11,1)),sg.InputCombo(['normal','oficinas']
		,disabled=len(lista_oficinas)==1,change_submits=True,key='elegir estilo',size=(10,1)),
		sg.InputCombo(lista_oficinas,disabled=True,key='oficina',size=(10,1))],
		[sg.Button('Guardar y salir',key='Guardar',size=(24,2)),sg.Button('Salir',key='Salir',size=(24,2))],
		]
	ventana_config=sg.Window('Configuración',margins=(10,30)).Layout(layout_config)
	fin=False
	while True:
		configurado=False
		event_config,values_config=ventana_config.Read()
		if event_config==None:
			return None
		if event_config=='Salir':
			if sg.PopupYesNo('¿Salir sin guardar?')=='Yes':
				break
		if tipografia!=values_config['tipografia titulo']:
			tipografia=values_config['tipografia titulo']
			ventana_config.FindElement('ejemplo').Update(font=tipografia+fontsize)
		if tipografia2!=values_config['tipografia cuerpo']:
			tipografia2=values_config['tipografia cuerpo']
			ventana_config.FindElement('ejemplo2').Update(font=tipografia2+fontsize)
		if event_config=='Guardar':
			if(not values_config['cant_adjetivos'].isdigit() or not values_config['cant_sustantivos'].isdigit()
			or not values_config['cant_verbos'].isdigit()):
				sg.Popup('Revise que las cantidades ingresadas para cada tipo de palabra\nSean numeros adecuados\n(Tenga cuidado con espacios que no se vean)')
			else:
				configurado=True
				break
		if 'oficinas'==values_config['elegir estilo']:
			ventana_config.FindElement('oficina').Update(disabled=False)
		if 'normal'==values_config['elegir estilo']:
			ventana_config.FindElement('oficina').Update(disabled=True)
		if event_config=='B1':
			ventana_config.Hide()
			mp.Ingresar_palabras(dic_palabras,reporte_pantalla)
		elif event_config=='B2':
			ventana_config.Hide()
			mc.elegir_colores(colores)
		ventana_config.UnHide()
	if configurado:
		configuracion=values_config
		configuracion['palabras']=dic_palabras
		configuracion['colores']=colores
		if not os.path.exists(os.path.join(ruta_app,'palabras anteriores')):
			os.mkdir(os.path.join(ruta_app,'palabras anteriores'))
		archpalabras=open(os.path.join(ruta_app,'palabras anteriores','palabras.json'),'w+')
		json.dump(dic_palabras,archpalabras)	
		archpalabras.close()
		ventana_config.Close()
		return configuracion
	ventana_config.Close()
	return None
