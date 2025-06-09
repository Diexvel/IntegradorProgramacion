import time
import random
import copy 


# Diccionario para almacenar categorías y nombres de ejemplo para generar datos
DATOS_PRODUCTOS_EJEMPLO = {
    "Electrónica": ["Televisor", "Auriculares", "Smartphone", "Tablet", "Cámara"],
    "Ferretería": ["Martillo", "Destornillador", "Llave", "Sierra", "Cinta Métrica"],
    "Hogar": ["Licuadora", "Cafetera", "Aspiradora", "Sábanas", "Olla"]
}

def generar_inventario_aleatorio(cantidad):
    """Genera una lista de productos aleatorios para pruebas de rendimiento."""
    productos_generados = []
    
    categorias = list(DATOS_PRODUCTOS_EJEMPLO.keys())

    for i in range(cantidad):
        id_prod = f"PROD{i:05d}"
        categoria_prod = random.choice(categorias)
        nombre_prod = random.choice(DATOS_PRODUCTOS_EJEMPLO[categoria_prod]) + f"_{i}" 
        precio_prod = round(random.uniform(1.0, 500.0), 2)
        
        productos_generados.append({
            "id_producto": id_prod,
            "nombre": nombre_prod,
            "categoria": categoria_prod,
            "precio": precio_prod
        })
    return productos_generados

# --- Funciones de Búsqueda ---

def busqueda_lineal_por_id(lista, id_buscar):
    """
    Realiza una búsqueda lineal en una lista de diccionarios por 'id_producto'.
    Retorna el producto si lo encuentra, de lo contrario None.
    """
    for producto in lista:
        if producto.get('id_producto') == id_buscar:
            return producto
    return None

def busqueda_binaria_por_id(lista_ordenada, id_buscar):
    """
    Realiza una búsqueda binaria en una lista de diccionarios por 'id_producto'.
    Requiere que la lista esté ORDENADA por 'id_producto'.
    Retorna el producto si lo encuentra, de lo contrario None.
    """
    izquierda, derecha = 0, len(lista_ordenada) - 1
    
    while izquierda <= derecha:
        medio = (izquierda + derecha) // 2
        producto_medio = lista_ordenada[medio]
        
        id_medio = producto_medio.get('id_producto')
        
        if id_medio == id_buscar:
            return producto_medio
        elif id_medio < id_buscar:
            izquierda = medio + 1
        else: 
            derecha = medio - 1
    return None 

# --- Algoritmos de Ordenamiento ---

def bubble_sort(lista, clave='precio', reverse=False):
    """Implementación de Bubble Sort."""
    n = len(lista)
    for i in range(n - 1):
        for j in range(0, n - i - 1):
            val1 = lista[j].get(clave)
            val2 = lista[j+1].get(clave)

            if reverse: # Orden descendente
                if val1 < val2:
                    lista[j], lista[j+1] = lista[j+1], lista[j]
            else: # Orden ascendente
                if val1 > val2:
                    lista[j], lista[j+1] = lista[j+1], lista[j]
    return lista 

def insertion_sort(lista, clave='precio', reverse=False):
    """Implementación de Insertion Sort."""
    
    for i in range(1, len(lista)):
        actual = lista[i]
        j = i - 1
        
        while j >= 0:
            if reverse: # Orden descendente
                if actual.get(clave) > lista[j].get(clave):
                    lista[j+1] = lista[j]
                    j -= 1
                else:
                    break
            else: # Orden ascendente
                if actual.get(clave) < lista[j].get(clave):
                    lista[j+1] = lista[j]
                    j -= 1
                else:
                    break
        lista[j+1] = actual
    return lista 

def merge_sort(lista, clave='precio', reverse=False):
    """Implementación de Merge Sort."""
    
    if len(lista) <= 1:
        return lista

    medio = len(lista) // 2
    izquierda = lista[:medio]
    derecha = lista[medio:]

    # Llamadas recursivas
    izquierda = merge_sort(izquierda, clave, reverse)
    derecha = merge_sort(derecha, clave, reverse)

    return _merge(izquierda, derecha, clave, reverse)

def _merge(izquierda, derecha, clave, reverse):
    """Función auxiliar para Merge Sort que combina dos listas ordenadas."""
    resultado = []
    i = j = 0

    while i < len(izquierda) and j < len(derecha):
        val_izq = izquierda[i].get(clave)
        val_der = derecha[j].get(clave)

        if reverse: # Descendente
            if val_izq >= val_der:
                resultado.append(izquierda[i])
                i += 1
            else:
                resultado.append(derecha[j])
                j += 1
        else: # Ascendente
            if val_izq <= val_der:
                resultado.append(izquierda[i])
                i += 1
            else:
                resultado.append(derecha[j])
                j += 1

    resultado.extend(izquierda[i:])
    resultado.extend(derecha[j:])
    return resultado

