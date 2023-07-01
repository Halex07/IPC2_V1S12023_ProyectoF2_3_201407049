from flask import Flask, render_template, request, redirect, Blueprint
import xml.etree.ElementTree as ET

app = Flask(__name__)
cartelera_bp = Blueprint('cartelera', __name__)

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
        self.boletos_comprados = []

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

    def agregar_boleto_comprado(self, boleto):
        self.boletos_comprados.append(boleto)

    def obtener_boletos_comprados(self):
        return self.boletos_comprados


class ListaCircular:
    def __init__(self):
        self.primer_pelicula = None

    def agregar_pelicula(self, pelicula):
        if self.primer_pelicula is None:
            pelicula.siguiente = pelicula
            self.primer_pelicula = pelicula
        else:
            actual = self.primer_pelicula
            while actual.siguiente != self.primer_pelicula:
                actual = actual.siguiente
            actual.siguiente = pelicula
            pelicula.siguiente = self.primer_pelicula

    def obtener_peliculas(self):
        peliculas = []
        actual = self.primer_pelicula
        while True:
            peliculas.append(actual)
            actual = actual.siguiente
            if actual == self.primer_pelicula:
                break
        return peliculas

    def marcar_como_favorita(self, nombre_pelicula):
        actual = self.primer_pelicula
        while True:
            if actual.titulo == nombre_pelicula:
                actual.favorita = True
                return True
            actual = actual.siguiente
            if actual == self.primer_pelicula:
                break
        return False

    def obtener_favoritas(self):
        peliculas = []
        actual = self.primer_pelicula
        while True:
            if actual.favorita:
                peliculas.append(actual)
            actual = actual.siguiente
            if actual == self.primer_pelicula:
                break
        return peliculas


cartelera = Cartelera()
favoritas = ListaCircular()


@cartelera_bp.route('/cartelera', methods=['GET'])
def mostrar_cartelera():
    peliculas = cartelera.obtener_peliculas()
    return render_template('cartelera.html', peliculas=peliculas)

@cartelera_bp.route('/carteleracl', methods=['GET'])
def mostrar_carteleracl():
    peliculas = cartelera.obtener_peliculas()
    return render_template('carteleraCliente.html', peliculas=peliculas)

@cartelera_bp.route('/favoritas', methods=['GET'])
def mostrar_favoritas():
    peliculas = favoritas.obtener_favoritas()
    return render_template('favoritas.html', peliculas=peliculas)


@cartelera_bp.route('/boletos_comprados', methods=['GET'])
def mostrar_boletos_comprados():
    boletos = cartelera.obtener_boletos_comprados()
    return render_template('boletos_comprados.html', boletos=boletos)


@cartelera_bp.route('/agregar', methods=['POST'])
def agregar_pelicula():
    cate = request.form['cat']
    titulo = request.form['titulo']
    director = request.form['director']
    anio = request.form['anio']
    fecha = request.form['fecha']
    hora = request.form['hora']
    nueva_pelicula = Pelicula(cate, titulo, director, anio, fecha, hora)
    cartelera.agregar_pelicula(nueva_pelicula)
    return redirect('/cartelera/carteleracl')


@cartelera_bp.route('/actualizar/<nombre_pelicula>', methods=['POST'])
def actualizar_pelicula(nombre_pelicula):
    datos_actualizados = {
        'cat': request.form['cat'],
        'titulo': request.form['titulo'],
        'director': request.form['director'],
        'anio': request.form['anio'],
        'fecha': request.form['fecha'],
        'hora': request.form['hora']
    }
    if cartelera.actualizar_pelicula(nombre_pelicula, datos_actualizados):
        return redirect('/cartelera/carteleracl')
    else:
        return "Pelicula no encontrada"


@cartelera_bp.route('/eliminar/<nombre_pelicula>', methods=['GET'])
def eliminar_pelicula(nombre_pelicula):
    if cartelera.eliminar_pelicula(nombre_pelicula):
        return redirect('/cartelera/carteleracl')
    else:
        return "Pelicula no encontrada"


@cartelera_bp.route('/comprar/<nombre_pelicula>', methods=['GET'])
def comprar_boletos(nombre_pelicula):
    actual = cartelera.primer_pelicula
    while actual:
        if actual.titulo == nombre_pelicula:
            # Agregar aquí la lógica para comprar boletos
            cartelera.agregar_boleto_comprado(actual)  # Agregar el boleto comprado a la lista
            break
        actual = actual.siguiente

    return redirect('/cartelera/carteleracl')


@cartelera_bp.route('/marcar_favorita/<nombre_pelicula>', methods=['GET'])
def marcar_favorita(nombre_pelicula):
    if favoritas.marcar_como_favorita(nombre_pelicula):
        return redirect('/cartelera/carteleracl')
    else:
        return "Pelicula no encontrada"


@cartelera_bp.route('/cargarxml', methods=['GET'])
def cargar_xml():
    
    tree = ET.parse('peliculas')
    root = tree.getroot()

    for pelicula in root.findall('pelicula'):
        cate = pelicula.find('categoria').text
        titulo = pelicula.find('titulo').text
        director = pelicula.find('director').text
        anio = pelicula.find('anio').text
        fecha = pelicula.find('fecha').text
        hora = pelicula.find('hora').text
        nueva_pelicula = Pelicula(cate, titulo, director, anio, fecha, hora)
        cartelera.agregar_pelicula(nueva_pelicula)

    return redirect('/cartelera/carteleracl')


app.register_blueprint(cartelera_bp, url_prefix='/cartelera')

if __name__ == "__main__":
    app.run()
