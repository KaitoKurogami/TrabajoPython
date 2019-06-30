from pattern.es import parse
import PySimpleGUI as sg
from buscar_wiki import palabra_wiki as pw
import os
ruta_app = os.getcwd()

			
def obtener_datos(palabra,reporte_pantalla,hoy):
	'''
	recibe una palabra, un diccionario con los dos tipos de reportes a hacer en pantalla los cuales actualizará
	y la fecha de hoy vista como dia mes año para poder nombrar el log de reporte según el dia
	si se agrega el elemento a la lista de palabras retorna un diccionario con el tipo y la descripcion
	sino retorna None
	'''
	tipo,desc=pw.InfoPalabraWiktionary(palabra)
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
		reporte_texto=palabra+': En Wiktionary se considera: '+tipo+', pero en pattern se considera un '+tipoPattern+'\n'
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
		
