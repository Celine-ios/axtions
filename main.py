#quandl.ApiConfig.api_key = "HWWiy9cYQYxJhaoCi1ac"
#data = quandl.get_table('MER/F1', compnumber="39102", paginate=True)
#import quandl
#https://finviz.com/screener.ashx
from tkinter import *
from tkinter import ttk
from bs4 import BeautifulSoup
import requests

def searchAction():
	key =  'IX09TC435VGY2C5F'
	print(action.get())
	r = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=ADS.DE&apikey='+key)
	#r = requests.get('https://finviz.com/screener.ashx')
	#print(r.text)

def main():
	window = Tk()
	frame = ttk.Frame(window, padding = '100 100 20 20', borderwidth = 20, relief = 'sunken')
	action = StringVar()
	ttk.Label(window, text= "Ingrese la Acción", relief = RAISED).place(x=50, y=9)
	ttk.Entry(window,textvariable=action,width=15).place(x=50, y=35)
	ttk.Button(window, text='Buscar', command = searchAction(action)).place(x = 55, y = 60)
	window.mainloop()

if __name__ == '__main__':
	main()