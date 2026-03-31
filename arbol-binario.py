from collections import deque

# 1. CLASE NODO
class Nodo:
    """
    Representa la unidad básica (nodo) de un árbol binario.

    Atributos:
        valor: El dato almacenado en el nodo.
        izq: Referencia al hijo izquierdo (menores).
        der: Referencia al hijo derecho (mayores).
    """

    def __init__(self, valor):
        """Inicializa un nuevo nodo con un valor dado."""
        self._valor = valor
        self._izq = None
        self._der = None

    @property
    def valor(self):
        """Obtiene el valor del nodo."""
        return self._valor

    @valor.setter
    def valor(self, v):
        """Establece un nuevo valor para el nodo."""
        self._valor = v

    @property
    def izq(self):
        """Obtiene el nodo hijo izquierdo."""
        return self._izq

    @izq.setter
    def izq(self, n):
        """Establece el nodo hijo izquierdo."""
        self._izq = n

    @property
    def der(self):
        """Obtiene el nodo hijo derecho."""
        return self._der

    @der.setter
    def der(self, n):
        """Establece el nodo hijo derecho."""
        self._der = n


# 2. CLASE ÁRBOL BINARIO DE BÚSQUEDA
class ArbolBinario:
    """
    Implementación de un Árbol Binario de Búsqueda (BST).
    Proporciona métodos para gestión de nodos, búsquedas y recorridos.
    """

    def __init__(self):
        """Inicializa un árbol binario vacío."""
        self.raiz = None

    def es_vacio(self):
        """
        Verifica si el árbol carece de nodos.
            bool: True si la raíz es None, False en caso contrario.
        """
        return self.raiz is None

    def insertar_nodo(self, x):
        """
        Inserta un nuevo valor en el árbol respetando la propiedad de orden.
            x: El valor a insertar.
        """
        if self.es_vacio():
            self.raiz = Nodo(x)
        else:
            self._insertar_recursivo(x, self.raiz)

    def _insertar_recursivo(self, valor, nodo):
        """Método auxiliar recursivo para encontrar la posición de inserción."""
        if valor < nodo.valor:
            if nodo.izq is None:
                nodo.izq = Nodo(valor)
            else:
                self._insertar_recursivo(valor, nodo.izq)
        elif valor > nodo.valor:
            if nodo.der is None:
                nodo.der = Nodo(valor)
            else:
                self._insertar_recursivo(valor, nodo.der)

    def buscar_x(self, x):
        """
        Busca un valor específico en el árbol.
            x: Valor a buscar.
            Nodo: El objeto Nodo si se encuentra, None si no existe.
        """
        def _buscar(nodo, v):
            if nodo is None or nodo.valor == v:
                return nodo
            return _buscar(nodo.izq if v < nodo.valor else nodo.der, v)
        return _buscar(self.raiz, x)

    def es_hoja(self, valor):
        """
        Determina si un nodo con un valor dado es un nodo hoja (sin hijos).
            valor: El valor del nodo a comprobar.
            bool: True si el nodo existe y no tiene hijos.
        """
        nodo = self.buscar_x(valor)
        if nodo:
            return nodo.izq is None and nodo.der is None
        return False

    def eliminar_nodo(self, x):
        """
        Elimina un nodo del árbol y lo reestructura para mantener el orden.
            x: Valor del nodo a eliminar.
        """
        self.raiz = self._eliminar_recursivo(self.raiz, x)

    def _eliminar_recursivo(self, nodo, x):
        """Maneja la lógica de eliminación según el número de hijos del nodo."""
        if nodo is None:
            return nodo

        if x < nodo.valor:
            nodo.izq = self._eliminar_recursivo(nodo.izq, x)
        elif x > nodo.valor:
            nodo.der = self._eliminar_recursivo(nodo.der, x)
        else:
            # Casos con 0 o 1 hijo
            if nodo.izq is None:
                return nodo.der
            if nodo.der is None:
                return nodo.izq

            # Caso con 2 hijos: Obtener sucesor in-orden
            sucesor = self._min_valor_nodo(nodo.der)
            nodo.valor = sucesor.valor
            nodo.der = self._eliminar_recursivo(nodo.der, sucesor.valor)
        return nodo

    def _min_valor_nodo(self, nodo):
        """Busca el nodo con el valor mínimo a partir de un punto dado."""
        actual = nodo
        while actual.izq is not None:
            actual = actual.izq
        return actual

    def in_orden(self):
        """
        Realiza un recorrido In-Orden (Izquierda, Raíz, Derecha).
            list: Lista con los valores del árbol ordenados ascendentemente.
        """
        res = []
        def _rec(n):
            if n:
                _rec(n.izq); res.append(n.valor); _rec(n.der)
        _rec(self.raiz)
        return res

    def pre_orden(self):
        """
        Realiza un recorrido Pre-Orden (Raíz, Izquierda, Derecha).
            list: Lista con los valores en el orden visitado.
        """
        res = []
        def _rec(n):
            if n:
                res.append(n.valor); _rec(n.izq); _rec(n.der)
        _rec(self.raiz)
        return res

    def post_orden(self):
        """
        Realiza un recorrido Post-Orden (Izquierda, Derecha, Raíz).
            list: Lista con los valores en el orden visitado.
        """
        res = []
        def _rec(n):
            if n:
                _rec(n.izq); _rec(n.der); res.append(n.valor)
        _rec(self.raiz)
        return res

    def mostrar_vertical(self):
        """Muestra una representación visual del árbol en la consola."""
        if self.es_vacio():
            print("Árbol vacío.")
            return

        def get_h(n): return 1 + max(get_h(n.izq), get_h(n.der)) if n else -1
        h = get_h(self.raiz)
        ancho = pow(2, h + 1) * 4
        matriz = [[" " for _ in range(ancho)] for _ in range((h + 1) * 2)]

        def dib(n, f, c, g):
            if n:
                v = str(n.valor)
                s = c - len(v) // 2
                matriz[f][s : s + len(v)] = list(v)
                if n.izq:
                    matriz[f+1][c-g//2] = "/"; dib(n.izq, f+2, c-g, g//2)
                if n.der:
                    matriz[f+1][c+g//2] = "\\"; dib(n.der, f+2, c+g, g//2)

        dib(self.raiz, 0, ancho // 2, ancho // 4)
        for f in matriz:
            linea = "".join(f).rstrip()
            if linea: print(linea)


# PRUEBAS DE FUNCIONAMIENTO
if __name__ == "__main__":
    arbol = ArbolBinario()
    for dato in [100, 50, 150, 25, 75, 125, 175]:
        arbol.insertar_nodo(dato)

    print("ESTADO INICIAL:")
    arbol.mostrar_vertical()

    print("\n--- PRUEBAS DE MÉTODOS ---")
    print(f"¿Está vacío?: {arbol.es_vacio()}")
    print(f"Búsqueda de 125: {'Encontrado' if arbol.buscar_x(125) else 'No existe'}")
    print(f"¿El 25 es hoja?: {arbol.es_hoja(25)}")
    print(f"InOrden:   {arbol.in_orden()}")
    print(f"PreOrden:  {arbol.pre_orden()}")
    print(f"PostOrden: {arbol.post_orden()}")

    print("\n--- ELIMINANDO EL 50 (Nodo con hijos) ---")
    arbol.eliminar_nodo(50)
    arbol.mostrar_vertical()
    print(f"InOrden final (debe seguir ordenado): {arbol.in_orden()}")