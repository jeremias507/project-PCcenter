import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from tkinter import messagebox
from aplicacion.servicio_producto import ServicioProducto
from form.registro_form_desing import FormularioRegistroDesign


class FormularioRegistro(FormularioRegistroDesign):
    def __init__(self):
        self.servicio_producto = ServicioProducto()
        super().__init__()

    # Función para imprimir factura y eliminar productos
    def imprimir_factura(self):
        # Obtener el correo del campo de entrada
        correo = self.campo_correo.get()

        if not correo:
            messagebox.showerror("Error", "Por favor ingrese un correo válido.")
            return

        # Obtener productos de la lista
        productos = self.servicio_producto.obtener_productos()
        if not productos:
            messagebox.showerror("Error", "No hay productos registrados para enviar.")
            return

        # Crear cuerpo del mensaje con los productos
        mensaje = "Lista de productos registrados:\n\n"
        for producto in productos:
            mensaje += f"ID: {producto.id}, Nombre: {producto.nombre}, Precio: {producto.precio}\n"

        # Guardar la factura en un archivo de texto
        if self.crear_archivo_factura(mensaje):
            # Si se guarda exitosamente, se envía el correo
            if self.enviar_correo(correo, mensaje):
                # Si el correo fue enviado exitosamente, eliminamos todos los productos
                self.servicio_producto.eliminar_todos()
                self.actualizar_lista()
                messagebox.showinfo("Éxito", "Factura enviada y productos eliminados.")
            else:
                messagebox.showerror("Error", "No se pudo enviar el correo. Intente de nuevo.")
        else:
            messagebox.showerror("Error", "No se pudo crear el archivo de factura.")

    # Función para enviar correo
    def enviar_correo(self, destinatario, mensaje):
        try:
            # Configuración del servidor SMTP (esto es para Gmail, puedes modificarlo para otro servidor)
            remitente = "supermarketlobueno@gmail.com"  # Cambia esto por tu correo
            password = "ayrg sohu wypi okzc"# Cambia esto por tu contraseña de aplicación o cuenta
            servidor = smtplib.SMTP('smtp.gmail.com', 587)
            servidor.starttls()
            servidor.login(remitente, password)

            # Crear el mensaje de correo
            email = MIMEMultipart()
            email['From'] = remitente
            email['To'] = destinatario
            email['Subject'] = "Factura de productos"
            email.attach(MIMEText(mensaje, 'plain'))

            # Enviar el correo
            servidor.send_message(email)
            servidor.quit()
            return True
        except Exception as e:
            print(f"Error al enviar correo: {e}")
            return False

    # Función para crear un archivo de texto con la factura
    def crear_archivo_factura(self, contenido):
        try:
            with open('factura_productos.txt', 'w') as archivo:
                archivo.write(contenido)
            return True
        except Exception as e:
            print(f"Error al crear archivo de factura: {e}")
            return False
