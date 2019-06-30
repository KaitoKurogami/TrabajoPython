import PySimpleGUI as sg

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
