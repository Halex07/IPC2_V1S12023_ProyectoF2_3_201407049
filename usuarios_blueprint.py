from flask import Flask, render_template, request, Blueprint, redirect, url_for
from xml.etree import ElementTree as etree
from lxml import etree


app = Flask(__name__)

# Clase para representar un usuario
class Usuario:
    def __init__(self, rol, nombre, apellido, telefono, correo, contrasena):
        self.rol = rol
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
        self.correo = correo
        self.contrasena = contrasena

# Clase para representar una lista enlazada de usuarios
class ListaUsuarios:
    def __init__(self):
        self.head = None

    def agregar_usuario(self, usuario):
        if not self.head:
            self.head = usuario
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = usuario

# Crear un objeto Blueprint
usuarios_blueprint = Blueprint('usuarios', __name__)

@usuarios_blueprint.route('/gestionar_usuarios')
def gestionar_usuarios():
    return render_template('gestionar_usarios.html')


@usuarios_blueprint.route('/modificar_usuario')
def modificar_usuario():
    return 'hola' 

@usuarios_blueprint.route('/ver_lista_usuarios')
def ver_lista_usuarios():
    return render_template('ver_lista_usuarios.html')

@usuarios_blueprint.route('/eliminar_usuario')
def eliminar_usuario():
    return render_template('eliminar_usuario.html')

# Ruta para agregar un usuario
@usuarios_blueprint.route('/agregar_usuario', methods=['GET', 'POST'])
def agregar_usuario():
    if request.method == 'POST':
        xml_file = etree.parse('usuarios.xml')
        root = xml_file.getroot()

        # Obtener los datos del formulario
        rol = request.form['rol']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        telefono = request.form['telefono']
        correo = request.form['correo']
        contrasena = request.form['contrasena']

        # Crear un objeto Usuario con los datos del formulario
        nuevo_usuario = Usuario(rol, nombre, apellido, telefono, correo, contrasena)

        # Agregar el usuario a la lista enlazada
        lista_usuarios.agregar_usuario(nuevo_usuario)

        # Agregar el usuario al archivo XML
        usuario_element = etree.SubElement(root, 'usuario')
        rol_element = etree.SubElement(usuario_element, 'rol')
        rol_element.text = rol
        nombre_element = etree.SubElement(usuario_element, 'nombre')
        nombre_element.text = nombre
        apellido_element = etree.SubElement(usuario_element, 'apellido')
        apellido_element.text = apellido
        telefono_element = etree.SubElement(usuario_element, 'telefono')
        telefono_element.text = telefono
        correo_element = etree.SubElement(usuario_element, 'correo')
        correo_element.text = correo
        contrasena_element = etree.SubElement(usuario_element, 'contrasena')
        contrasena_element.text = contrasena

        # Guardar los cambios en el archivo XML
        xml_file.write('usuarios.xml', encoding='utf-8')

        #return redirect(url_for('usuarios.exito_registro'))

    return render_template('agregar_usuario.html')

# Registrar el blueprint en la aplicación
app.register_blueprint(usuarios_blueprint)

# Ruta de inicio
@app.route('/')
def index():
    return render_template('login.html')

# Crear una instancia de la lista de usuarios
lista_usuarios = ListaUsuarios()

if __name__ == '__main__':
    app.run(debug=True)