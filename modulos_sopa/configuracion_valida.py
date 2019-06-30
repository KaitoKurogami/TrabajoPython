import PySimpleGUI as sg
import json
import random
import os
ruta_app = os.getcwd()
frio='#58C9FE'
fin_color_frio=20
templado='#1EC733'
inicio_calido=30
calor='#FF2525'
palabras_max=20

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
		contadores={'sustantivos':0,'adjetivos':0,'verbos':0}
		max_long=0
		total=0
		for tipo_palabra in contadores.keys():
			for num in range(0,int(dic_config['cant_'+tipo_palabra])):
				try:
					if(total<palabras_max):
						Pelegida=random.choice(list(palabras_por_tipo[tipo_palabra].keys()))
						Delegida=palabras_por_tipo[tipo_palabra].pop(Pelegida)
						if dic_config['MayusOMinus']=='mayusculas':
							Pelegida=Pelegida.upper()
						palabras_final[tipo_palabra][Pelegida]=Delegida
						if len(Pelegida)>max_long:
							max_long=len(Pelegida)
						contadores[tipo_palabra]=contadores[tipo_palabra]+1
						total=total+1
				except IndexError:
					break
		#reviso si hay al menos una palabra
		if total==0:
			return False,{}
		else:
			sustantivos={'cantidad':contadores['sustantivos'],'color':dic_config['colores']['Sustantivos'],
			'palabras':palabras_final['sustantivos']}
			adjetivos={'cantidad':contadores['adjetivos'],'color':dic_config['colores']['Adjetivos'],
			'palabras':palabras_final['adjetivos']}
			verbos={'cantidad':contadores['verbos'],'color':dic_config['colores']['Verbos'],
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
