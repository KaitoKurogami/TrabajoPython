# -*- coding: utf-8 -*-

from pattern.web import Wiktionary
from pattern.es import parse
import PySimpleGUI as sg
import os
import sys
import json
import string
from datetime import datetime
import time
import random
ruta_app = os.getcwd()
frio='#58C9FE'
fin_color_frio=20
templado='#1EC733'
inicio_calido=30
calor='#FF2525'
tam_min=8
palabras_max=20

def InfoPalabraWiktionary(palabra):
	'''
	Recibe una palabra, la busca en wiktionary y retorna si es sustantivo,
	adjetivo o verbo, y una definición
	Si no encuentra nada, returna None,None
	'''
	
	fin=False
	esp=False
	article = Wiktionary(language="es").search(palabra) 
	if article==None:
		return None,None
	else:
		for section in article.sections:
			if section.title=='Español':
				esp=True
				for subsection in section.children:
					if not fin:
						desc=repr(subsection.string)
					if not fin and ('Adjetivo' in subsection.title or 'adjetiva' in subsection.title):
						tipo='adjetivo'
						fin=True
					elif not fin and ('Sustantivo' in subsection.title or 'sustantiva' in subsection.title):
						tipo='sustantivo'
						fin=True
					elif not fin and ('Verbo' in subsection.title or'Forma verbal' in subsection.title):
						tipo='verbo'
						fin=True
					elif not fin and 'Etimología' in subsection.title:
						for sub in subsection.children:
							if not fin:
								desc=repr(sub.string)
							if not fin and ('Adjetivo' in sub.title or 'adjetiva' in sub.title):
								tipo='adjetivo'
								fin=True
							elif not fin and ('Sustantivo' in sub.title or 'sustantiva' in sub.title):
								tipo='sustantivo'
								fin=True
							elif not fin and ('Verbo' in sub.title or'Forma verbal' in sub.title):
								tipo='verbo'
								fin=True
		if esp:					
			desc = desc.split('\\n')
			desc=list(filter(lambda x:x.startswith('1'),desc))
			desc=desc[0].replace('1','')+'\n'
			if desc[0]!=' ':
				desc=' '+desc
			return (tipo,desc)
		else:
			return None,None
			
def obtener_datos(palabra,reporte_pantalla,hoy):
	'''
	recibe una palabra, un diccionario con los dos tipos de reportes a hacer en pantalla los cuales actualizará
	y la fecha de hoy vista como dia mes año para poder nombrar el log de reporte según el dia
	si se agrega el elemento a la lista de palabras retorna un diccionario con el tipo y la descripcion
	sino retorna None
	'''
	tipo,desc=InfoPalabraWiktionary(palabra)
	s=parse(palabra).split()
	if 'NN' in s[0][0][1]:
		tipoPattern='sustantivo'
	elif 'JJ' in s[0][0][1]:
		tipoPattern='adjetivo'
	elif 'VB' in s[0][0][1]:
		tipoPattern='verbo'
	elif s[0][0][1]=='IN':
		tipoPattern='conjuncion'
	elif 'RB' in s[0][0][1] or 'RP'==s[0][0][1]:
		tipoPattern='adverbio'
	elif 'CD'==s[0][0][1]:
		tipoPattern='cardinal'
	else:
		tipoPattern='desconocido'
	valido=True
	modif=True
	opciones=['-Elegir-','sustantivo','adjetivo','verbo']
	if tipo==None:
		if not os.path.exists(os.path.join(ruta_app,'log')):
			os.mkdir(os.path.join(ruta_app,'log'))
		reporte=open(os.path.join(ruta_app,'log','reporte'+hoy+'.txt'),'a+')
		reporte_texto=palabra+': No ha sido encontrada en Wiktionary, pero pattern la considera un '+tipoPattern+'\n'
		reporte.write(reporte_texto)
		reporte.close()
		reporte_pantalla['No encontrado']=reporte_pantalla['No encontrado']+reporte_texto
		tipo='-Elegir-'
		desc=''
		valido=sg.PopupYesNo('Elemento no encontrado en Wiktionary\n¿Desea agregarlo manualmente?')=='Yes'
		modif=False
	elif tipo!=tipoPattern:
		if not os.path.exists(os.path.join(ruta_app,'log')):
			os.mkdir(os.path.join(ruta_app,'log'))
		reporte=open(os.path.join(ruta_app,'log','reporte'+hoy+'.txt'),'a+')
		reporte_texto=palabra+': En Wiktionary se considera: '+tipo+', pero pattern se considera un '+tipoPattern+'\n'
		reporte.write(reporte_texto)
		reporte.close()
		reporte_pantalla['No coinciden']=reporte_pantalla['No coinciden']+reporte_texto
	desc_og=desc
	if valido:
		layout_datos=[
			[sg.Text('Tipo',size=(5,1)),sg.InputCombo(opciones,default_value=tipo,key='tipo',size=(10,1))],
			[sg.Text('Descripcion')],
			[sg.Multiline(desc,size=(51,5),key='descripcion',disabled=True)],
			[sg.Button('Descripcion original',disabled=True,key='Original',size=(22,2)),sg.Button('Editar descripcion',key='Modificar',size=(22,2))],
			[sg.Button('Aceptar',key='Aceptar',disabled=not modif,size=(22,2)),sg.Button('Salir sin guardar',key='Salir',size=(22,2))],
			]
		ventana_datos=sg.Window('Datos de la palabra',margins=(10,30)).Layout(layout_datos)
		while True:
			event_datos,values_datos=ventana_datos.Read()
			if event_datos=='Modificar':
				ventana_datos.FindElement('descripcion').Update(disabled=False)
				ventana_datos.FindElement('Original').Update(disabled=False)
				ventana_datos.FindElement('Aceptar').Update(disabled=False)
			elif event_datos=='Original':
				ventana_datos.FindElement('descripcion').Update(desc_og)
			elif event_datos=='Aceptar':
				if values_datos['tipo']=='-Elegir-':
					sg.Popup('Eliga un tipo para la palabra')
				elif sg.PopupYesNo('Estos datos son correctos?')=='Yes':
					agregar=True
					break
			elif event_datos=='Salir' or event_datos==None:
				if sg.PopupYesNo('Desea salir sin guardar?')=='Yes':
					agregar=False
					break
		ventana_datos.Close()
		if agregar:
			return values_datos
	return None
		

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
				datos_palabra=obtener_datos(palabra,reporte_pantalla,hoy)
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
			
