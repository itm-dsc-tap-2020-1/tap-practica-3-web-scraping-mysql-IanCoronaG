from urllib.request import urlopen
from bs4 import BeautifulSoup
import mysql.connector as mysql
import tkinter as tk
from tkinter import *
from tkinter import ttk

conexion = mysql.connect( host='localhost', user= 'root', passwd='', db='prac3' )
operacion = conexion.cursor(buffered=True)

links = []

def checksts(pag):
    try:
        html=urlopen(pag)
        soup=BeautifulSoup(html, 'html.parser')
        for link in soup.findAll('a'):
            print('href: {}'.format(link.get('href')))
            links.append(link.get('href'))
            try:
                ex='INSERT INTO webs values("'+link.get('href')+'", False)'
                operacion.execute(ex)
            except:
                print("valor duplicado")
    except:
        print("No se pudo acceder a "+pag+"\n")

    operacion.execute("UPDATE webs SET estatus=1 WHERE pagina='"+pag+"'")
    conexion.commit()



def boton():
    url=str(p.get())
    #http://sagitario.itmorelia.edu.mx/~rogelio/hola.htm
    html=urlopen(url)
    soup=BeautifulSoup(html, 'html.parser')
    print("\nExtraer los enlaces de la pagina web: "+url+"\n")
    

    ex='INSERT INTO webs values("'+url+'", False)'
    try:
        operacion.execute(ex)
    except:
        print()

    operacion.execute( 'select * from webs where estatus=0')
    conexion.commit()
    for pag, trsh in operacion:
        print("\ntrabajando con "+pag+"\n")
        checksts(pag)
        print("\nTerminó de Revisar Enlaces de "+pag)
        operacion.execute( 'select * from webs where estatus=0')

    print("Terminó de Revisar los enlaces.")
    conexion.commit()
    conexion.close()


v=tk.Tk()
v.title('Web Scrapping')
#v.geometry('380x350')
pg=tk.StringVar()

main=ttk.LabelFrame(v,relief='solid')
tk.Label(main, text="Ingresa la direccion de la página web: ").pack(padx=10,pady=10)
p=tk.Entry(main, textvariable=pg, width=45)
p.pack(padx=10, pady=10)

bt=ttk.Button(main, text='Aceptar', command=boton).pack(padx=10, pady=10)

main.pack(padx=20, pady=20)


v.mainloop()