from pattern.web import Wiktionary
import PySimpleGUI as sg


def InfoPalabraWiktionary(palabra):
	'''
	Recibe una palabra, la busca en wiktionary y retorna si es sustantivo,
	adjetivo o verbo, y una definición
	Si no encuentra nada, returna None,None
	'''
	layout=[
			[sg.Text('Al cerrarse esto comenzará a buscar la palabra\nNo debería tardar mas de 30 segundos')],
			]
	ventana_buscando=sg.Window('Buscando',no_titlebar=True, auto_close=True,auto_close_duration=5).Layout(layout)
	ventana_buscando.Show()
	fin=False
	esp=False
	article = Wiktionary(language="es").search(palabra) 
	ventana_buscando.Close()
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