def elegir_colores(colores):
	'''
	recibe un diccionario con el color correspondiente a cada tipo de palabra y los modifica
	'''
	dic_colores={'Rojo':'red','Naranja rojizo':'#FF4500','Verde':'green','Naranja':'orange','Celeste':'#3D82F9',
	'Verde lima':'#32CD32',	'Verde Oscuro':'darkgreen','Verde marino':'#2E8B57','Amarillo':'yellow','Rosa':'pink',
	'Rosa fuerte':'#FF69B4','Salmón':'salmon','Violeta':'#EE82EE','oliva':'#808000','Aguamarina':'#7FFFD4',
	'Turquesa':'#40E0D0','Chocolate':'#D2691E','coral':'#FF7F50'}
	lista_colores=list(dic_colores.keys())
	BCS='red'
	BCA='green'
	BCV='yellow'
	columna1=[
		[sg.Text('Sustantivos')],
		[sg.InputCombo(lista_colores,change_submits=True,default_value='Rojo',size=(13,1),key='color_sust')],
		[sg.Button('',size=(13,2),disabled=True,button_color=('black',BCS),key='BS')],
		]
	columna2=[
		[sg.Text('Adjetivos')],
		[sg.InputCombo(lista_colores,change_submits=True,default_value='Verde',size=(13,1),key='color_adj')],
		[sg.Button('',size=(13,2),disabled=True,button_color=('black',BCA),key='BA')],
		]
	columna3=[
		[sg.Text('Verbos')],
		[sg.InputCombo(lista_colores,change_submits=True,default_value='Amarillo',size=(13,1),key='color_verbo')],
		[sg.Button('',size=(13,2),disabled=True,button_color=('black',BCV),key='BV')],
		]
	layout_colores=[
		[sg.Column(columna1),sg.Column(columna2),sg.Column(columna3)],
		[sg.Button('Terminar',size=(12,2),key='Terminar')],
		]
	ventana_colores=sg.Window('Elegir colores',margins=(10,30)).Layout(layout_colores)
	while True:
		event_col,values_col=ventana_colores.Read()
		if event_col is None:
			break
		CS=dic_colores[values_col['color_sust']]
		CA=dic_colores[values_col['color_adj']]
		CV=dic_colores[values_col['color_verbo']]
		if CS!=BCS:
			BCS=CS
			ventana_colores.FindElement('BS').Update(button_color=('black',BCS))
		if CA!=BCA:
			BCA=CA
			ventana_colores.FindElement('BA').Update(button_color=('black',BCA))
		if CV!=BCV:
			BCV=CV
			ventana_colores.FindElement('BV').Update(button_color=('black',BCV))
		if event_col=='Terminar':
			if(BCS!=BCA and BCS!=BCV and BCA!=BCV):
				colores['Sustantivos']=BCS
				colores['Adjetivos']=BCA
				colores['Verbos']=BCV
				break
			else:
				sg.Popup('Elija 3 colores diferentes')
	ventana_colores.Close()
			
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
	tipografia='Courier '
	tipografia2='Courier '
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
		sg.Text('Texto de Ejemplo',font=tipografia+fontsize,size=(20,1),key='ejemplo2')],
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
			configurado=True
			break
		if 'oficinas'==values_config['elegir estilo']:
			ventana_config.FindElement('oficina').Update(disabled=False)
		if 'normal'==values_config['elegir estilo']:
			ventana_config.FindElement('oficina').Update(disabled=True)
		if event_config=='B1':
			ventana_config.Hide()
			Ingresar_palabras(dic_palabras,reporte_pantalla)
		elif event_config=='B2':
			ventana_config.Hide()
			elegir_colores(colores)
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
	
