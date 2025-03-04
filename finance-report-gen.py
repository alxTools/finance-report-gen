#!/usr/bin/env python3

import pandas as pd
import tkinter as tk
from tkinter import filedialog
import os


def generate_report(file_path):
    # Cargar el CSV con manejo de líneas mal formateadas (tomando solo los primeros 18 campos)
    df = pd.read_csv(file_path, engine='python', on_bad_lines=lambda x: x[:18])

    # Convertir la columna 'Date' a formato datetime (suponiendo formato mes/día/año)
    df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y')

    # Asegurarse de que las columnas 'Gross' y 'Net' sean numéricas
    df['Gross'] = pd.to_numeric(df['Gross'], errors='coerce')
    df['Net'] = pd.to_numeric(df['Net'], errors='coerce')

    # Resumen general
    total_transacciones = len(df)
    fecha_inicio = df['Date'].min().date()
    fecha_fin = df['Date'].max().date()

    # Transacciones por tipo (Description)
    transacciones_por_tipo = df.groupby('Description').size().reset_index(name='Cantidad')

    # Agrupación mensual del monto neto
    df['Mes'] = df['Date'].dt.to_period('M')
    neto_por_mes = df.groupby('Mes')['Net'].sum().reset_index()
    neto_por_mes['Mes'] = neto_por_mes['Mes'].astype(str)  # Convertir Period a string

    # Ingresos (transacciones donde Gross > 0)
    df_ingresos = df[df['Gross'] > 0]
    ingresos_por_company = df_ingresos.groupby('Name')['Gross'].sum().reset_index().sort_values(by='Gross',
                                                                                                ascending=False)

    # Gastos (transacciones donde Gross < 0)
    df_gastos = df[df['Gross'] < 0]
    gastos_por_company = df_gastos.groupby('Name')['Gross'].sum().reset_index().sort_values(by='Gross', ascending=True)

    # Generar contenido Markdown
    markdown = []
    markdown.append(f"# Reporte del Statement: {fecha_inicio} - {fecha_fin}\n")
    markdown.append(f"**Total de transacciones:** {total_transacciones}\n")

    markdown.append("## Transacciones por Tipo (Description)\n")
    markdown.append(transacciones_por_tipo.to_markdown(index=False))
    markdown.append("\n")

    markdown.append("## Monto Neto por Mes\n")
    markdown.append(neto_por_mes.to_markdown(index=False))
    markdown.append("\n")

    markdown.append("## Ingresos Totales por Compañía\n")
    markdown.append(ingresos_por_company.to_markdown(index=False))
    markdown.append("\n")

    markdown.append("## Gastos Totales por Compañía\n")
    markdown.append(gastos_por_company.to_markdown(index=False))
    markdown.append("\n")

    return "\n".join(markdown)


def main():
    # Crear ventana oculta para seleccionar el archivo
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Selecciona el archivo CSV",
        filetypes=[("Archivos CSV", "*.CSV"), ("Archivos CSV", "*.csv")]
    )

    if not file_path:
        print("No se seleccionó ningún archivo.")
        return

    print(f"Procesando el archivo: {file_path}")
    markdown_report = generate_report(file_path)

    # Guardar el reporte en Markdown en la misma carpeta del archivo, con el mismo nombre base y sufijo '_reporte.md'
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    md_file = os.path.join(os.path.dirname(file_path), f"{base_name}_reporte.md")
    with open(md_file, "w", encoding="utf-8") as f:
        f.write(markdown_report)

    print(f"Reporte generado exitosamente: {md_file}")


if __name__ == "__main__":
    main()
