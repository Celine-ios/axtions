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

window = Tk()

def searchByDate(date, action):
	response = requests.get('https://finance.yahoo.com/quote/SONO/history?p=SONO')
	page = response.text
	yahoo = BeautifulSoup(page, 'html.parser')
	rows = yahoo.findAll('tr', {'class': 'BdT Bdc($c-fuji-grey-c) Ta(end) Fz(s) Whs(nw)'})
	print(rows)
	print(date+ ' ' +action)
	
def createFile():

	file = open('acciones.txt', 'w')

	r = requests.get('https://finviz.com/screener.ashx')
	soup = BeautifulSoup(r.text, 'html.parser')
	actions = soup.findAll('tr', {'class': 'table-dark-row-cp'})

	for action in actions:
		cells = action.findAll('td', {'class': 'screener-body-table-nw'})
		for cell in cells:
			file.write(cell.get_text() + ' ')
		file.write('\n')
	file.close()
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
	window.mainloop()

if __name__ == '__main__':
	main()