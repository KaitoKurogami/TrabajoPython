import PySimpleGUI as sg


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
	