def config_valida(dic_config):
	'''
	Devuelve como primer elemento un boolean de si la configuracion es correcta
	y devuelve un diccionario con los datos necesarios para jugar en caso de serlo
	o un diccionario vacio en caso contrario
	'''
	if dic_config=={} or dic_config==None:
		return False,{}
	else:
		if dic_config['palabras']=={}:
			return False,{}
		palabras_por_tipo={'sustantivos':{},'adjetivos':{},'verbos':{}}
		#Generar diccionario segun el tipo
		for palabra in dic_config['palabras'].keys():
			tipo_a_usar=dic_config['palabras'][palabra]['tipo']+'s'
			palabras_por_tipo[tipo_a_usar][palabra]=dic_config['palabras'][palabra]['descripcion']
		palabras_final={'sustantivos':{},'adjetivos':{},'verbos':{}}
		#Diccionario final eligiendo las palabras a usar en el juego
		cont_sust=0
		cont_adj=0
		cont_verb=0
		max_long=0
		total=0
		for num in range(0,int(dic_config['cant_sustantivos'])):
			try:
				if(total<palabras_max):
					Pelegida=random.choice(list(palabras_por_tipo['sustantivos'].keys()))
					Delegida=palabras_por_tipo['sustantivos'].pop(Pelegida)
					if dic_config['MayusOMinus']=='mayusculas':
						Pelegida=Pelegida.upper()
					palabras_final['sustantivos'][Pelegida]=Delegida
					if len(Pelegida)>max_long:
						max_long=len(Pelegida)
					cont_sust=cont_sust+1
					total=total+1
			except IndexError:
				break
		for num in range(0,int(dic_config['cant_adjetivos'])):
			try:
				if(total<palabras_max):
					Pelegida=random.choice(list(palabras_por_tipo['adjetivos'].keys()))
					Delegida=palabras_por_tipo['adjetivos'].pop(Pelegida)
					if dic_config['MayusOMinus']=='mayusculas':
						Pelegida=Pelegida.upper()
					palabras_final['adjetivos'][Pelegida]=Delegida
					if len(Pelegida)>max_long:
						max_long=len(Pelegida)
					cont_adj=cont_adj+1
					total=total+1
			except IndexError:
				break
		for num in range(0,int(dic_config['cant_verbos'])):
			try:
				if(total<palabras_max):
					Pelegida=random.choice(list(palabras_por_tipo['verbos'].keys()))
					Delegida=palabras_por_tipo['verbos'].pop(Pelegida)
					if dic_config['MayusOMinus']=='mayusculas':
						Pelegida=Pelegida.upper()
					palabras_final['verbos'][Pelegida]=Delegida
					if len(Pelegida)>max_long:
						max_long=len(Pelegida)
					cont_verb=cont_verb+1
					total=total+1
			except IndexError:
				break
		#reviso si hay al menos una palabra
		if total==0:
			return False,{}
		else:
			sustantivos={'cantidad':cont_sust,'color':dic_config['colores']['Sustantivos'],
			'palabras':palabras_final['sustantivos']}
			adjetivos={'cantidad':cont_adj,'color':dic_config['colores']['Adjetivos'],
			'palabras':palabras_final['adjetivos']}
			verbos={'cantidad':cont_verb,'color':dic_config['colores']['Verbos'],
			'palabras':palabras_final['verbos']}
		if dic_config['elegir estilo']=='normal':
			estilo=None
		else:
			if not os.path.exists(os.path.join(ruta_app,'oficinas')):
				dic_oficinas={}
			else:
				try:
					archofice=open(os.path.join(ruta_app,'oficinas','oficinas.json'),'r+')
					dic_oficinas=json.load(archofice)
					archofice.close()
				except FileNotFoundError:
					dic_oficinas={}
			
			if dic_oficinas=={}:
				estilo=None
			else:
				if dic_config['oficina'] in dic_oficinas.keys():
					temp_total=0
					cant_temp=0
					for elem in dic_oficinas[dic_config['oficina']]:
						temp_total=temp_total+elem['temp']
						cant_temp=cant_temp+1
					prom=temp_total/cant_temp
					if prom<=fin_color_frio:
						estilo=frio
					elif prom<=inicio_calido:
						estilo=templado
					else:
						estilo=calor
				else:
					estilo=None
		return True,{'sustantivos':sustantivos,'adjetivos':adjetivos,'verbos':verbos,'ayuda':dic_config['ayuda'],
		'longitud_maxima':max_long,'cantidad_palabras':total,'orientacion':dic_config['orientacion'],
		'letras':dic_config['MayusOMinus'],'estilo':estilo}
		
