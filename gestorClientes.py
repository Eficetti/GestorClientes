from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3

root = Tk()
root.title('Hola Mundo CRM')

conn = sqlite3.connect('crm.db')
c = conn.cursor()
c.execute('CREATE TABLE if not exists cliente (id INTEGER PRIMARY KEY AUTOINCREMENT,nombre TEXT NOT NULL,telefono TEXT NOT NULL,empresa TEXT NOT NULL);')

def renderClientes():
    rows = c.execute('SELECT * FROM cliente').fetchall()
    
    tree.delete(*tree.get_children())

    for row in rows:
        tree.insert('', END, row[0], values=(row[1],row[2],row[3]))


def insertar(cliente):
    c.execute('INSERT INTO cliente (nombre,telefono,empresa) VALUES (?, ?, ?)', (cliente['nombre'],cliente['telefono'],cliente['empresa']))
    conn.commit()
    renderClientes()

def nuevoCliente():
    def guardar():
        if not nombre.get():
            messagebox.showerror('Error', 'El nombre es obligatorio')
            return
        elif not telefono.get():
            messagebox.showerror('Error', 'El telefono es obligatorio')
            return
        elif not empresa.get():
            messagebox.showerror('Error', 'La empresa es obligatoria')
            return

        cliente = {
            'nombre': nombre.get(),
            'telefono': telefono.get(),
            'empresa': empresa.get()
        }
        insertar(cliente)
        top.destroy()


    top = Toplevel()
    top.title('Nuevo Cliente')

    lnombre = Label(top,text='Nombre')
    nombre = Entry(top, width=40)
    lnombre.grid(row=0, column=0)
    nombre.grid(row=0, column=1)

    ltelefono = Label(top,text='Teléfono')
    telefono = Entry(top, width=40)
    ltelefono.grid(row=1, column=0)
    telefono.grid(row=1, column=1)

    lempresa = Label(top,text='Empresa')
    empresa = Entry(top, width=40)
    lempresa.grid(row=2, column=0)
    empresa.grid(row=2, column=1)

    guardar = Button(top, text='Guardar', command=guardar)
    guardar.grid(row=3,column=1)

    top.mainloop()


def eliminarCliente():
    id = tree.selection()[0]
    
    cliente = c.execute('SELECT * FROM cliente WHERE id = ?', (id, )).fetchone()
    respuesta = messagebox.askokcancel(f'Seguro?', 'Estas seguro de eliminar el cliente ' + cliente[1] + '?')

    if respuesta:
        c.execute('DELETE FROM cliente WHERE id = ?',(id,))
        conn.commit()
        renderClientes()
    else:
        pass

btn = Button(root, text='Nuevo Cliente', command=nuevoCliente)
btn.grid(column=0, row=0)

btnEliminar = Button(root, text='Eliminar Cliente', command=eliminarCliente)
btnEliminar.grid(column=1, row=0)

tree = ttk.Treeview(root)
tree['columns'] = ('Nombre','Telefono', 'Empresa')
tree.column('#0', width=0, stretch=NO)
tree.column('Nombre')
tree.column('Telefono')
tree.column('Empresa')

tree.heading('Nombre', text='Nombre')
tree.heading('Telefono', text='Teléfono')
tree.heading('Empresa', text='Empresa')
tree.grid(column=0,row=1, columnspan=2)
renderClientes()
root.mainloop()