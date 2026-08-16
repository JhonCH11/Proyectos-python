# Proyecto ETL - Análisis de los Bancos más Grandes

## 📋 Descripción

Este proyecto implementa un proceso **ETL (Extract, Transform, Load)** para extraer, transformar y cargar información sobre los bancos más grandes del mundo. Los datos se obtienen de una página de Wikipedia archivada, se transforman a múltiples monedas y se almacenan tanto en archivos CSV como en una base de datos SQLite.

## 🎯 Objetivos

- **Extraer** datos de capitalización de mercado de bancos desde una fuente web
- **Transformar** los valores de USD a otras monedas (GBP, EUR, INR)
- **Cargar** los datos en un archivo CSV y en una base de datos SQLite
- **Consultar** y analizar los datos procesados

## 📁 Estructura del Proyecto

```
PROYECTO_ETL/
├── banks_project.py           # Script principal del proyecto ETL
├── exchange_rate.csv          # Archivo de tasas de cambio
├── Largest_banks_data.csv     # Salida: datos de bancos procesados
├── Banks.db                   # Base de datos SQLite
├── code_log.txt               # Registro de ejecución del proceso
└── README.md                  # Este archivo
```

## 🔧 Requisitos

Asegúrate de tener instaladas las siguientes librerías de Python:

```bash
pip install requests
pip install pandas
pip install numpy
pip install beautifulsoup4
```

También necesitarás un archivo `exchange_rate.csv` con las tasas de cambio en el siguiente formato:

```csv
Currency,Rate
GBP,1.27
EUR,1.08
INR,83.45
```

## 🚀 Uso

Para ejecutar el proyecto, simplemente corre el script:

```bash
python banks_project.py
```

### Pasos del Proceso ETL

1. **Extracción (Extract)**
   - Se conecta a la página de Wikipedia archivada
   - Extrae información de la tabla de bancos más grandes
   - Obtiene el nombre y capitalización de mercado en USD

2. **Transformación (Transform)**
   - Lee las tasas de cambio desde `exchange_rate.csv`
   - Convierte los valores a GBP, EUR e INR
   - Redondea los valores a 2 decimales

3. **Carga (Load)**
   - Guarda los datos en `Largest_banks_data.csv`
   - Crea una tabla en la base de datos SQLite `Banks.db`

4. **Consultas**
   - Muestra todos los datos de la tabla
   - Calcula la capitalización de mercado promedio en GBP
   - Lista los 5 bancos principales

## 📊 Funciones Principales

### `log_progress(message)`
Registra el progreso del proceso ETL en un archivo de log con timestamp.

### `extract(url, table_attribs)`
Extrae datos de bancos desde una página web usando BeautifulSoup.

### `transform(df, csv_path)`
Transforma los valores de capitalización de mercado a múltiples monedas.

### `load_to_csv(df, output_path)`
Guarda el DataFrame en un archivo CSV.

### `load_to_db(df, sql_connection, table_name)`
Guarda el DataFrame en una tabla de base de datos SQLite.

### `run_query(query_statement, sql_connection)`
Ejecuta consultas SQL en la base de datos e imprime los resultados.

## 📝 Salidas

### Archivo CSV
- **Nombre**: `Largest_banks_data.csv`
- **Contenido**: Datos de bancos con capitalización en USD, GBP, EUR e INR

### Base de Datos
- **Nombre**: `Banks.db`
- **Tabla**: `Largest_banks`
- **Campos**: Name, MC_USD_Billion, MC_GBP_Billion, MC_EUR_Billion, MC_INR_Billion

### Registro de Log
- **Nombre**: `code_log.txt`
- **Contenido**: Timestamp de cada etapa del proceso ETL

## ✅ Validación

El script ejecuta automáticamente 3 consultas para validar los datos:
1. Muestra todos los registros de la tabla
2. Calcula el promedio de capitalización en GBP
3. Muestra los 5 bancos principales

## 🐛 Solución de Problemas

- **Error de conexión**: Verifica tu conexión a internet
- **Archivo no encontrado**: Asegúrate de que `exchange_rate.csv` esté en la carpeta del proyecto
- **Error de base de datos**: Elimina `Banks.db` si existe y vuelve a ejecutar

## 📄 Licencia

Este proyecto es de uso personal y educativo.

## 👨‍💻 Autor

Proyecto desarrollado como práctica de procesos ETL en Python.
