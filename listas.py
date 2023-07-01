class Nodo:
    def __init__(self, boleto):
        self.boleto = boleto
        self.siguiente = None
class Boleto:
    def __init__(self, categoria, titulo, numero_boleto):
        self.categoria = categoria
        self.titulo = titulo
        self.numero_boleto = numero_boleto

class ListaBoletos:
    def __init__(self):
        self.primer_boleto = None

    def agregar_boleto(self, boleto):
        nuevo_nodo = Nodo(boleto)
        if self.primer_boleto is None:
            self.primer_boleto = nuevo_nodo
        else:
            actual = self.primer_boleto
            while actual.siguiente is not None:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo
    
    def append(self, boleto):
        nuevo_nodo = Nodo(boleto)
        if self.primer_boleto is None:
            self.primer_boleto = nuevo_nodo
        else:
            actual = self.primer_boleto
            while actual.siguiente is not None:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo

    def obtener_comprasb(self):
        compras = []
        actual = self.primer_boleto
        while actual is not None:
            compras.append(actual.boleto)
            actual = actual.siguiente
        return compras


lista_boletos = ListaBoletos()