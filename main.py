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

def searchAction(value):
	key =  'IX09TC435VGY2C5F'
	r = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+value+'&apikey='+key)
	#r = requests.get('https://finviz.com/screener.ashx')
	results = json.loads(r.text)
	ttk.Label(window, text= 'Abrió: '+results['Time Series (Daily)'][time.strftime("20%y-%m-%d")]['1. open'], foreground = 'purple').place(x=50, y=100)
	ttk.Label(window, text= 'Alto: '+results['Time Series (Daily)'][time.strftime("20%y-%m-%d")]['2. high'], foreground  = 'green').place(x=50, y=120)
	ttk.Label(window, text= 'Bajo: '+results['Time Series (Daily)'][time.strftime("20%y-%m-%d")]['3. low'], foreground = 'red').place(x=50, y=140)
	ttk.Label(window, text= 'Cerró: '+results['Time Series (Daily)'][time.strftime("20%y-%m-%d")]['4. close'], foreground = 'brown').place(x=50, y=160)

def main():
	frame = ttk.Frame(window, padding = '100 100 20 20', borderwidth = 20, relief = 'sunken')
	ttk.Label(window, text= "Ingrese la Acción").place(x=50, y=9)
	value = StringVar()
	entry = ttk.Entry(window, width=15, textvariable = value).place(x=50, y=35)
	ttk.Button(window, text='Buscar', command = lambda: searchAction(value.get())).place(x = 55, y = 60)
	window.mainloop()

if __name__ == '__main__':
	main()