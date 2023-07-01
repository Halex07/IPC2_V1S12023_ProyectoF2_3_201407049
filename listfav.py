class lNodo:
    def __init__(self, boleto):
        self.boleto = boleto
        self.siguiente = None
class Favorito:
    def __init__(self, categoria, titulo, numero_boleto):
        self.categoria = categoria
        self.titulo = titulo
        self.numero_boleto = numero_boleto

class ListaFavorito:
    def __init__(self):
        self.primer_boleto = None

    def agregar_favorito(self, boleto):
        nuevo_nodo = lNodo(boleto)
        if self.primer_boleto is None:
            self.primer_boleto = nuevo_nodo
        else:
            actual = self.primer_boleto
            while actual.siguiente is not None:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo
    
    def append(self, boleto):
        nuevo_nodo = lNodo(boleto)
        if self.primer_boleto is None:
            self.primer_boleto = nuevo_nodo
        else:
            actual = self.primer_boleto
            while actual.siguiente is not None:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo

    def obtener_favoritas(self):
        favorita= []
        actual = self.primer_boleto
        while actual is not None:
            favorita.append(actual.boleto)
            actual = actual.siguiente
        return favorita


lista_favoritos = ListaFavorito()