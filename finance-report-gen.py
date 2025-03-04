#!/usr/bin/env python3

import pandas as pd
import tkinter as tk
from tkinter import filedialog
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def generate_report(file_path):
    try:
        # Load CSV with handling of malformed lines (taking only the first 18 fields)
        df = pd.read_csv(file_path, engine='python', on_bad_lines='skip')

        logging.info(f"CSV loaded successfully: {file_path}")

    except Exception as e:
        logging.error(f"Error loading CSV file: {str(e)}")
        return None

    try:
        # Convert 'Date' column to datetime with format '%m/%d/%Y'
        df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y', errors='coerce')

        if df['Date'].isnull().sum() > 0:
            logging.warning(f"Warning: {df['Date'].isnull().sum()} dates could not be parsed.")

    except ValueError as e:
        logging.error(f"Error converting 'Date' to datetime: {str(e)}")
        return None

    try:
        # Ensure 'Gross' and 'Net' columns are numeric
        df['Gross'] = pd.to_numeric(df['Gross'], errors='coerce')
        df['Net'] = pd.to_numeric(df['Net'], errors='coerce')

        if df['Gross'].isnull().sum() > 0 or df['Net'].isnull().sum() > 0:
            logging.warning(
                f"Warning: {df['Gross'].isnull().sum()} Gross values and {df['Net'].isnull().sum()} Net values are NaN.")

    except ValueError as e:
        logging.error(f"Error converting 'Gross' or 'Net' to numeric: {str(e)}")
        return None

    # Generate summary statistics
    total_transacciones = len(df)
    fecha_inicio = df['Date'].min().date() if not df['Date'].isnull().all() else None
    fecha_fin = df['Date'].max().date() if not df['Date'].isnull().all() else None

    try:
        # Transacciones por tipo (Description)
        transacciones_por_tipo = df.groupby('Description').size().reset_index(name='Cantidad')

        # Agrupación mensual del monto neto
        df['Mes'] = df['Date'].dt.to_period('M')
        neto_por_mes = df.groupby('Mes')['Net'].sum().reset_index()
        neto_por_mes['Mes'] = neto_por_mes['Mes'].astype(str)

        # Ingresos (transacciones donde Gross > 0)
        df_ingresos = df[df['Gross'] > 0]
        ingresos_por_company = df_ingresos.groupby('Name')['Gross'].sum().reset_index().sort_values(by='Gross',
                                                                                                    ascending=False)

        # Gastos (transacciones donde Gross < 0)
        df_gastos = df[df['Gross'] < 0]
        gastos_por_company = df_gastos.groupby('Name')['Gross'].sum().reset_index().sort_values(by='Gross',
                                                                                                ascending=True)

        # Generate content in Markdown format
        markdown = []
        markdown.append(f"# Reporte del Statement: {fecha_inicio} - {fecha_fin}\n")
        if total_transacciones is not None:
            markdown.append(f"**Total de transacciones:** {total_transacciones}\n")

        if fecha_inicio and fecha_fin:
            markdown.append("## Fecha de Inicio y Fin\n")
            markdown.append(f"Fecha Inicio: {fecha_inicio}\n")
            markdown.append(f"Fecha Fin: {fecha_fin}\n")

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

    except Exception as e:
        logging.error(f"Error generating report: {str(e)}")
        return None


def main():
    # Create a hidden window for file selection
    root = tk.Tk()
    root.withdraw()

    try:
        file_path = filedialog.askopenfilename(
            title="Selecciona el archivo CSV",
            filetypes=[("Archivos CSV", "*.csv"), ("Archivo CSV", "*.CSV")]
        )

        if not file_path:
            print("No se seleccionó ningún archivo.")
            return

        logging.info(f"Selected file: {file_path}")

        markdown_report = generate_report(file_path)

        if markdown_report is None:
            print("Error generating report. Please check the logs for more details.")
            return

        # Save the report in Markdown format in the same directory as the file, with the same base name and suffix '_reporte.md'
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        md_file = os.path.join(os.path.dirname(file_path), f"{base_name}_reporte.md")

        with open(md_file, "w", encoding="utf-8") as f:
            f.write(markdown_report)

        print(f"Reporte generado exitosamente: {md_file}")

    except Exception as e:
        logging.error(f"Error in main function: {str(e)}")


if __name__ == "__main__":
    main()
#workingV2