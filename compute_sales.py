"""
Calculador de ventas
por Mateo Cruz L A01793882

Este programa calcula el costo total de ventas
generado a partir de un archivo .json
"""

import json
import sys
import os
import time


class Producto:
    """
    Clase que representa un producto en el catálogo.
    """

    def __init__(self, titulo, precio):
        self.titulo = titulo
        self.precio = precio

    def obtener_precio(self):
        """
        Devuelve el precio del producto.
        """
        return self.precio

    def calcular_total(self, cantidad):
        """
        Calcula el total a pagar por una cierta cantidad del producto.
        """
        return cantidad * self.precio


def leer_catalogo(ruta_catalogo):
    """
    Lee el catálogo desde un archivo JSON.
    """
    try:
        with open(ruta_catalogo, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        print(f"No se pudo encontrar el archivo: {ruta_catalogo}")
        sys.exit(1)
    except json.JSONDecodeError:
        print("Error al decodificar el archivo JSON")
        sys.exit(1)
    except UnicodeDecodeError:
        print("El archivo debe estar codificado en UTF-8")
        sys.exit(1)


def calcular_ventas(ruta_ventas, catalogo):
    """
    Calcula los cobros de acuerdo a los datos de ventas y el catálogo.
    """
    cobros = {}
    ventas = leer_catalogo(ruta_ventas)

    for venta in ventas:
        producto = venta["Product"]
        cantidad = venta["Quantity"]
        precio = next(
            (item["price"] for item in catalogo if item["title"] == producto),
            None)

        if precio is None:
            print(f"Producto '{producto}' no encontrado en el catálogo.")
        else:
            if producto in cobros:
                cobros[producto]["cantidad"] += cantidad
                cobros[producto]["total"] += cantidad * precio
            else:
                cobros[producto] = {
                    "precio": precio,
                    "cantidad": cantidad,
                    "total": cantidad * precio,
                }

    return cobros


def imprimir_cobros(cobros):
    """
    Imprime los cobros en un formato legible.
    """
    total_general = sum(cobro["total"] for cobro in cobros.values())
    for producto, detalles in cobros.items():
        cantidad = detalles["cantidad"]
        precio = detalles["precio"]
        total = detalles["total"]
        print(f"{producto}: {cantidad} x ${precio} = ${total}")
    print("=" * 50)
    print(f"Total: ${total_general:.2f}")


def main():
    """
    Función principal del programa.
    """
    if len(sys.argv) != 3:
        print("Usage: python computeSales.py ProductList.json Sales.json")
        sys.exit(1)

    product_list_path = sys.argv[1]
    sales_data_path = sys.argv[2]

    start_time = time.time()

    catalogo = leer_catalogo(product_list_path)
    cobros = calcular_ventas(sales_data_path, catalogo)
    imprimir_cobros(cobros)

    end_time = time.time()
    elapsed_time = end_time - start_time

    # Writing the elapsed time to the console
    print(f"\nTiempo para la ejecución del cálculo: {elapsed_time:.5f} seg")

    # Generating the filename based on the current timestamp
    sales_filename = os.path.basename(sales_data_path)
    results_filename = os.path.splitext(sales_filename)[0] + "_results.txt"

    # Writing the elapsed time and results to a separate file
    with open(results_filename, "w", encoding="UTF-8") as results_file:
        results_file.write("Results:\n")
        results_lines = [
            f"{producto}: {cobro['cantidad']} x ${cobro['precio']} = ${cobro['total']}"
            for producto, cobro in cobros.items()
        ]
        results_file.write("\n".join(results_lines))
        results_file.write(f'\n{"-" * 50}\n')
        results_file.write(
            f"Total: ${sum(cobro['total'] for cobro in cobros.values())}\n"
        )
        results_file.write(
            f"\nTiempo para ejecución del cálculo: {elapsed_time:.5f} seg\n"
        )

    print(f"Resultados generados para {results_filename}")


if __name__ == "__main__":
    main()
