#quandl.ApiConfig.api_key = "HWWiy9cYQYxJhaoCi1ac"
#data = quandl.get_table('MER/F1', compnumber="39102", paginate=True)
#import quandl
#https://finviz.com/screener.ashx
from tkinter import *
from tkinter import ttk
from bs4 import BeautifulSoup
import requests
import json
import time
import xlsxwriter
import os

window = Tk()
actions = []

def downloadTables(tableIndex):
	i = 0
	f = open('tablas.html', 'w')
	while i < 7451:
		if i == 0:
			req = requests.get('https://finviz.com/screener.ashx?v=311')
			page = req.text
			soup = BeautifulSoup(req.text, 'html.parser')
			tables = soup.findAll('div', {'id': 'screener-content'})
			f.write(tables[0].prettify())
			i = i + 11

		if tableIndex == 0:
			req = requests.get('https://finviz.com/screener.ashx?v=311&r=' + str(i))
		else:
			req = requests.get('https://finviz.com/screener.ashx?v=311&r=' + str(i) + '&ft=' + str(tableIndex))

		page = req.text
		soup = BeautifulSoup(req.text, 'html.parser')
		tables = soup.findAll('div', {'id': 'screener-content'})

		if tableIndex != 0:
			f.close()
			f = open('tablas'+str((tableIndex + 1))+'.html', 'w')
		f.write('\n' + tables[0].prettify())
	
		i = i + 10
		
	f.close()

def downloadAllTables():
	j = 0
	while j < 4:
		downloadTables(j)

def downloadImg():

	os.mkdir('graficas')

	header = 0
	while header < 7441:
		if header == 0:
			req = requests.get('https://finviz.com/screener.ashx')
			soup = BeautifulSoup(req.text, 'html.parser')

			acciones = soup.findAll('tr', {'class': 'table-dark-row-cp'})
			for accion in acciones:
				celdas = accion.findAll('td', {'class': 'screener-body-table-nw'})
				nombreAccion = celdas[1].get_text()
				actions.append(nombreAccion)

			accionesW = soup.findAll('tr', {'class': 'table-light-row-cp'})
			for accionW in accionesW:
				celdasW = accionW.findAll('td', {'class': 'screener-body-table-nw'})
				nombreAccionW = celdasW[1].get_text()
				actions.append(nombreAccionW)

			for action in actions:
				page = requests.get('https://finviz.com/chart.ashx?t='+action+'&ta=1&ty=c&p=d&s=l')
				img = page.content	
				with open('graficas/'+action+'.png', 'wb') as handler:
					handler.write(img)
			header = header + 21	
		
		req = requests.get('https://finviz.com/screener.ashx?v=111&r='+str(header))
		soup = BeautifulSoup(req.text, 'html.parser')

		acciones = soup.findAll('tr', {'class': 'table-dark-row-cp'})
		for accion in acciones:
			celdas = accion.findAll('td', {'class': 'screener-body-table-nw'})
			nombreAccion = celdas[1].get_text()
			actions.append(nombreAccion)

		accionesW = soup.findAll('tr', {'class': 'table-light-row-cp'})
		for accionW in accionesW:
			celdasW = accionW.findAll('td', {'class': 'screener-body-table-nw'})
			nombreAccionW = celdasW[1].get_text()
			actions.append(nombreAccionW)

		for action in actions:
			page = requests.get('https://finviz.com/chart.ashx?t='+action+'&ta=1&ty=c&p=d&s=l')
			img = page.content	
			with open('graficas/'+action+'.png', 'wb') as handler:
				handler.write(img)	

		header = header + 21
def createFile():
	file = open('acciones.csv', 'w')
	file.write('No.' + ',' + 'Ticker' + ',' + 'Company' + ',' + 'Sector' + ',' + 'Industry' + ',' + 'Country' + ',' + 'Market Cap' + ',' + 'P/E' + ',' + 'Price' + ',' + 'Change' + ',' + 'Volume' + '\n')
	header = 0
	while header < 7441:
		if header == 0:
			url = 'https://finviz.com/screener.ashx'
			r = requests.get(url)
			soup = BeautifulSoup(r.text, 'html.parser')
			actions = soup.findAll('tr', {'class': 'table-dark-row-cp'})

			for action in actions:
				cells = action.findAll('td', {'class': 'screener-body-table-nw'})
				for cell in cells:
					file.write(cell.get_text() + ',')
				file.write('\n')

			actionsW = soup.findAll('tr', {'class': 'table-light-row-cp'})

			for actionW in actionsW:
				cellsW = actionW.findAll('td', {'class': 'screener-body-table-nw'})
				for cellW in cellsW:
					file.write(cellW.get_text() + ',')
				file.write('\n')

			header = header + 21
		

		url = 'https://finviz.com/screener.ashx?v=111&r='+str(header)
		r = requests.get(url)
		soup = BeautifulSoup(r.text, 'html.parser')
		actions = soup.findAll('tr', {'class': 'table-dark-row-cp'})

		for action in actions:
			cells = action.findAll('td', {'class': 'screener-body-table-nw'})
			for cell in cells:
				file.write(cell.get_text() + ',')
			file.write('\n')
		
		actionsW = soup.findAll('tr', {'class': 'table-light-row-cp'})

		for actionW in actionsW:
			cellsW = actionW.findAll('td', {'class': 'screener-body-table-nw'})
			for cellW in cellsW:
				file.write(cellW.get_text() + ',')
			file.write('\n')
		header = header + 20
	file.close()

	workbook = xlsxwriter.Workbook('acciones.xlsx')
	worksheet = workbook.add_worksheet()

	worksheet.set_column('A:A', 20)

	csv = open('acciones.csv', 'r')
	csvLines = csv.readlines()

	y = 0
	
	for line in csvLines:
		lineArray = str(line).split(',')
		x = 0
		for cell in lineArray:
			worksheet.write(y, x, cell)
			x = x + 1
		y = y + 1
	#print(str(csvLines))

	workbook.close()
	return main()
	
