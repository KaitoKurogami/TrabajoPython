import string
import PySimpleGUI as sg
import random


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
	lista_tipos=['sustantivos','adjetivos','verbos']
	for tipo in lista_tipos:
		for palabra in config_juego[tipo]['palabras']:
			if config_juego['orientacion']=='vertical':
				posicion=(lista_posiciones.pop(random.randint(0,len(lista_posiciones)-1)),random.randint(1,longitud+1-len(palabra)))
			else:
				posicion=(random.randint(1,longitud+1-len(palabra)),lista_posiciones.pop(random.randint(0,len(lista_posiciones)-1)))
				
			if config_juego['ayuda']=='palabra':
				texto_ayuda=texto_ayuda+palabra+'\n'
			elif config_juego['ayuda']=='definicion':
				texto_ayuda=texto_ayuda+config_juego[tipo]['palabras'][palabra]
			else:
				texto_ayuda=texto_ayuda+palabra+': '+config_juego[tipo]['palabras'][palabra]
				
			palabras[palabra]={'inicio':posicion,'color':config_juego[tipo]['color']}
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
			[sg.Button('Enviar resultado',size=(20,2),key='Enviar_resultado'),sg.Button('Salir',size=(20,2),key='Salir'),
			sg.Button('Mostrar Ayuda',size=(20,2),key='mostrar_ayuda',disabled=(config_juego['ayuda']=='sin')),
			sg.Button('Ocultar Ayuda',size=(20,2),key='ocultar_ayuda',visible=False)],
			[sg.Text('',background_color=config_juego['estilo'])],
			[sg.Multiline(texto_ayuda,size=(80,5),visible=False,key='lista_ayuda')]
			]
				
	ventana_juego=sg.Window('Sopa de letras',element_padding=(0,0),background_color=config_juego['estilo'],margins=(10,30)).Layout(layout_juego)
	while True:
		event_juego,values_juego=ventana_juego.Read()
		if event_juego==None:
			break
		if event_juego=='Salir':
			if sg.PopupYesNo('Seguro que desea salir?')=='Yes':
				break
		elif event_juego=='mostrar_ayuda':
			ventana_juego.Size=(ventana_juego.Size[0],ventana_juego.Size[1]+83)
			ventana_juego.FindElement('lista_ayuda').Update(visible=True)
			ventana_juego.FindElement('mostrar_ayuda').Update(visible=False)
			ventana_juego.FindElement('ocultar_ayuda').Update(visible=True)
			ventana_juego.Refresh()
		elif event_juego=='ocultar_ayuda':
			ventana_juego.Size=(ventana_juego.Size[0],ventana_juego.Size[1]-83)
			ventana_juego.FindElement('lista_ayuda').Update(visible=False)
			ventana_juego.FindElement('mostrar_ayuda').Update(visible=True)
			ventana_juego.FindElement('ocultar_ayuda').Update(visible=False)
			ventana_juego.Refresh()
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
				if sg.PopupYesNo('Respuesta Incorrecta\n¿Desea ver la solución?\nSe considerará como perdido')=='Yes':
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