def reporte(reporte_pantalla,tipo_titulo,tipo_cuerpo):
	'''
	Recibe un diccionario con los reportes
	y las tipografias de los titulos y cuerpos
	muestra en pantalla los reportes con las
	tipografias correspondientes
	'''
	tamaño=300
	repo1=reporte_pantalla['No encontrado']==''
	repo2=reporte_pantalla['No coinciden']==''
	if not repo1 and not repo2:
		tamaño=460
	fonts={'Courier ':'courier 10','Helvetica ':'Helvetica 10','Times ':'Times 11'}
	fontsT={'Courier ':'courier 11','Helvetica ':'Helvetica 11','Times ':'Times 12'}
	layout_reporte=[
			[sg.Text('Palabras que no se han encontrado en Wiktionary',font=fontsT[tipo_titulo],size=(56,1),visible=not repo1)],
			[sg.Multiline(reporte_pantalla['No encontrado'],font=fonts[tipo_cuerpo],size=(76,8),disabled=True,visible=not repo1)],
			[sg.Text('Palabras encontradas en Wiktionary\nPero cuyo tipo no coincide con el de Pattern',font=fontsT[tipo_titulo],size=(56,2),visible=not repo2)],
			[sg.Multiline(reporte_pantalla['No coinciden'],font=fonts[tipo_cuerpo],size=(76,8),disabled=True,visible=not repo2)],
			[sg.Button('Terminar',key='Terminar',size=(20,2))],
			]
	ventana_reporte=sg.Window('Menú',size=(680,tamaño),margins=(30,30)).Layout(layout_reporte)
	while True:
		event_repo,values_repo = ventana_reporte.Read()
		if event_repo==None or event_repo=='Terminar':
			break
	ventana_reporte.Close()
	