def searchAction(url, value):
	#key =  'IX09TC435VGY2C5F'
	#r = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+value+'&apikey='+key)
	#print(r.text)
	r = requests.get(url)
	soup = BeautifulSoup(r.text, 'html.parser')
	actions = soup.findAll('tr', {'class': 'table-dark-row-cp'})

	for action in actions:
		cells = action.findAll('td', {'class': 'screener-body-table-nw'})
		if cells[1].get_text() == value:
			newWindow = Tk()
			newFrame = ttk.Frame(newWindow, padding = '100 100 40 20', borderwidth = 20, relief = 'sunken')
			ttk.Label(newWindow, text= 'Acción Requerida: ' + str(cells[1].get_text()), foreground = 'purple').place(x=50, y=100)
			ttk.Label(newWindow, text= 'P/E: ' + str(cells[7].get_text()), foreground  = 'green').place(x=50, y=120)
			ttk.Label(newWindow, text= 'Price: ' + str(cells[8].get_text()), foreground = 'red').place(x=50, y=140)
			ttk.Label(newWindow, text= 'Change: ' + str(cells[9].get_text()), foreground = 'brown').place(x=50, y=160)
			ttk.Label(newWindow, text= 'Change: ' + str(cells[10].get_text()), foreground = 'brown').place(x=50, y=180)
			return main()

	actionsW = soup.findAll('tr', {'class': 'table-light-row-cp'})
	for actionW in actionsW:
		cellsW = actionW.findAll('td', {'class': 'screener-body-table-nw'})
		if cellsW[1].get_text() == value:
			newWindow = Tk()
			newFrame = ttk.Frame(newWindow, padding = '100 100 40 20', borderwidth = 20, relief = 'sunken')
			ttk.Label(newWindow, text= 'Acción Requerida: ' + str(cellsW[1].get_text()), foreground = 'purple').place(x=50, y=100)
			ttk.Label(newWindow, text= 'P/E: ' + str(cellsW[7].get_text()), foreground  = 'green').place(x=50, y=120)
			ttk.Label(newWindow, text= 'Price: ' + str(cellsW[8].get_text()), foreground = 'red').place(x=50, y=140)
			ttk.Label(newWindow, text= 'Change: ' + str(cellsW[9].get_text()), foreground = 'brown').place(x=50, y=160)
			ttk.Label(newWindow, text= 'Change: ' + str(cellsW[10].get_text()), foreground = 'brown').place(x=50, y=180)
			return main()

def searchLoop(value):
	header = 0
	while header < 7441:
		if header == 0:
			url = 'https://finviz.com/screener.ashx'
			searchAction(url, value)
			header = header + 21

		url = 'https://finviz.com/screener.ashx?v=111&r='+str(header)
		searchAction(url, value)
		header = header + 20

def main():
	frame = ttk.Frame(window, padding = '100 100 40 20', borderwidth = 20, relief = 'sunken')
	ttk.Label(window, text= "Ingrese la Acción").place(x=50, y=9)
	value = StringVar()
	entry = ttk.Entry(window, width=15, textvariable = value).place(x=50, y=35)
	ttk.Button(window, text='Buscar', command = lambda: searchLoop(value.get())).place(x = 55, y = 60)
	ttk.Button(window, text='Crear Archivo', command = createFile).place(x = 45, y = 90)
	ttk.Button(window, text='Descargar Gráficas', command = downloadImg).place(x = 65, y = 120)
	ttk.Button(window, text='Descargar Tablas', command = downloadAllTables).place(x = 65, y = 140)
	window.mainloop()

if __name__ == '__main__':
	main()