# ---  Demostración y Comparación de Tiempos ---

def ejecutar_pruebas():
    print("--- Demostración de Algoritmos ---")
    
    # Tamaños de inventario para las pruebas
    tamano_inventario_pequeno = 100
    tamano_inventario_mediano = 4500
    tamano_inventario_grande = 15000 

    # Generamos los inventarios una sola vez
    print(f"\nPreparando inventario de {tamano_inventario_pequeno} productos...")
    inventario_base_pequeno = generar_inventario_aleatorio(tamano_inventario_pequeno)
    
    print(f"Preparando inventario de {tamano_inventario_mediano} productos...")
    inventario_base_mediano = generar_inventario_aleatorio(tamano_inventario_mediano)

    print(f"Preparando inventario de {tamano_inventario_grande} productos...")
    inventario_base_grande = generar_inventario_aleatorio(tamano_inventario_grande)

    # --- PRUEBAS DE ORDENAMIENTO por PRECIO (Ascendente) ---
    print("\n\n===== Pruebas de ORDENAMIENTO por PRECIO (Ascendente) =====")
    
    ordenamientos = {
        "Bubble Sort": bubble_sort,
        "Insertion Sort": insertion_sort,
        "Merge Sort": merge_sort,
        "Python Timsort (built-in)": lambda lst, clave='precio', reverse=False: sorted(lst, key=lambda x: x.get(clave), reverse=reverse)
    }

    inventarios_a_probar = {
        "Inventario Pequeño (100)": inventario_base_pequeno,
        "Inventario Mediano (4500)": inventario_base_mediano,
        "Inventario Grande (15000)": inventario_base_grande
    }

    for tamano_desc, inv_original in inventarios_a_probar.items():
        print(f"\n--- Probando con {tamano_desc} ---")
        for nombre_algo, algo_func in ordenamientos.items():
            
            # Cada algoritmo recibe una COPIA PROFUNDA NUEVA del inventario original no ordenado.
            inventario_para_prueba = copy.deepcopy(inv_original) 
            
            start_time = time.time()
            _ = algo_func(inventario_para_prueba, clave='precio', reverse=False)
            end_time = time.time()
            print(f"  {nombre_algo}: {end_time - start_time:.6f} segundos")

    # --- PRUEBAS DE BÚSQUEDA por ID de Producto ---
    print("\n\n===== Pruebas de BÚSQUEDA por ID de Producto =====")

    # Usaremos el inventario grande para las pruebas de búsqueda, para que las diferencias sean más evidentes
    inventario_busqueda = inventario_base_grande 
    
    # Necesitamos una lista ordenada por ID para la búsqueda binaria.
    # Usamos Timsort  para preparar esta lista de manera eficiente.
    # Es importante que esta lista sea una copia de los datos originales
    inventario_ordenado_por_id = sorted(copy.deepcopy(inventario_busqueda), key=lambda x: x['id_producto'])
    
    
    id_existente = inventario_busqueda[len(inventario_busqueda) // 2]['id_producto'] if inventario_busqueda else "PROD00001" 
    id_no_existente = "NO_EXISTE_12345" # Un ID que no está en la lista

    print("\n--- Búsqueda Lineal por ID ---")
    start_time = time.time()
    resultado_lineal_existente = busqueda_lineal_por_id(inventario_busqueda, id_existente)
    end_time = time.time()
    print(f"  Búsqueda Lineal por ID '{id_existente}' (existente): {end_time - start_time:.9f} segundos. Encontrado: {'Sí' if resultado_lineal_existente else 'No'}")

    start_time = time.time()
    resultado_lineal_no_existente = busqueda_lineal_por_id(inventario_busqueda, id_no_existente)
    end_time = time.time()
    print(f"  Búsqueda Lineal por ID '{id_no_existente}' (no existente): {end_time - start_time:.9f} segundos. Encontrado: {'Sí' if resultado_lineal_no_existente else 'No'}")

    print("\n--- Búsqueda Binaria por ID (en lista ordenada) ---")
    start_time = time.time()
    resultado_binaria_existente = busqueda_binaria_por_id(inventario_ordenado_por_id, id_existente)
    end_time = time.time()
    print(f"  Búsqueda Binaria por ID '{id_existente}' (existente): {end_time - start_time:.9f} segundos. Encontrado: {'Sí' if resultado_binaria_existente else 'No'}")

    start_time = time.time()
    resultado_binaria_no_existente = busqueda_binaria_por_id(inventario_ordenado_por_id, id_no_existente)
    end_time = time.time()
    print(f"  Búsqueda Binaria por ID '{id_no_existente}' (no existente): {end_time - start_time:.9f} segundos. Encontrado: {'Sí' if resultado_binaria_no_existente else 'No'}")

    print("\n--- Fin de las pruebas ---")

# --- Ejecución Principal ---
if __name__ == "__main__":
    ejecutar_pruebas()