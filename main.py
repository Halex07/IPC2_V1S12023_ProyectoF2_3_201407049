from flask import Flask, request, render_template, session, redirect, url_for
import xml.etree.ElementTree as ET
from usuarios_blueprint import usuarios_blueprint

app = Flask(__name__)

# Registrar el blueprint en la aplicación
app.register_blueprint(usuarios_blueprint)

class Nodo:
    def __init__(self, dato=None):
        self.dato = dato
        self.siguiente = None


class ListaEnlazada:
    def __init__(self):
        self.cabeza = None

    def esta_vacia(self):
        return self.cabeza is None

    def agregar(self, dato):
        nuevo_nodo = Nodo(dato)
        if self.esta_vacia():
            self.cabeza = nuevo_nodo
        else:
            nodo_actual = self.cabeza
            while nodo_actual.siguiente is not None:
                nodo_actual = nodo_actual.siguiente
            nodo_actual.siguiente = nuevo_nodo

    def remover(self, dato):
        if self.cabeza is None:
            return
        if self.cabeza.dato == dato:
            self.cabeza = self.cabeza.siguiente
            return
        nodo_actual = self.cabeza
        while nodo_actual.siguiente is not None:
            if nodo_actual.siguiente.dato == dato:
                nodo_actual.siguiente = nodo_actual.siguiente.siguiente
                return
            nodo_actual = nodo_actual.siguiente

    def buscar(self, dato):
        nodo_actual = self.cabeza
        while nodo_actual is not None:
            if nodo_actual.dato == dato:
                return True
            nodo_actual = nodo_actual.siguiente
        return False


def cargar_usuarios():
    tree = ET.parse('usuarios.xml')  # Ruta al archivo XML
    root = tree.getroot()
    usuarios = ListaEnlazada()
    for usuario in root.findall('usuario'):
        usuario_info = {}
        for elemento in usuario:
            usuario_info[elemento.tag] = elemento.text
        usuarios.agregar(usuario_info)
    return usuarios


app = Flask(__name__)
app.secret_key = "tu_clave_secreta"  # Esta clave se utiliza para firmar las cookies de sesión


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['correo']
        contrasena = request.form['contrasena']
        usuarios = cargar_usuarios()
        nodo_actual = usuarios.cabeza
        while nodo_actual is not None:
            usuario = nodo_actual.dato
            if usuario['correo'] == correo and usuario['contrasena'] == contrasena:
                session['rol'] = usuario['rol']
                return redirect(url_for('menu'))
            nodo_actual = nodo_actual.siguiente
        return 'Credenciales inválidas'
    return render_template('login.html')


@app.route('/menu')
def menu():
    if 'rol' in session:
        if session['rol'] == 'administrador':
            return render_template('menu.html')
        elif session['rol'] == 'cliente':
            return render_template('menu.html')
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop('rol', None)
    return redirect(url_for('login'))


# Define las otras rutas y funciones asociadas para gestionar películas, salas, boletos, etc.

if __name__ == '__main__':
    app.run(debug=True)
