from flask import Flask, render_template, request, redirect, Blueprint
import xml.etree.ElementTree as ET
from tkinter import filedialog
import tkinter as tk
from werkzeug.utils import secure_filename
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired

app = Flask(__name__)
cartelera_bp = Blueprint('cartelera', __name__)

root = tk.Tk()
root.withdraw()

class Pelicula:
    def __init__(self, cate, titulo, director, anio, fecha, hora):
        self.cate = cate
        self.titulo = titulo
        self.director = director
        self.anio = anio
        self.fecha = fecha
        self.hora = hora
        self.siguiente = None

class Cartelera:
    def __init__(self):
        self.primer_pelicula = None

    def agregar_pelicula(self, pelicula):
        if self.primer_pelicula is None:
            self.primer_pelicula = pelicula
        else:
            actual = self.primer_pelicula
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = pelicula

    def obtener_peliculas(self):
        peliculas = []
        actual = self.primer_pelicula
        while actual:
            peliculas.append(actual)
            actual = actual.siguiente
        return peliculas

    def actualizar_pelicula(self, nombre_pelicula, datos_actualizados):
        actual = self.primer_pelicula
        while actual:
            if actual.titulo == nombre_pelicula:
                actual.cate = datos_actualizados.get('cat', actual.cate)
                actual.titulo = datos_actualizados.get('titulo', actual.titulo)
                actual.director = datos_actualizados.get('director', actual.director)
                actual.anio = datos_actualizados.get('anio', actual.anio)
                actual.fecha = datos_actualizados.get('fecha', actual.fecha)
                actual.hora = datos_actualizados.get('hora', actual.hora)
                return True
            actual = actual.siguiente
        return False


    def eliminar_pelicula(self, nombre_pelicula):
        if self.primer_pelicula.titulo == nombre_pelicula:
            self.primer_pelicula = self.primer_pelicula.siguiente
            return True
        actual = self.primer_pelicula
        while actual.siguiente:
            if actual.siguiente.titulo == nombre_pelicula:
                actual.siguiente = actual.siguiente.siguiente
                return True
            actual = actual.siguiente
        return False


cartelera = Cartelera()



root = ET.parse('peliculas.xml')

# Recorrer el XML y agregar las películas a la cartelera
for categoria in root.findall('categoria'):
    cate = categoria.find('nombre').text
    peliculas = categoria.find('peliculas')
    for pelicula in peliculas.findall('pelicula'):
        titulo = pelicula.find('titulo').text
        director = pelicula.find('director').text
        anio = pelicula.find('anio').text
        fecha = pelicula.find('fecha').text
        hora = pelicula.find('hora').text

        nueva_pelicula = Pelicula(cate, titulo, director, anio, fecha, hora)
        cartelera.agregar_pelicula(nueva_pelicula)
    

@cartelera_bp.route('/index', methods=['GET'])
def index():
    return render_template('index.html')

# Ruta para mostrar la cartelera
@cartelera_bp.route('/cartelera', methods=['GET'])
def mostrar_cartelera():
    peliculas = cartelera.obtener_peliculas()
    return render_template('cartelera.html', peliculas=peliculas)


@cartelera_bp.route('/agregar_pelicula', methods=['GET', 'POST'])
def agregar_pelicula():
    if request.method == 'POST':
        cate = request.form.get('cate')
        titulo = request.form.get('titulo')
        director = request.form.get('director')
        anio = request.form.get('anio')
        fecha = request.form.get('fecha')
        hora = request.form.get('hora')
        nueva_pelicula = Pelicula(cate, titulo, director, anio, fecha, hora)
        cartelera.agregar_pelicula(nueva_pelicula)

        return redirect('/cartelera/cartelera')

    return render_template('agregar_pelicula.html')


# Ruta para editar una película
# Ruta para editar una película
@cartelera_bp.route('/editar/<nombre_pelicula>', methods=['GET', 'POST'])
def editar_pelicula(nombre_pelicula):
    if request.method == 'POST':
        datos_actualizados = {
            'cat': request.form.get('cate'),
            'titulo': request.form.get('titulo'),
            'director': request.form.get('director'),
            'anio': request.form.get('anio'),
            'fecha': request.form.get('fecha'),
            'hora': request.form.get('hora')
        }
        cartelera.actualizar_pelicula(nombre_pelicula, datos_actualizados)
        return redirect('/cartelera/cartelera')

    pelicula = None
    actual = cartelera.primer_pelicula
    while actual:
        if actual.titulo == nombre_pelicula:
            pelicula = actual
            break
        actual = actual.siguiente

    if pelicula is None:
      
        return "Película no encontrada"

    return render_template('editar_pelicula.html', pelicula=pelicula)


# Ruta para eliminar una película
@cartelera_bp.route('/eliminar/<nombre_pelicula>', methods=['GET'])
def eliminar_pelicula(nombre_pelicula):
    eliminada = cartelera.eliminar_pelicula(nombre_pelicula)
    if eliminada:
        return redirect('/cartelera/cartelera')
    else:
        
        return "Película no encontrada"



app.register_blueprint(cartelera_bp)

#if __name__ == '__main__':
    #app.run()