def juego(config_juego):
	'''
	El juego en si, recibe un diccionario con las cosas necesarias
	'''
	texto_ayuda=''
	palabras={}
	longitud=config_juego['longitud_maxima']+6
	if config_juego['orientacion']=='vertical':
		alto=longitud
		ancho=max(config_juego['cantidad_palabras']+3,alto)
		lista_posiciones=list(range(1,ancho+1))
	else:
		ancho=longitud
		alto=max(config_juego['cantidad_palabras']+3,ancho)
		lista_posiciones=list(range(1,alto+1))
		
	#a medida que se procesa cada palabra se designa sus coordenadas, se le asigna el color que le corresponde
	#y se suma su contenido necesario al texto de ayuda a ser mostrado
	cant_elim=0
	for palabra in config_juego['sustantivos']['palabras']:
		if config_juego['orientacion']=='vertical':
			posicion=(lista_posiciones.pop(random.randint(0,len(lista_posiciones)-1)),random.randint(1,longitud+1-len(palabra)))
		else:
			posicion=(random.randint(1,longitud+1-len(palabra)),lista_posiciones.pop(random.randint(0,len(lista_posiciones)-1)))
			
		if config_juego['ayuda']=='palabra':
			texto_ayuda=texto_ayuda+palabra+'\n'
		elif config_juego['ayuda']=='definicion':
			texto_ayuda=texto_ayuda+config_juego['sustantivos']['palabras'][palabra]
		else:
			texto_ayuda=texto_ayuda+palabra+': '+config_juego['sustantivos']['palabras'][palabra]
			
		palabras[palabra]={'inicio':posicion,'color':config_juego['sustantivos']['color']}
		cant_elim=cant_elim+1
	for palabra in config_juego['adjetivos']['palabras']:
		if config_juego['orientacion']=='vertical':
			posicion=(lista_posiciones.pop(random.randint(0,len(lista_posiciones)-1)),random.randint(1,longitud+1-len(palabra)))
		else:
			posicion=(random.randint(1,longitud+1-len(palabra)),lista_posiciones.pop(random.randint(0,len(lista_posiciones)-1)))
			
		if config_juego['ayuda']=='palabra':
			texto_ayuda=texto_ayuda+palabra+'\n'
		elif config_juego['ayuda']=='definicion':
			texto_ayuda=texto_ayuda+config_juego['adjetivos']['palabras'][palabra]
		else:
			texto_ayuda=texto_ayuda+palabra+': '+config_juego['adjetivos']['palabras'][palabra]
			
		palabras[palabra]={'inicio':posicion,'color':config_juego['adjetivos']['color']}
		cant_elim=cant_elim+1
	for palabra in config_juego['verbos']['palabras']:
		if config_juego['orientacion']=='vertical':
			posicion=(lista_posiciones.pop(random.randint(0,len(lista_posiciones)-1)),random.randint(1,longitud+1-len(palabra)))
		else:
			posicion=(random.randint(1,longitud+1-len(palabra)),lista_posiciones.pop(random.randint(0,len(lista_posiciones)-1)))
			
		if config_juego['ayuda']=='palabra':
			texto_ayuda=texto_ayuda+palabra+'\n'
		elif config_juego['ayuda']=='definicion':
			texto_ayuda=texto_ayuda+config_juego['verbos']['palabras'][palabra]
		else:
			texto_ayuda=texto_ayuda+palabra+': '+config_juego['verbos']['palabras'][palabra]
			
		palabras[palabra]={'inicio':posicion,'color':config_juego['verbos']['color']}
		cant_elim=cant_elim+1
	
	if config_juego['letras']=='mayusculas':
		letras_todas=string.ascii_uppercase
	else:
		letras_todas=string.ascii_lowercase
	#Una grilla de botones para jugar, una con los botones de los colores corresponmdientes para mostrar el resultado
	#correcto, una matriz para modificar durante el juego y una matriz para comparar si lo que hice es correcto
	grilla_resuelta=[]
	grilla_juego=[]
	grilla_botones=[]
	grilla_botones_resuelta=[]
	if config_juego['orientacion']=='vertical':
		for columna in range(1,ancho+1):
			grilla_resuelta.append([])
			grilla_juego.append([])
			grilla_botones.append([])
			grilla_botones_resuelta.append([])
			fila=1
			while fila<=alto:
				encontrada=False
				for palabra in palabras.keys():
					if (columna,fila)==palabras[palabra]['inicio']:
						encontrada=True
						sumado=0
						for letra_palabra in list(palabra):
							grilla_resuelta[columna-1].append(palabras[palabra]['color'])
							grilla_juego[columna-1].append(None)
							grilla_botones[columna-1].append([sg.Button(letra_palabra,button_color=('black','lightgrey'),size=(2,1),key=str(columna)+'_'+str(fila+sumado))])
							grilla_botones_resuelta[columna-1].append([sg.Button(letra_palabra,size=(2,1),button_color=('black',palabras[palabra]['color']))])
							sumado=sumado+1
						fila=fila+len(palabra)
						break
				if not encontrada:
					grilla_resuelta[columna-1].append(None)
					grilla_juego[columna-1].append(None)
					una_letra=random.choice(letras_todas)
					grilla_botones[columna-1].append([sg.Button(una_letra,button_color=('black','lightgrey'),size=(2,1),key=str(columna)+'_'+str(fila))])
					grilla_botones_resuelta[columna-1].append([sg.Button(una_letra,button_color=('black','lightgrey'),size=(2,1))])
					fila=fila+1
	else:
		for fila in range(1,alto+1):
			grilla_resuelta.append([])
			grilla_juego.append([])
			grilla_botones.append([])
			grilla_botones_resuelta.append([])
			columna=1
			while columna<=ancho:
				encontrada=False
				for palabra in palabras.keys():
					if (columna,fila)==palabras[palabra]['inicio']:
						encontrada=True
						sumado=0
						for letra_palabra in list(palabra):
							grilla_resuelta[fila-1].append(palabras[palabra]['color'])
							grilla_juego[fila-1].append(None)
							grilla_botones[fila-1].append(sg.Button(letra_palabra,button_color=('black','lightgrey'),size=(2,1),key=str(fila)+'_'+str(columna+sumado)))
							grilla_botones_resuelta[fila-1].append(sg.Button(letra_palabra,size=(2,1),button_color=('black',palabras[palabra]['color'])))
							sumado=sumado+1
						columna=columna+len(palabra)
						break
				if not encontrada:
					grilla_resuelta[fila-1].append(None)
					grilla_juego[fila-1].append(None)
					una_letra=random.choice(letras_todas)
					grilla_botones[fila-1].append(sg.Button(una_letra,button_color=('black','lightgrey'),size=(2,1),key=str(fila)+'_'+str(columna)))
					grilla_botones_resuelta[fila-1].append(sg.Button(una_letra,button_color=('black','lightgrey'),size=(2,1)))
					columna=columna+1
					
	if config_juego['orientacion']=='vertical':
		columna_grilla_layout=[]
		columna_grilla_resuelta_layout=[]
		for fila in range(0,alto):
			columna_grilla_layout.append([])
			columna_grilla_resuelta_layout.append([])
			for columna_buttons in grilla_botones:
				columna_grilla_layout[fila].extend(columna_buttons[fila])
			for columna_resuelta in grilla_botones_resuelta:
				columna_grilla_resuelta_layout[fila].extend(columna_resuelta[fila])
			fila=fila+1
	else:
		columna_grilla_layout=[]
		columna_grilla_resuelta_layout=[]
		for fila_buttons in grilla_botones:
			columna_grilla_layout.append(fila_buttons)
		for fila_resuelta in grilla_botones_resuelta:
			columna_grilla_resuelta_layout.append(fila_resuelta)
	
	#inicio con el color de los sustantivos, para no iniciar en nada
	color_actual=config_juego['sustantivos']['color']
	
	layout_solucion=[]
	layout_solucion.extend(columna_grilla_resuelta_layout)
	layout_solucion.append([sg.Text('',background_color=config_juego['estilo'])])
	layout_solucion.append([sg.Button('Salir',size=(20,2))])
				
	columna_elegir_tipo=[
						[sg.Text('Elegir color',size=(10,2),background_color=config_juego['estilo'])],
						[sg.Button('Sustantivos',disabled=True,key='Elegir_sust',size=(10,2),button_color=('black',config_juego['sustantivos']['color']))],
						[sg.Text('',background_color=config_juego['estilo'])],
						[sg.Button('Adjetivos',disabled=False,key='Elegir_adj',size=(10,2),button_color=('black',config_juego['adjetivos']['color']))],
						[sg.Text('',background_color=config_juego['estilo'])],
						[sg.Button('Verbos',disabled=False,key='Elegir_verb',size=(10,2),button_color=('black',config_juego['verbos']['color']))],
						]
	columna_informacion=[
						[sg.Text('Cantidad de Sustantivos: '+str(config_juego['sustantivos']['cantidad']),size=(20,2),background_color=config_juego['estilo'])],
						[sg.Text('Cantidad de Adjetivos: '+str(config_juego['adjetivos']['cantidad']),size=(20,2),background_color=config_juego['estilo'])],
						[sg.Text('Cantidad de Verbos: '+str(config_juego['verbos']['cantidad']),size=(20,2),background_color=config_juego['estilo'])],
						]
						
	lista_aux=[sg.Column(columna_elegir_tipo,background_color=config_juego['estilo']),sg.Text('',background_color=config_juego['estilo'])]
	lista_aux.append(sg.Column(columna_grilla_layout))
	lista_aux.append(sg.Text('',background_color=config_juego['estilo']))
	lista_aux.append(sg.Column(columna_informacion,background_color=config_juego['estilo']))
						
	layout_juego=[
			[sg.Column(columna_elegir_tipo,background_color=config_juego['estilo']),
			sg.Text('',background_color=config_juego['estilo']),
			sg.Column(columna_grilla_layout,background_color=config_juego['estilo']),
			sg.Text('',background_color=config_juego['estilo']),
			sg.Column(columna_informacion,background_color=config_juego['estilo'])],
			[sg.Text('',background_color=config_juego['estilo'])],
			[sg.Multiline(texto_ayuda,size=(80,5),disabled=True,visible=(config_juego['ayuda']!='sin'))],
			[sg.Button('Enviar resultado',size=(35,2),key='Enviar_resultado'),sg.Button('Salir',size=(35,2),key='Salir')]
			]
				
	ventana_juego=sg.Window('Sopa de letras',element_padding=(0,0),background_color=config_juego['estilo'],margins=(10,30)).Layout(layout_juego)
	while True:
		event_juego,values_juego=ventana_juego.Read()
		if event_juego==None:
			break
		if event_juego=='Salir':
			if sg.PopupYesNo('Seguro que desea salir?')=='Yes':
				break
		elif event_juego=='Elegir_sust':
			color_actual=config_juego['sustantivos']['color']
			ventana_juego.FindElement('Elegir_sust').Update(disabled=True)
			ventana_juego.FindElement('Elegir_adj').Update(disabled=False)
			ventana_juego.FindElement('Elegir_verb').Update(disabled=False)
		elif event_juego=='Elegir_adj':
			color_actual=config_juego['adjetivos']['color']
			ventana_juego.FindElement('Elegir_sust').Update(disabled=False)
			ventana_juego.FindElement('Elegir_adj').Update(disabled=True)
			ventana_juego.FindElement('Elegir_verb').Update(disabled=False)
		elif event_juego=='Elegir_verb':
			color_actual=config_juego['verbos']['color']
			ventana_juego.FindElement('Elegir_sust').Update(disabled=False)
			ventana_juego.FindElement('Elegir_adj').Update(disabled=False)
			ventana_juego.FindElement('Elegir_verb').Update(disabled=True)
		elif event_juego=='Enviar_resultado':
			if grilla_juego==grilla_resuelta:
				sg.Popup('Felicidades, respuesta correcta!')
			else:
				if sg.PopupYesNo('Respuesta Incorrecta\n¿Desea ver la solución?')=='Yes':
					ventana_solucion=sg.Window('Solución',background_color=config_juego['estilo'],element_padding=(0,0),margins=(10,30)).Layout(layout_solucion)
					event_solucion,values_solucion=ventana_solucion.Read()
					ventana_solucion.Close()
					break
		else:
			coordenadas=event_juego.split('_')
			fila=int(coordenadas[0])		
			columna=int(coordenadas[1])
			if grilla_juego[fila-1][columna-1]==color_actual:
				ventana_juego.FindElement(event_juego).Update(button_color=('black','lightgrey'))
				grilla_juego[fila-1][columna-1]=None
			else:
				ventana_juego.FindElement(event_juego).Update(button_color=('black',color_actual))	
				grilla_juego[fila-1][columna-1]=color_actual
	ventana_juego.Close()

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
	valido,config_juego=config_valida(dic_config)
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
				config=Configurar(reporte_pantalla,dic_config)
				valido,config_juego=config_valida(config)
				if reporte_pantalla['No encontrado']!='' or reporte_pantalla['No coinciden']!='':
					ventana_menu.FindElement('Reporte').Update(disabled=False)
					if config==None:
						config={'tipografia titulo':'Times ','tipografia cuerpo':'Times '}
				if valido:
					dic_config=config
					if not os.path.exists(os.path.join(ruta_app,'configuracion anterior')):
						os.mkdir(os.path.join(ruta_app,'configuracion anterior'))
					archconfig=open(os.path.join(ruta_app,'configuracion anterior','config.json'),'w+')
					json.dump(dic_config,archconfig)	
					archconfig.close()
					ventana_menu.FindElement('Jugar').Update(disabled=False)
			elif event_menu[0]=='Reporte':
				reporte(reporte_pantalla,config['tipografia titulo'],config['tipografia cuerpo'])
			elif event_menu[0]=='Jugar':
				juego(config_juego)
			ventana_menu.UnHide()
	ventana_menu.Close()
