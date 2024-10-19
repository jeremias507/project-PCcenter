import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import util.util_ventana as util_ventana
from tkinter import Frame, Entry, Button
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from aplicacion.servicio_producto import ServicioProducto

COLOR_FONDO = "#fff"
COLOR_FONDO_BUSQUEDA = "#f7f8fa"

class FormularioRegistroDesign(tk.Tk):

    def __init__(self):
        super().__init__()

        self.config_window()
        self.crear_paneles()
        self.crear_controles()

    def config_window(self):
        self.title('Python CRUD')
        w, h = 800, 500
        util_ventana.centrar_ventana(self, w, h)
        self.configure(bg=COLOR_FONDO_BUSQUEDA)

    def obtener_conf_btn_pack(self):
        return {"side": tk.RIGHT, "padx": 10, "pady": 10}

    def crear_paneles(self):
        self.marco_titulo = tk.Frame(self, bg=COLOR_FONDO_BUSQUEDA, height=40)
        self.marco_titulo.pack(side=tk.TOP, fill='both')

        self.marco_registro = tk.Frame(self, bg="blue", height=50)
        self.marco_registro.pack(side=tk.TOP, fill='both', pady=10)

        self.marco_acciones = tk.Frame(self, bg=COLOR_FONDO, height=50)
        self.marco_acciones.pack(side=tk.TOP, fill='both')

        self.marco_productos = tk.Frame(self, bg="black")
        self.marco_productos.pack(side=tk.TOP, fill='both', padx=30, pady=15, expand=True)

    def crear_controles(self):
        title = tk.Label(self.marco_titulo, text="REGISTRAR PRODUCTO", font=('Roboto', 20), fg="#485159",
                         bg=COLOR_FONDO_BUSQUEDA, pady=20)
        title.pack(expand=True, fill=tk.BOTH)

        etiqueta_id = tk.Label(self.marco_registro, text="Id:", font=('Times', 14), fg="#666a88", bg=COLOR_FONDO,
                               width=5)
        etiqueta_id.pack(side="left", padx=5, pady=10)

        self.campo_id = ttk.Entry(self.marco_registro, font=('Times', 14), state="readonly", width=5)
        self.campo_id.pack(side="left", padx=5, pady=10)

        etiqueta_nombre = tk.Label(self.marco_registro, text="Producto:", font=('Times', 14), fg="#666a88",
                                   bg=COLOR_FONDO)
        etiqueta_nombre.pack(side="left", padx=5, pady=10)
        self.campo_nombre = ttk.Entry(self.marco_registro, font=('Times', 14))
        self.campo_nombre.pack(side="left", padx=5, pady=10)

        etiqueta_precio = tk.Label(self.marco_registro, text="Precio:", font=('Times', 14), fg="#666a88",
                                   bg=COLOR_FONDO)
        etiqueta_precio.pack(side="left", padx=5, pady=10)
        self.campo_precio = ttk.Entry(self.marco_registro, font=('Times', 14))
        self.campo_precio.pack(side="left", padx=5, pady=10)

        etiqueta_correo = tk.Label(self.marco_registro, text="Correo:", font=('Times', 14), fg="#666a88",
                                  bg=COLOR_FONDO)
        etiqueta_correo.pack(side="left", padx=5, pady=10)
        self.campo_correo = ttk.Entry(self.marco_registro, font=('Times', 14))
        self.campo_correo.pack(side="left", padx=5, pady=10)

        # Botones
        self.btn_eliminar_todos = tk.Button(self.marco_acciones, text="Eliminar Todos", font=('Times', 13),
                                            bg='#ed5153', bd=0, fg="#fff", padx=15, command=self.eliminar_todos)
        self.btn_eliminar_todos.pack(**self.obtener_conf_btn_pack())

        self.btn_eliminar = tk.Button(self.marco_acciones, text="Eliminar", font=('Times', 13), bg='#ed5153', bd=0,
                                      fg="#fff", padx=15, command=self.eliminar_producto)
        self.btn_eliminar.pack(**self.obtener_conf_btn_pack())  # Mostrar siempre

        self.btn_modificar = tk.Button(self.marco_acciones, text="Modificar", font=('Times', 13), bg='#536270', bd=0,
                                       padx=15, fg="#fff", command=self.modificar_producto)
        self.btn_modificar.pack(**self.obtener_conf_btn_pack())  # Mostrar siempre

        self.btn_limpiar_campos = tk.Button(self.marco_acciones, text="Limpiar Campos", font=('Times', 13),
                                            bg='#e39531', bd=0, padx=15, fg="#fff", command=self.limpiar_campos)
        self.btn_limpiar_campos.pack(**self.obtener_conf_btn_pack())

        self.btn_imprimir_factura = tk.Button(self.marco_acciones, text="Imprimir Factura", font=('Times', 13),
                                              bg='#007b00', bd=0, padx=15, fg="#fff", command=self.imprimir_factura)
        self.btn_imprimir_factura.pack(**self.obtener_conf_btn_pack())

        self.btn_registro = tk.Button(self.marco_acciones, text="Registrar", font=('Times', 13), bg='#51aded', bd=0,
                                      fg="#fff", padx=15, command=self.registrar_producto)
        self.btn_registro.pack(**self.obtener_conf_btn_pack())


        # Configuración del Treeview
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Treeview", background="#eafbea", foreground="#000")
        style.configure('Treeview.Heading', background="#6f9a8d", foreground="#fff")

        tree_scroll = ttk.Scrollbar(self.marco_productos)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree = ttk.Treeview(self.marco_productos, show='headings', yscrollcommand=tree_scroll.set)
        self.tree['columns'] = ('Id', 'Nombre', 'Precio', 'Cédula', 'Correo')
        self.tree.column('#0', width=0, stretch=tk.NO)
        self.tree.column('Id', anchor=tk.W, width=120)
        self.tree.column('Nombre', anchor=tk.W, width=250)
        self.tree.column('Precio', anchor=tk.W, width=120)

        self.tree.heading('Id', text='Id', anchor=tk.W)
        self.tree.heading('Nombre', text='Nombre', anchor=tk.W)
        self.tree.heading('Precio', text='Precio', anchor=tk.W)


        self.tree.pack(expand=True, fill='both')
        self.tree.bind("<<TreeviewSelect>>", self.al_seleccionar_treeview)

        tree_scroll.config(command=self.tree.yview)

        self.tree.tag_configure('evenrow', background="#c8e1f4")
        self.tree.tag_configure('oddrow', background="#e7f2fb")

        self.tree.bind("<ButtonRelease-1>", self.obtener_datos)

    def limpiar_campos(self):
        self.campo_id.config(state="normal")
        self.campo_id.delete(0, tk.END)
        self.campo_nombre.delete(0, tk.END)
        self.campo_precio.delete(0, tk.END)
        self.campo_id.config(state="readonly")

    def enviar_correo(self, destinatario):
        servicio_producto = ServicioProducto()

        remitente = "supermarketlobueno@gmail.com"
        contrasena = "ayrg sohu wypi okzc"

        # Crear el
        mensaje = MIMEMultipart("alternative")
        mensaje['From'] = remitente
        mensaje['To'] = destinatario
        mensaje['Subject'] = "Factura Registrada"

        productos = servicio_producto.obtener_productos()

        empresa_nombre = "Supermercado Lo Bueno"
        empresa_direccion = "Calle 50, Panama norte"
        empresa_telefono = "(507) 3456-7890"
        empresa_email = "info@supermercadolobueno.com"

        cliente_email = destinatario

        total = 0

        cuerpo = f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ text-align: center; }}
                .invoice {{ border: 1px solid #ccc; padding: 20px; margin-top: 20px; }}
                .table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
                .table th, .table td {{ border: 1px solid #ccc; padding: 8px; text-align: left; }}
                .total {{ font-weight: bold; }}
                .total-row {{ background-color: #f9f9f9; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>{empresa_nombre}</h1>
                <p>{empresa_direccion}<br>
                Tel: {empresa_telefono}<br>
                Email: {empresa_email}</p>
            </div>
            <div class="invoice">
                <h2>Factura</h2>
                <p>Email: {cliente_email}</p>
                <table class="table">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Nombre</th>
                            <th>Precio</th>
                        </tr>
                    </thead>
                    <tbody>
        """

        for producto in productos:
            cuerpo += f"<tr><td>{producto.id}</td><td>{producto.nombre}</td><td>${producto.precio:.2f}</td></tr>\n"
            total += producto.precio

        itbms = total * 0.07
        total_con_itbms = total + itbms

        cuerpo += f"""
                    </tbody>
                    <tfoot>
                        <tr class="total-row">
                            <td colspan="2" class="total">Total:</td>
                            <td class="total">${total:.2f}</td>
                        </tr>
                        <tr class="total-row">
                            <td colspan="2" class="total">ITBMS (7%):</td>
                            <td class="total">${itbms:.2f}</td>
                        </tr>
                        <tr class="total-row">
                            <td colspan="2" class="total">Total a pagar:</td>
                            <td class="total">${total_con_itbms:.2f}</td>
                        </tr>
                    </tfoot>
                </table>
                <p>Gracias por su compra!</p>
                <p>Nota: Las devoluciones se aceptan dentro de los 30 días con el recibo.</p>
            </div>
        </body>
        </html>
        """

        mensaje.attach(MIMEText(cuerpo, 'html'))

        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as servidor:
                servidor.starttls()
                servidor.login(remitente, contrasena)
                servidor.send_message(mensaje)
                messagebox.showinfo("Éxito", "Factura enviada por correo.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo enviar el correo: {e}")

    def imprimir_factura(self):
        destinatario = self.campo_correo.get()
        if destinatario:
            self.enviar_correo(destinatario)
        else:
            messagebox.showwarning("Advertencia", "Por favor ingrese un correo electrónico.")


    def obtener_datos(self, event):

        selected_item = self.tree.selection()
        if selected_item:

            item_data = self.tree.item(selected_item, 'values')

            self.campo_id.config(state="normal")
            self.campo_id.delete(0, tk.END)
            self.campo_id.insert(0, item_data[0])  # Id
            self.campo_nombre.delete(0, tk.END)
            self.campo_nombre.insert(0, item_data[1])  # Nombre
            self.campo_precio.delete(0, tk.END)
            self.campo_precio.insert(0, item_data[2])  # Precio
            self.campo_cedula.delete(0, tk.END)
            self.campo_cedula.insert(0, item_data[3])  # Cédula
            self.campo_correo.delete(0, tk.END)
            self.campo_correo.insert(0, item_data[4])  # Correo
            self.campo_id.config(state="readonly")

    def al_seleccionar_treeview(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            self.btn_eliminar.pack(**self.obtener_conf_btn_pack())
            self.btn_modificar.pack(**self.obtener_conf_btn_pack())
        else:
            self.btn_eliminar.pack_forget()
            self.btn_modificar.pack_forget()


    def ocultar_botones(self):
        self.btn_eliminar.pack_forget()
        self.btn_modificar.pack_forget()