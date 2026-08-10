# Documentación: ejemplo_ibm_pipeline.py

Este repositorio contiene un ejemplo sencillo de un pipeline ETL (Extract, Transform, Load) escrito en Python. Este README documenta el archivo `ejemplo_ibm_pipeline.py`, explica su propósito, cómo usarlo, el formato esperado de los archivos de entrada y notas sobre mejoras y posibles errores.

## Descripción

`ejemplo_ibm_pipeline.py` es un script que:

- Extrae datos de archivos CSV, JSON Lines y XML en el directorio actual.
- Transforma las medidas: convierte altura de pulgadas a metros y peso de libras a kilogramos.
- Carga el resultado transformado a un archivo CSV objetivo (`transformed_data.csv`).
- Registra el progreso del pipeline en `log_file.txt`.

Es un ejemplo educativo para ilustrar un flujo ETL básico usando pandas y xml.etree.ElementTree.

## Requisitos

- Python 3.7+ (recomendado)
- pandas

Instalación rápida de dependencias:

```bash
python -m pip install pandas
```

## Archivos principales

- `ejemplo_ibm_pipeline.py`: Script con la implementación del ETL.
- `transformed_data.csv`: Archivo de salida (generado por el script).
- `log_file.txt`: Archivo de logs (generado/actualizado por el script).

## Formato de los archivos de entrada

El script espera cualquiera de los siguientes formatos en archivos dentro del directorio de trabajo:

1. CSV
   - Columnas esperadas: `name`, `height`, `weight`
   - Ejemplo:

```csv
name,height,weight
Alice,65,130
Bob,70,180
```

2. JSON Lines (cada línea es un objeto JSON)
   - Campos esperados: `name`, `height`, `weight`
   - Ejemplo (archivo `.json` con `lines=True`):

```jsonl
{"name": "Alice", "height": 65, "weight": 130}
{"name": "Bob", "height": 70, "weight": 180}
```

3. XML
   - Estructura esperada mínima por persona:

```xml
<root>
  <person>
    <name>Alice</name>
    <height>65</height>
    <weight>130</weight>
  </person>
  <person>
    ...
  </person>
</root>
```

El script combina todos los datos leídos en un DataFrame con columnas `name`, `height`, `weight`.

## Funcionamiento (resumen de funciones)

- extract_from_csv(file_to_process)
  - Lee un archivo CSV usando `pandas.read_csv` y devuelve un DataFrame.

- extract_from_json(file_to_process)
  - Lee un archivo JSON en formato "line-delimited" con `pandas.read_json(..., lines=True)` y devuelve un DataFrame.

- extract_from_xml(file_to_process)
  - Parsea un archivo XML con `xml.etree.ElementTree` y extrae los campos `name`, `height` y `weight` construyendo un DataFrame.

- extract()
  - Recorre todos los archivos `*.csv`, `*.json` y `*.xml` en el directorio actual y concatena los datos.
  - Omite el archivo objetivo (`transformed_data.csv`) para evitar re-procesarlo.

- transform(data)
  - Convierte `height` (pulgadas -> metros) con el factor 0.0254 y redondea a 2 decimales.
  - Convierte `weight` (libras -> kilogramos) con el factor 0.45359237 y redondea a 2 decimales.
  - Devuelve el DataFrame transformado.

- load_data(target_file, transformed_data)
  - Escribe el DataFrame transformado a `target_file` usando `to_csv`.

- log_progress(message)
  - Añade una línea en `log_file.txt` con la marca temporal y el mensaje pasado.
  - El script registra el inicio y fin de cada fase (Extract, Transform, Load) y del job completo.

## Salida

- `transformed_data.csv`: contiene todas las filas combinadas con las columnas `name`, `height` (en metros) y `weight` (en kg).
- `log_file.txt`: contiene entradas con marcas temporales y mensajes del progreso.

## Ejecución

Ejecutar el script desde el directorio que contenga los archivos de entrada:

```bash
python ejemplo_ibm_pipeline.py
```

El script procesará todos los archivos `*.csv`, `*.json` y `*.xml` del directorio actual.

## Notas y mejoras sugeridas

- Índice en CSV de salida: Actualmente `to_csv` escribe el índice por defecto. Para evitar una columna índice innecesaria, se recomienda usar `to_csv(target_file, index=False)`.

- Robustez y validación: El script asume que todas las filas tienen columnas/etiquetas `height` y `weight` convertibles a float. Sería conveniente añadir validación/gestión de errores para filas dañadas o formatos inesperados.

- Formato de timestamp: El formato usado en `log_progress` es `'%Y-%h-%d-%H:%M:%S'` — en Python la especificación estándar para el nombre abreviado del mes es `%b`. Usar `%Y-%b-%d-%H:%M:%S` si se pretende incluir el mes abreviado. Alternativamente, usar `%Y-%m-%d %H:%M:%S` para un formato numérico `YYYY-MM-DD HH:MM:SS`.

- Evitar lectura del archivo de salida: El script ya evita concatenar `transformed_data.csv` al comprobar `csvfile != target_file`. Si se cambian nombres, revisar esta lógica.

- Manejo de codificaciones: Al leer archivos CSV o JSON con codificaciones distintas a UTF-8, especificar `encoding` o detectar automáticamente.

- Rendimiento: Para directorios con muchos archivos, usar lectura por chunks o procesar por lotes para reducir uso de memoria.
